# CDK Pipelines webinar

## Setup

DO NOT use pyenv.  Ships with a virtualenv starter.

Need to add ```  "python.autoComplete.extraPaths": [
    ".venv/lib/python3.7/site-packages"
  ],
``` to your settings for autocomplete.

Create Github token.  Put it in secrets manager as a plain text secret.  Remember the name.

## Bootstrap

cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess


20210301
With proxy=false, need to define all the routes or they sever error
Add to root with api.root.add_method

ApiGWv2 has more natural ergonomics, but might not be fully CDK'd yet
Don't need to split handler across files, DO need unique names on functions
Tests are great, use em.

20210306
Use a lambda layer.  The bundling docker image doesn't communicate with the local docker host correctly.
Layers get loaded in /opt/.

20210307
Create lambda layer correctly, with the subprocess call writing to the place the lambda reads from, and it Just Works!

20210308
Found where artifacts are stored for my substack.  In S3:
default-pipelineartifactsbucketaea9a052-lpsqy28hbwaq/WebinarPipeline/Artifact_B/9qG6Cbj
Inside the PreProdWebService8885BFD7.template file.

ExpressionAttributeValues are a dict of replacement implies dict of type implies value.  Call this a KeyTypeValue
Dynobase uses not-ADB-recommended DDB lookups instead of client get/put/query/scan.
PutItem signature: TableName, Item=KeyTypeValue, ConditionExpression=function(attr)
GetItem signature: Tablename, Key=KeyTypeValue
