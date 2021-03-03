from os import path
from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw


class PipelineWebinarStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        this_dir = path.dirname(__file__)
        hello_handler = lmb.Function(
            self,
            "Handler",
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="handler.handler",
            code=lmb.Code.from_asset(path.join(this_dir, "lambda")),
        )
        custom_handler = lmb.Function(
            self,
            "Handler",
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="handler.custom",
            code=lmb.Code.from_asset(path.join(this_dir, "lambda")),
        )

        api = apigw.LambdaRestApi(
            self,
            "Gateway",
            description="Endpoint for simple lambda-powered web service",
            handler=hello_handler.current_version,
            proxy=False,
        )

        items = api.root.add_resource("items")
        items.add_method("GET", integration=apigw.LambdaIntegration(custom_handler))

        self.url_output = core.CfnOutput(self, "Url", value=api.url)
