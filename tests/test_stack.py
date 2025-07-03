import aws_cdk as cdk
from ypr_cicd.ypr_cicd_stack import YprCicdStack

def test_stack_synthesis():
    """Test that the stack can be synthesized without errors"""
    app = cdk.App()
    stack = YprCicdStack(app, "TestStack", env_name="dev")
    
    # This will fail if there are any synthesis errors
    template = app.synth()
    assert template is not None

def test_stack_creates_resources():
    """Test that the stack creates expected resources"""
    app = cdk.App()
    stack = YprCicdStack(app, "TestStack", env_name="dev")
    
    # Synthesize to CloudFormation
    template = cdk.assertions.Template.from_stack(stack)
    
    # Check resource counts
    template.resource_count_is("AWS::S3::Bucket", 1)
    template.resource_count_is("AWS::SSM::Parameter", 1)