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
