from datetime import datetime, timedelta
from uuid import uuid4

EXPIRATION_DAYS = 1


class Session:
    def __init__(self, username, session_token=None):
        if session_token is None:
            session_token = uuid4()

        self.session_token = session_token
        self.username = username
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(days=EXPIRATION_DAYS)
        self.ttl = int(datetime.timestamp(self.expires_at))

    @property
    def display_created_at(self):
        return self.created_at.strftime("%Y/%m/%d, %H:%M:%S")

    @property
    def display_expires_at(self):
        return self.expires_at.strftime("%Y/%m/%d, %H:%M:%S")

    def __repr__(self):
        print(
            f"Session {self.session_token} for {self.username}, for {self.display_created_at} to {self.display_expires_at}"
        )
        return f"Session {self.session_token} for {self.username}, for {self.display_created_at} to {self.display_expires_at}"
