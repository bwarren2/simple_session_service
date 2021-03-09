import os
import subprocess

from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_dynamodb as dynamodb


class PipelineWebinarStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = dynamodb.Table(
            self,
            "SessionTable",
            partition_key=dynamodb.Attribute(
                name="SessionToken", type=dynamodb.AttributeType.STRING
            ),
        )

        this_dir = os.path.dirname(__file__)
        if not os.environ.get("SKIP_PIP"):
            # Note: Pip will create the output dir if it does not exist
            subprocess.check_call(
                f"pip install -U -r \
                    {os.path.join(this_dir, 'lambdas', 'requirements.txt')} \
                    -t {os.path.join(this_dir, 'layer', 'python')}".split()
            )
        layer = lmb.LayerVersion(
            self,
            "BaseLayer",
            code=lmb.Code.asset(os.path.join(this_dir, "layer")),
        )
        codeAsset = lmb.Code.from_asset(os.path.join(this_dir, "lambdas"))

        hello_handler = lmb.Function(
            self,
            "Handler",
            layers=[layer],
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="handlers.hello",
            code=codeAsset,
        )
        create_handler = lmb.Function(
            self,
            "CreateHandler",
            layers=[layer],
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="handlers.create",
            code=codeAsset,
            environment={"SESSION_TABLE_NAME": table.table_name},
        )
        listing_handler = lmb.Function(
            self,
            "ListingHandler",
            layers=[layer],
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="handlers.listing",
            code=codeAsset,
            environment={"SESSION_TABLE_NAME": table.table_name},
        )
        retrieve_handler = lmb.Function(
            self,
            "RetrieveHandler",
            layers=[layer],
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="handlers.retrieve",
            code=codeAsset,
            environment={"SESSION_TABLE_NAME": table.table_name},
        )

        table.grant_read_data(listing_handler)
        table.grant_read_write_data(create_handler)

        api = apigw.LambdaRestApi(
            self,
            "Gateway",
            description="Endpoint for simple lambda-powered web service",
            handler=hello_handler.current_version,
            proxy=False,
        )
        api.root.add_method("GET", integration=apigw.LambdaIntegration(hello_handler))

        items = api.root.add_resource("sessions")
        items.add_method("GET", integration=apigw.LambdaIntegration(listing_handler))
        items.add_method("POST", integration=apigw.LambdaIntegration(create_handler))

        item = items.add_resource("{item}")
        item.add_method(
            "GET", integration=apigw.LambdaIntegration(retrieve_handler)
        )  # GET /items/{item}
        self.url_output = core.CfnOutput(self, "Url", value=api.url)
