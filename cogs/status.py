import discord
import os
from discord.ext import commands, tasks
from itertools import cycle

class status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle(["Vodka Or beer? ",f"listening on {len(self.bot.guilds)} server's","keep it a secret!"])

    @tasks.loop(seconds=10.0)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.status)))
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.change_status.start()
        print(f"Logged in as {self.bot.user}, d.py V{discord.__version__}")    

def setup(bot):
    bot.add_cog(status(bot))
    print("status is ready")