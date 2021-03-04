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
    assert len(functions) == 3
    assert functions[0]["Properties"]["Handler"] == "sessions.hello"
    assert functions[1]["Properties"]["Handler"] == "sessions.create"
    assert functions[2]["Properties"]["Handler"] == "sessions.listing"
