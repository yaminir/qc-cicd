import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class YprCicdStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC", max_azs=2)
        
        ec2.Instance(self, "Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2()
        )