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


@freeze_time("2020-01-01")
def test_create_handler_successful(mocker):
    input_event = {"body": '{\n "username": "ben"\n}', "isBase64Encoded": False}
    client_mock = mocker.MagicMock()
    mocker.patch("boto3.resource", lambda x: client_mock)
    mocker.patch("sessions.models.uuid4", lambda: "A")
    output = handlers.create(input_event, {})
    assert output == {
        "body": "Session A for ben, for 2020/01/01, 00:00:00 to 2020/01/02, 00:00:00",
        "statusCode": "201",
    }
    client_mock.Table.assert_called_with(os.getenv("SESSION_TABLE_NAME"))

    client_mock.Table.return_value.put_item.assert_called_with(
        ConditionExpression="attribute_not_exists(SessionToken)",
        Item={
            "SessionToken": "A",
            "Username": "ben",
            "CreatedAt": "2020-01-01 00:00:00",
            "ExpiresAt": "2020-01-02 00:00:00",
            "TTL": "1577923200",
        },
        ReturnValues="ALL_OLD",
    )


def test_create_handler_invalid_json(mocker):
    input_event = {"body": '{\n "username": }', "isBase64Encoded": False}
    mocker.patch("sessions.models.uuid4", lambda: "A")
    output = handlers.create(input_event, {})
    assert output == {
        "body": "Invalid request body",
        "statusCode": "400",
    }


def test_create_handler_no_body(mocker):
    input_event = {"isBase64Encoded": False}
    mocker.patch("sessions.models.uuid4", lambda: "A")
    output = handlers.create(input_event, {})
    assert output == {
        "body": "Missing request body",
        "statusCode": "400",
    }
