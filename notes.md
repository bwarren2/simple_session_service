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
