from motor.motor_asyncio import AsyncIOMotorClient
import config

ChatBot = AsyncIOMotorClient(config.MONGO_URL)
db = ChatBot["ChatBot"]  
usersdb = db["users"]    
chatsdb = db["chats"]    

from .chats import *
from .fsub import *
