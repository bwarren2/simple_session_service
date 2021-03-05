from datetime import datetime, timedelta
from uuid import uuid4

EXPIRATION_DAYS = 1


class Session:
    def __init__(self, username, uid=None):
        if uid is None:
            uid = uuid4()

        self.uid = uid
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
            f"Session {self.uid} for {self.username}, for {self.display_created_at} to {self.display_expires_at}"
        )
        return f"Session {self.uid} for {self.username}, for {self.display_created_at} to {self.display_expires_at}"
