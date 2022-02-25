import discord
import json 
import asyncio
import platform
import os
import sys
import traceback
import collections
import textwrap
import random
from discord.ext import commands
from discord.ext.commands import bot

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot   
        
    
      
    @commands.Cog.listener(name="on_message")
    async def on_afk_say(self, message):

        if message.guild:
            with open('afks.json', 'r') as f:
                afks = json.load(f)

            try:
                if afks[str(message.author.id)]:
                    # replace the time with python struct, i forgot how it works sorry
                    longmess = int(int(str(message.created_at).split(" ")[1].replace(":", ".").replace(
                        ".", "")) - int(afks[str(message.author.id)]["time"])) / 1000000
                    _min, sec = divmod(longmess, 60)
                    hour, _min = divmod(_min, 60)
                    finalmess = "%d:%02d:%02d" % (hour, _min, sec)
                    await message.channel.send(f'{message.author.mention}, I removed your AFK', delete_after=5)
                    afks.pop(str(message.author.id))
                    with open('afks.json', 'w') as f:
                        json.dump(afks, f, indent=4)

            except KeyError:
                pass

    @commands.Cog.listener(name="on_message")
    async def on_afk_ping(self, message):

        if len(message.mentions):
            with open('afks.json', 'r') as f:
                afks = json.load(f)
            for i in message.mentions:
                if str(i.id) in afks and message.author != message.guild.me:
                    await message.channel.send(
                        f'**{message.author.mention},** `{i.display_name} is currently AFK.`\n**Reason:** `{afks[str(i.id)]["message"]}`',
                        delete_after=5)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
    
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        with open("prefixes.json", "r") as f:
            prefixes=json.load(f)
        prefixes[str(guild.id)]="!"
        with open("prefixes.json","w") as f:
            json.dump(prefixes,f)
            
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        await asyncio.sleep(60)
        del snipe_message_author[message.channel.id]
        del snipe_message_content[message.channel.id]


def setup(bot):
    bot.add_cog(Events(bot))
    print("event Cog is Loaded")