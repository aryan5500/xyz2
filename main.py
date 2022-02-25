import discord
import time
import asyncio
import platform
import random
import os
import sys
import traceback
import collections
import ffmpeg
import datetime
import json
import os
import textwrap
import secrets
from io import BytesIO
from discord.ext import commands
from discord import permissions
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from datetime import datetime, timedelta
from discord.ext.commands import clean_content
from discord.ext.commands import cooldown, BucketType



async def get_prefix(self,message: discord.Message):
        with open("prefixes.json","r") as f:
            prefixes = json.load(f)
        guild_prefix = prefixes[str(message.guild.id)]
        return (guild_prefix)

   

intents = discord.Intents.default()  
intents.members = True  
bot=commands.Bot(command_prefix =get_prefix,intents=intents)
bot.remove_command('help')



extensions=[
            "cogs.moderation","cogs.Events", "cogs.fun", "cogs.utiles","cogs.Errors","cogs.Admin","cogs.music","cogs.help","cogs.giveaway"
]
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"error loading {extension}",file=sys.stderr)
            traceback.print_exc()

bot.run("OTI1NzgwMzcyNTQzOTA1ODQy.YcyGKA.ivmjo8srsZhGrQxC_xsaINIudi4") 