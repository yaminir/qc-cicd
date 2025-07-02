# QC CI/CD Project

AWS CDK project with automated CI/CD pipeline that deploys an S3 bucket.

## Prerequisites

- AWS CLI configured with appropriate permissions
- Node.js and npm installed
- Python 3.9+ installed
- Git configured

## Initial Setup

1. **Install AWS CDK**
   ```bash
   npm install -g aws-cdk
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Bootstrap AWS environment** (one-time setup)
   ```bash
   cdk bootstrap
   ```

## Deployment

### First-time Pipeline Deployment

1. **Set up GitHub connection**
   - Go to AWS Console → CodePipeline → Settings → Connections
   - Create GitHub connection and note the ARN
   - Update `connection_arn` in `ypr_cicd/pipeline_stack.py`

2. **Deploy the pipeline**
   ```bash
   cdk deploy PipelineStack
   ```

### Deploying Application Changes

Once the pipeline is deployed, all application changes are deployed automatically:

1. **Make your changes** to any stack files
2. **Commit and push**
   ```bash
   git add .
   git commit -m "Your change description"
   git push
   ```
3. **Pipeline automatically triggers** and deploys changes

## Project Structure

```
├── app.py                    # CDK app entry point
├── ypr_cicd/
│   ├── pipeline_stack.py     # CI/CD pipeline definition
│   └── ypr_cicd_stack.py    # Application stack (S3 bucket)
├── requirements.txt          # Python dependencies
└── README.md
```

## Important Notes

- **Never run `cdk deploy` for application stacks** - let the pipeline handle it
- **Only deploy PipelineStack locally** when changing the pipeline itself
- Pipeline automatically triggers on pushes to main branch
- Manual trigger available in AWS Console → CodePipeline

## Resources Created

- **CodePipeline**: Automated CI/CD pipeline
- **S3 Bucket**: Versioned bucket with destroy policy
- **IAM Roles**: Required pipeline execution roles

## Troubleshooting

- Check CodeBuild logs in AWS Console for build failures
- Ensure GitHub connection is active
- Verify AWS permissions for CDK operations