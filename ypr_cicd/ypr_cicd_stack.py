import aws_cdk as cdk
from aws_cdk import aws_s3 as s3, aws_ssm as ssm
from constructs import Construct
from .config import ENVIRONMENTS


class YprCicdStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get environment-specific configuration
        env_config = ENVIRONMENTS[env_name]

        # Environment-specific S3 bucket
        bucket = s3.Bucket(
            self, "MyBucket",
            versioned=env_config["bucket_versioning"],
            removal_policy=getattr(cdk.RemovalPolicy, env_config["removal_policy"])
        )

        # Environment-specific SSM parameter
        ssm.StringParameter(
            self, "MyParameter",
            parameter_name=f"{env_config['parameter_prefix']}/bucket-name",
            string_value=bucket.bucket_name,
            description=f"S3 bucket name for {env_name} environment"
        )

        # Add environment tags
        cdk.Tags.of(self).add("Environment", env_config["environment_tag"])
        cdk.Tags.of(self).add("Project", "QC-CICD")
