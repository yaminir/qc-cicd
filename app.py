#!/usr/bin/env python3
import aws_cdk as cdk
from ypr_cicd.pipeline_stack import PipelineStack

app = cdk.App()
PipelineStack(app, "PipelineStack", env=cdk.Environment(
    account="014111701234",  # Pipeline account
    region="us-east-1"
))
app.synth()