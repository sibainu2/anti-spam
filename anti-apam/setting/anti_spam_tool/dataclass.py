from sqlalchemy import DateTime
import datetime


class User():
    def __init__(self, id, name, mute, message_count, threat_level) -> None:
        self.id = id
        self.name = name
        self.mute = mute
        self.message_count = message_count
        self.threat_level = threat_level


class Message():
    def __init__(self, id: int, user: User, content: str, threat_level) -> None:
        self.id = id
        self.user = user
        self.content = content
        self.threat_level = threat_level


class SpamSession():
    def __init__(self) -> None:
        self.send_all_user = []
        self.mute_user = []
        self.all_message = []
        self.start_time: DateTime = datetime.datetime.utcnow()
        self.latest_time: DateTime = datetime.datetime.utcnow()
        self.end_time: DateTime = None
