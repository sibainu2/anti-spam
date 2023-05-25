import sys
sys.path.append('../')
import time
import asyncio
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
import MeCab

class User():
    def __init__(self,id:int,name:str,mute:bool=False,threat:float=0,message:list=[]) -> None:
        self.id = id
        self.name = name
        self.mute = mute
        self.threat = threat
        self.message = message#messageのIDのリストです。

    def add_message(self,message_id:int):
        self.message.append(message_id)

    def silence(self):
        self.mute = True

    def unsilence(self):
        self.mute = False

class Message():
    def __init__(self,id:int,content:str,user:User,delete:bool):
        self.id = id
        self.content = content
        self.user = user#userのIDです。
        self.delete = delete

class TmpGuild():
    def __init__(self):
        self.messages:list[Message] = []
        self.users:list[User] = []

        self.spam_messages:list[Message] = []
        self.spam_users:list[User] = []



def analyze_text(text):
    # MeCabの初期化
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

    # テキストを形態素解析して結果を取得
    node = m.parseToNode(text)

    # 分解した内容、分解した意味、および読みを格納するリスト
    morphemes = []
    meanings = []
    readings = []

    while node:
        surface = node.surface
        feature = node.feature.split(",")
        morpheme = surface
        meaning = feature[0]
        reading = feature[7] if len(feature) > 7 else ""
        morphemes.append(morpheme)
        meanings.append(meaning)
        readings.append(reading)
        node = node.next

    # 先頭ノードは空なので削除
    morphemes = morphemes[1:]
    meanings = meanings[1:]
    readings = readings[1:]
    output = list(zip(morphemes, meanings, readings))

    if output and output[-1] == ('', 'BOS/EOS', '*'):
        output.pop()  # リストの最後の要素を削除

    return output



async def on_message(message:Message):

    user = message.user
    print(message.id,user.name,analyze_text(message.content))
    




