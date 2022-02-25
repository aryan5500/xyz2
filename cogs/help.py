import discord
import json 
import asyncio
import platform
import random
import os
import sys
import traceback
import collections
import os
import textwrap
import secrets
from io import BytesIO
from discord.ext import commands
from discord.ext.commands import bot

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self,ctx):
        page1 = discord.Embed (colour = discord.Colour.orange()
        )
        page1.add_field(name=f"{ctx.author}",value=f'Prefix For This Server Is **`{ctx.prefix}`**')
        page1.add_field(name=f"•{ctx.prefix}help <Command | Module>",value=f'For More Info.')
        page1.add_field(name=f"🅼🅰🅸🅽",value=f'🔨 **Moderation**\n'
                                f'☯️ **Utiles**\n'
                                f'🎯  **Fun**\n'
                                f'👻  **music**\n', inline=False)
        page1.set_footer(text="Made With 💝 by Mystic07#6829")
        page2 = discord.Embed (
            title = f'{ctx.author}',
            colour = discord.Colour.orange())
        page2.add_field(name="🔨 **🅼🅾🅳🅴🆁🅰🆃🅸🅾🅽 Commands**",value="**`hackban`,   `warn`,   `timemute`,   `banlist`,   `lockdown`,    `massrole`,   `massroleremove`,   `mute`,   `slowmode`,   `ban`,   `unban`,   `mute`,   `unmute`,   `kick`,   `nick`,   `addrole`,   `removerole`,   `mroles`,   `lock`,   `unlock`,   `hide`,   `unhide`,   `close_all`,   `open_all`,   `makerole`,   `delrole`,   `vcmuteall`,   `vcunmuteall`,   `vcmute`,   `vcunmute`,   `vcdeafen`,   `vcundeafen`,   `modsetup`**")
        page2.set_footer(text="📑 Showing Page 1/4")
        page3 = discord.Embed (
            title = f' {ctx.author}',
            colour = discord.Colour.orange()
        )
        page3.add_field(name="☯️  **🆄🆃🅸🅻🅴🆂 Commands**", value="**`membercount`,   `visualembed`,   `invite`,   `poll`,   `userinfo`,   `setprefix`,   `afk`,   `serverinfo`,   `purge`,   `ping`,   `avatar`,   `embed`,   `snipe`,   `move`,   `createvc`,   `deletevc`,   `createchannel`,   `deletechannel`,   `multicreatechannel`,   `multideletechannel`,   `multicreatevc`,   `multideletevc`,   `moveallhere`,   `renamevc`,   `dc`,   `dcall`,   `drag`,   `dropall`,   `kickallvc`,   **")
        page3.set_footer(text="📑 Showing page 2/4")
        page4 = discord.Embed (
            title = f'{ctx.author}',
            colour = discord.Colour.orange()
        )
        page4.add_field(name="🎯 **🅵🆄🅽 Commands**", value="**```Guess```,   `meme`,   ```Say```,   ```Spam```,   ```EightBall```,   ```Combine```,   ```GayScanner```,   ```Ship```,   ```Tictactoe```,   ```Spin```,   ```HotCalc```,   ```Beer```,   ```Password```,   ```Reverse```**")
        page4.set_footer(text="📑 Showing page 3/4")
        page5 = discord.Embed (
            title = f'{ctx.author}',
            colour = discord.Colour.orange()
        )
        page5.add_field(name="👻 **music Commands**", value="**```play```,   `join`,   ```pause```,   ```resume```,   ```now playing```,   ```queue```,   ```disconnect```,   ```Skip```,   ```remove```,   ```clearq```,   ```volume```**")
        page5.set_footer(text="📑 Showing page 4/4")
        
        pages = [page1, page2, page3,page4 ,page5]

        message = await ctx.send(embed = page1)
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')

        def check(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < 4:
                    i += 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                i = 4
                await message.edit(embed = pages[i])
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 15.0, check = check)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()
        
        
       
def setup(bot):
    bot.add_cog(help(bot))
    print("help Cog is Loaded")