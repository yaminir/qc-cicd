import pytest
import aws_cdk as cdk
from ypr_cicd.ypr_cicd_stack import YprCicdStack

def test_stack_creates_bucket():
    """Test that the stack creates an S3 bucket"""
    app = cdk.App()
    stack = YprCicdStack(app, "TestStack", env_name="dev")
    
    # Synthesize the stack to CloudFormation template
    template = cdk.assertions.Template.from_stack(stack)
    
    # Assert S3 bucket is created (dev has versioning disabled, so no VersioningConfiguration)
    template.has_resource("AWS::S3::Bucket")

def test_stack_creates_ssm_parameter():
    """Test that the stack creates an SSM parameter"""
    app = cdk.App()
    stack = YprCicdStack(app, "TestStack", env_name="dev")
    
    template = cdk.assertions.Template.from_stack(stack)
    
    # Assert SSM parameter is created
    template.has_resource_properties("AWS::SSM::Parameter", {
        "Name": "/dev/myapp/bucket-name",
        "Type": "String"
    })