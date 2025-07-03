ENVIRONMENTS = {
    "dev": {
        "account": "387385193794",
        "region": "us-east-1",
        "bucket_versioning": False,
        "parameter_prefix": "/dev/myapp",
        "removal_policy": "DESTROY",
        "environment_tag": "development"
    },
    "prod": {
        "account": "093004983829",
        "region": "us-east-1",
        "bucket_versioning": True,
        "parameter_prefix": "/prod/myapp",
        "removal_policy": "RETAIN",
        "environment_tag": "production"
    }
}
