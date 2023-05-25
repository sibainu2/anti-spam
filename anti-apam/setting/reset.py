
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, event
import datetime
import asyncio
import data
import random
import string

# create_engine関数でエンジンを作成
engine = create_engine('sqlite:///test.db', echo=True)

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

# テーブルを作成するためのベースクラスを作成
Base = declarative_base()

# テーブルの定義
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    mute = Column(Boolean,default=False)#発言権
    threat = Column(Integer)#脅威
    messages = relationship("Message", back_populates="user")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="messages")

    def __init__(self, content, user):
        if user is None:
            raise ValueError("Cannot add message because user is from")
        if user.mute:
            raise ValueError('Cannot add message to muted user')
        self.content = content
        self.user = user


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    # テーブルを作成
    Base.metadata.create_all(engine)

    # データを追加
    for name in data.USER_NAMES:
        user = User(name=name, mute=False, threat=0)
        session.add(user)
    session.commit()

    # データを取得
    users = session.query(User).all()
    for user in users:
        print(user.name, user.id)

    messages = session.query(Message).all()
    for message in messages:
        print(message.user.name, message.id)