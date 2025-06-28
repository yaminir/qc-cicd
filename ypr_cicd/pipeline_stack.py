import aws_cdk as cdk
from aws_cdk import pipelines
from constructs import Construct
from .ypr_cicd_stack import YprCicdStack

class PipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(self, "Pipeline",
            pipeline_name="YprCicdPipeline",
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.connection("yaminir/qc-cicd", "main",
                    connection_arn="arn:aws:codeconnections:us-east-1:014111701234:connection/771d8fb0-36c6-4734-993e-0cfe1a09d178",
                    trigger_on_push=True),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt", 
                    "cdk synth"
                ]
            )
        )

        pipeline.add_stage(AppStage(self, "Deploy"))

class AppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        YprCicdStack(self, "YprCicdStack")