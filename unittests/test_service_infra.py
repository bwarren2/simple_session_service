from aws_cdk import core
from pipelines_webinar.pipelines_webinar_stack import PipelineWebinarStack


def test_lambda_handler():

    app = core.App()

    PipelineWebinarStack(app, "Stack")

    template = app.synth().get_stack_by_name("Stack").template
    functions = [
        resource
        for resource in template["Resources"].values()
        if resource["Type"] == "AWS::Lambda::Function"
    ]
    assert len(functions) == 2
    assert functions[0]["Properties"]["Handler"] == "handler.handler"
    assert functions[1]["Properties"]["Handler"] == "custom.custom"
