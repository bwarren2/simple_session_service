from pipelines_webinar.lambdas.sessions import models, schemas
from freezegun import freeze_time
from datetime import datetime


@freeze_time("2020-01-01")
def test_schema():
    session_data = {"username": "ben"}
    session = schemas.SessionSchema().load(session_data)
    assert session.username == "ben"
    assert (
        datetime.fromtimestamp(session.ttl).strftime("%Y/%m/%d, %H:%M:%S")
        == "2020/01/02, 00:00:00"
    )
    assert type(session.ttl) == int
    assert session.created_at.strftime("%Y/%m/%d, %H:%M:%S") == "2020/01/01, 00:00:00"
    assert session.expires_at.strftime("%Y/%m/%d, %H:%M:%S") == "2020/01/02, 00:00:00"
