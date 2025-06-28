import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class YprCicdStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3.Bucket(self, "MyBucket",
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )