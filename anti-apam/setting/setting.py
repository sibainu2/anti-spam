
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, event
import datetime
import asyncio
import data
import random
import string


DB_USER = 'postgres'
DB_PASSWORD = '1224'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

# PostgreSQLに接続するためのURLを作成
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# create_engine関数でエンジンを作成
engine = create_engine(DATABASE_URL)

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
    mute = Column(Boolean)#発言権
    threat = Column(Integer)#脅威
    messages = relationship("Message", back_populates="user")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="messages")

    def __init__(self, message, user):
        if user.mute:
            raise ValueError('Cannot add message to muted user')
        self.message = message
        self.user = user

#Base.metadata.drop_all(engine)
# テーブルを作成
Base.metadata.create_all(engine)

# データを追加
#or name in data.USER_NAMES:
#   user = User(name=name, mute=False, threat=0)
#   session.add(user)
#ession.commit()

# データを取得
#users = session.query(User).all()
#for user in users:
#    print(user.name, user.id)


from anti_spam_tool.event import on_message
@event.listens_for(Message, 'after_insert')
def on_new_message(mapper, connection, target):
    global loop, task
    if type(target) is Message:
        #print('New message added:', target.message)
        
        loop = asyncio.get_event_loop()
        task = loop.create_task(on_message(target))


#ここから下は荒らし
def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

async def spam(number):
    user = session.get(User,number)
    for i in range(1,random.randint(5,10)):
        try:
            message = Message(message=f'こんにちわ日本語って入るの？{randomname(5)}', user=user)
            session.add(message)
            session.commit()
            await asyncio.sleep(random.uniform(0.05,0.5))
        except ValueError:
            print("書き込みに失敗しました。")
        



async def spam_main():
    spam_user = [1,2,3,4,5,6,7,8,9,10]
    tasks = [asyncio.create_task(spam(user_id)) for user_id in spam_user]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(spam_main())




#loop.run_until_complete(task)

