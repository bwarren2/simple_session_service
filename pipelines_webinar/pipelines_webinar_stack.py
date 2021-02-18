from os import path
from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw


class PipelineWebinarStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        this_dir = path.dirname(__file__)
        handler = lmb.Function(
            self,
            "Handler",
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="handler.handler",
            code=lmb.Code.from_asset(path.join(this_dir, "lambda")),
        )

        gw = apigw.LambdaRestApi(
            self,
            "Gateway",
            description="Endpoint for simple lambda-powered web service",
            handler=handler.current_version,
        )

        self.url_output = core.CfnOutput(self, "Url", value=gw.url)
