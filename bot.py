from interactions import *
from interactions.api.events import Component
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
url = f"mongodb+srv://dumerat:{os.environ.get('PASS')}@bddisc.diuwvtd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url, server_api=ServerApi('1'))
db = client["m2i"]

user_db = db["user"]
event_db = db["event"]
homework_db = db["homework"]
dash_db = db["dashboard"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    print("Don't forget to check authorized IP")

bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_startup():
    print(f"Salut c'est {bot.user.display_name} fait par {bot.owner.display_name}")
    await bot.wait_until_ready()

@slash_command(name="hi")
async def hello(ctx: SlashContext):
    await ctx.send("Hello world!")

bot.load_extension("dashboard", bot, db=db)
bot.start(os.environ.get('TOKEN'))