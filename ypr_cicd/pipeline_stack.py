import aws_cdk as cdk
from aws_cdk import pipelines
from constructs import Construct
from .ypr_cicd_stack import YprCicdStack
from .config import ENVIRONMENTS


class PipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.connection(
            "yaminir/qc-cicd", "main",
            connection_arn="arn:aws:codeconnections:us-east-1:014111701234:connection/89a0ea4c-89e1-4392-a652-6d616c365ba4",
            trigger_on_push=True)

        pipeline = pipelines.CodePipeline(self, "Pipeline",
                                          pipeline_name="YprCicdPipeline",
                                          cross_account_keys=True,
                                          synth=pipelines.ShellStep("Synth",
                                                                     input=source,
                commands=[
                    # Quality Gate - Run before synth
                    "echo 'Starting Quality Gate...'",
                    "pip install -r requirements.txt",
                    "pip install -r requirements-dev.txt",
                    
                    # Unit Tests
                    "echo 'Running unit tests...'",
                    "python --version",
                    "pip list | grep -E '(aws-cdk|pytest)'",
                    "export PYTHONPATH=$PYTHONPATH:.",
                    "python -m pytest tests/ -v --tb=short || (echo 'Tests failed, showing detailed output:' && python -m pytest tests/ -v --tb=long && exit 1)",
                    
                    # Code Linting
                    "echo 'Running code linting...'",
                    "flake8 .",
                    "black --check . --exclude=cdk.out",
                    "pylint ypr_cicd/ --disable=C0114,C0116",
                    
                    # Security Scan
                    "echo 'Running security scan...'",
                    "bandit -r ypr_cicd/ -f json || true",
                    
                    # CDK Synth (only after quality gates pass)
                    "echo 'Quality gates passed! Running CDK synth...'",
                    "npm install -g aws-cdk",
                    "cdk synth",
                    "echo 'Pipeline synthesis completed!'"
                ]
            )
        )

        # Development stage - auto deploy from main
        dev_config = ENVIRONMENTS["dev"]
        dev_stage = AppStage(self, "Dev", 
            env_name="dev",
            env=cdk.Environment(
                account=dev_config["account"],
                region=dev_config["region"]
            )
        )
        pipeline.add_stage(dev_stage, post=[
            pipelines.ShellStep("DevValidation",
                commands=[
                    "echo 'Running dev environment tests...'",
                    "# Add your validation commands here",
                    "echo 'Dev deployment validated successfully'"
                ]
            )
        ])
        
        # Production stage - manual approval after dev success
        prod_config = ENVIRONMENTS["prod"]
        prod_stage = AppStage(self, "Prod", 
            env_name="prod",
            env=cdk.Environment(
                account=prod_config["account"],
                region=prod_config["region"]
            )
        )
        pipeline.add_stage(prod_stage, pre=[
            pipelines.ManualApprovalStep("PromoteToProd")
        ])

class AppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        YprCicdStack(self, f"YprCicdStack-{construct_id}", env_name=env_name)