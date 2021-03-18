import os
from aws_cdk import core
from pipelines_webinar.pipelines_webinar_stack import PipelineWebinarStack
from pipelines_webinar.lambdas import handlers
from freezegun import freeze_time


def test_lambda_handler():

    app = core.App()

    PipelineWebinarStack(app, "Stack")

    template = app.synth().get_stack_by_name("Stack").template
    functions = [
        resource
        for resource in template["Resources"].values()
        if resource["Type"] == "AWS::Lambda::Function"
    ]
    assert len(functions) == 4
    assert functions[0]["Properties"]["Handler"] == "handlers.hello"
    assert functions[1]["Properties"]["Handler"] == "handlers.create"
    assert functions[2]["Properties"]["Handler"] == "handlers.listing"
    assert functions[3]["Properties"]["Handler"] == "handlers.retrieve"
