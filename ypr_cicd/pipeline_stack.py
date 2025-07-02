import aws_cdk as cdk
from aws_cdk import pipelines
from constructs import Construct
from .ypr_cicd_stack import YprCicdStack

class PipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(self, "Pipeline",
            pipeline_name="YprCicdPipeline",
            cross_account_keys=True,
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.connection("yaminir/qc-cicd", "main",
                    connection_arn="arn:aws:codeconnections:us-east-1:014111701234:connection/89a0ea4c-89e1-4392-a652-6d616c365ba4",
                    trigger_on_push=True),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt", 
                    "cdk synth"
                ]
            )
        )

        # Development stage - auto deploy from main
        dev_stage = AppStage(self, "Dev", env=cdk.Environment(
            account="387385193794",  # Replace with actual dev account ID
            region="us-east-1"
        ))
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
        prod_stage = AppStage(self, "Prod", env=cdk.Environment(
            account="093004983829",  # Replace with actual prod account ID
            region="us-east-1"
        ))
        pipeline.add_stage(prod_stage, pre=[
            pipelines.ManualApprovalStep("PromoteToProd")
        ])

class AppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        YprCicdStack(self, f"YprCicdStack-{construct_id}")