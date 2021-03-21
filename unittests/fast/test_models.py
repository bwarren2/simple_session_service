from session_tokens_app.lambdas.sessions import models
from freezegun import freeze_time
from datetime import datetime


@freeze_time("2020-01-01")
def test_session_create():
    session = models.Session("ben")
    assert session.ttl == 1577923200  # Jan 2 2021
    assert (
        datetime.fromtimestamp(session.ttl).strftime("%Y/%m/%d, %H:%M:%S")
        == "2020/01/02, 00:00:00"
    )
    assert type(session.ttl) == int
    assert session.username == "ben"
    assert session.created_at.strftime("%Y/%m/%d, %H:%M:%S") == "2020/01/01, 00:00:00"
    assert session.expires_at.strftime("%Y/%m/%d, %H:%M:%S") == "2020/01/02, 00:00:00"
