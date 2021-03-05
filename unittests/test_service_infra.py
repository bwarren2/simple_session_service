from aws_cdk import core
from pipelines_webinar.pipelines_webinar_stack import PipelineWebinarStack
from pipelines_webinar.lambdas import sessions
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
    assert len(functions) == 3
    assert functions[0]["Properties"]["Handler"] == "sessions.hello"
    assert functions[1]["Properties"]["Handler"] == "sessions.create"
    assert functions[2]["Properties"]["Handler"] == "sessions.listing"


@freeze_time("2020-01-01")
def test_create_handler_successful(mocker):
    input_event = {"body": '{\n "username": "ben"\n}', "isBase64Encoded": False}
    mocker.patch("pipelines_webinar.lambdas.models.uuid4", lambda: "A")
    output = sessions.create(input_event, {})
    assert output == {
        "body": "Session A for ben, for 2020/01/01, 00:00:00 to 2020/01/02, 00:00:00",
        "statusCode": "201",
    }


def test_create_handler_invalid_json(mocker):
    input_event = {"body": '{\n "username": }', "isBase64Encoded": False}
    mocker.patch("pipelines_webinar.lambdas.models.uuid4", lambda: "A")
    output = sessions.create(input_event, {})
    assert output == {
        "body": "Invalid request body",
        "statusCode": "400",
    }


def test_create_handler_no_body(mocker):
    input_event = {"isBase64Encoded": False}
    mocker.patch("pipelines_webinar.lambdas.models.uuid4", lambda: "A")
    output = sessions.create(input_event, {})
    assert output == {
        "body": "Missing request body",
        "statusCode": "400",
    }
