import os
from collections import OrderedDict
from pipelines_webinar.lambdas import handlers
from freezegun import freeze_time


@freeze_time("2020-01-01")
def test_create_handler_successful(mocker):
    input_event = {"body": '{\n "username": "ben"\n}', "isBase64Encoded": False}
    resource_mock = mocker.MagicMock()
    mocker.patch("boto3.resource", lambda x: resource_mock)
    mocker.patch("sessions.models.uuid4", lambda: "A")
    output = handlers.create(input_event, {})
    expected_body = (
        '{"session_token": "A", "username": "ben", "created_at": "2020-01-01T00:00:00", '
        '"expires_at": "2020-01-02T00:00:00", "ttl": 1577923200}'
    )
    assert output == {
        "body": expected_body,
        "statusCode": "201",
        "headers": {"Content-Type": "application/json"},
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


# def test_create(mocker):
#     input_event = {"body": '{\n "username": "ben"\n}', "isBase64Encoded": False}
#     handlers.create(input_event, {})


# def test_check(mocker):
#     input_event = {
#         "pathParameters": {"item": "c9ae0f18-397e-4f71-b6e9-f93c0c83c974"},
#         "isBase64Encoded": False,
#     }
#     print(handlers.retrieve(input_event, {}))
