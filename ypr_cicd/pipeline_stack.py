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
                input=pipelines.CodePipelineSource.git_hub("YOUR_GITHUB_USERNAME/ypr-cicd", "main"),
                commands=["pip install -r requirements.txt", "cdk synth"]
            )
        )

        pipeline.add_stage(AppStage(self, "Deploy"))

class AppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        YprCicdStack(self, "YprCicdStack")