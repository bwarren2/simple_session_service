
# Simple Sessions Service

This is a toy project to get comfortable gluing many different AWS services together.

Nominally, it does CRUD operations on tokens served under a `sessions/{id}` resource.

The _actual_ thing it was made to do is:

 * Use AWS CDK.
 * Set up a code pipeline with multiple environments cued off merging into `master`.
 * Make a python lambda layer.
 * In each test environment, spin up an APIGateway endpoint with Lambda proxy integrations talking to a DynamoDB table.
 * Promote between environments based on passing unit and integration tests.
 * Use pytest with some plugins and to mock and freeze time as needed, and inline coverage in VSCode.

AKA act like a professional cloud-native project.  In theory, adding more functionality is just extending this pattern.
# Development
Activate your venv:

```
$ source .venv/bin/activate
```

# Testing

`export AWS_PROFILE=BenW` for the tests that actually touch AWS.

Use `pytest --cov=session_tokens_app/ --cov-report xml:cov.xml tests/ -vv`
