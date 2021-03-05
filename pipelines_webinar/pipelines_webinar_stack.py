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
            handler="sessions.handlers.hello",
            code=lmb.Code.from_asset(path.join(this_dir, "lambdas")),
        )
        create_handler = lmb.Function(
            self,
            "CreateHandler",
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="sessions.handlers.create",
            code=lmb.Code.from_asset(path.join(this_dir, "lambdas")),
        )

        listing_handler = lmb.Function(
            self,
            "ListingHandler",
            runtime=lmb.Runtime.PYTHON_3_7,
            handler="sessions.handlers.listing",
            code=lmb.Code.from_asset(path.join(this_dir, "lambdas")),
        )

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

        self.url_output = core.CfnOutput(self, "Url", value=api.url)
