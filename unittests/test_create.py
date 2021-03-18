import os
from collections import OrderedDict
from aws_cdk import core
from pipelines_webinar.pipelines_webinar_stack import PipelineWebinarStack
from pipelines_webinar.lambdas import handlers
from freezegun import freeze_time


@freeze_time("2020-01-01")
def test_create_handler_successful(mocker):
    input_event = {"body": '{\n "username": "ben"\n}', "isBase64Encoded": False}
    resource_mock = mocker.MagicMock()
    mocker.patch("boto3.resource", lambda x: resource_mock)
    mocker.patch("sessions.models.uuid4", lambda: "A")
    output = handlers.create(input_event, {})
    assert output == {
        "body": "Session A for ben, for 2020/01/01, 00:00:00 to 2020/01/02, 00:00:00",
        "statusCode": "201",
    }
    resource_mock.Table.assert_called_with(os.getenv("SESSION_TABLE_NAME"))

    resource_mock.Table.return_value.put_item.assert_called_with(
        ConditionExpression="attribute_not_exists(session_token)",
        Item=OrderedDict(
            [
                ("session_token", "A"),
                ("username", "ben"),
                ("created_at", "2020-01-01T00:00:00"),
                ("expires_at", "2020-01-02T00:00:00"),
                ("ttl", 1577923200),
            ]
        ),
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


# def test_no_mocks_test_create_handler_successful(mocker):
#     input_event = {"body": '{\n "username": "ben"\n}', "isBase64Encoded": False}
#     output = handlers.create(input_event, {})
#     assert output == {
#         "body": "Session A for ben, for 2020/01/01, 00:00:00 to 2020/01/02, 00:00:00",
#         "statusCode": "201",
#     }
#     resource_mock.Table.assert_called_with(os.getenv("SESSION_TABLE_NAME"))

#     resource_mock.Table.return_value.put_item.assert_called_with(
#         ConditionExpression="attribute_not_exists(SessionToken)",
#         Item={
#             "SessionToken": "A",
#             "Username": "ben",
#             "CreatedAt": "2020-01-01 00:00:00",
#             "ExpiresAt": "2020-01-02 00:00:00",
#             "TTL": "1577923200",
#         },
#         ReturnValues="ALL_OLD",
#     )
