import discord
import json 
import asyncio
import time
import datetime
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
from ago import human
from pygelbooru import Gelbooru
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import bot

class utiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self,ctx,*, prefix):
        
        with open(r"prefixes.json","r") as f:
            prefixes = json.load(f)
        
        prefixes[str(ctx.guild.id)] = prefix
        
        with open(r"prefixes.json","w") as f:
            json.dump(prefixes, f, indent=4)
        
        await ctx.send(f"{prefix} is the new guild prefix ")
    
    @commands.command()
    async def afk(self, ctx, *, reason: str = 'None Provided'):
        """Sets or removes an outstanding AFK"""
        with open('afks.json', 'r') as f:
            afks = json.load(f)

        try:
            if afks[str(ctx.author.id)]:
                afks.pop(str(ctx.author.id))
                with open('afks.json', 'w') as f:
                    json.dump(afks, f, indent=4)
                return await ctx.send(f'{ctx.author.mention}, I removed your AFK.')
        except KeyError:
            pass

        finaltime = str(ctx.message.created_at).split(
            ' ')[1].replace(':', '').replace('.', '')
        afks[str(ctx.author.id)] = {"message": reason, "time": finaltime}
        await ctx.send(f'{ctx.author.mention}, I successfully marked you as AFK.')
        await asyncio.sleep(1)
        with open('afks.json', 'w') as f:
            json.dump(afks, f, indent=4)
    
    @commands.command(aliases=['si'], description='To get the server information.')
    @commands.guild_only()
    async def serverinfo(self, ctx):


        if ctx.channel.id ==757108786497585172:
            return

        guild= ctx.guild
        emojis = str(len(guild.emojis))

        channels = str(len(guild.channels))
        roles= str(len(guild.roles))
        time= ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p ")
        voice= str(len(guild.voice_channels))
        text= str(len(guild.text_channels))
        statuses = collections.Counter([member.status for member in guild.members])

        online = statuses[discord.Status.online]
        idel = statuses[discord.Status.idle]
        dnd = statuses[discord.Status.dnd]
        offline= statuses[discord.Status.offline]

        embed= discord.Embed(
                                timestamp= ctx.message.created_at, color=discord.Color.random())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=f"Information for  {ctx.guild.name}")
        embed.add_field(name="__General information__\n", value= f'**Server name : ** {guild.name}\n'
                                                               f'**Server region : ** {guild.region}\n'
                                                               f'**Server ID : ** {guild.id}\n'
                                                               f'**Created at : ** {time}\n'
                                                               f'**Verification level : ** {guild.verification_level} \n'
                                                               f'**Server owner : ** {ctx.guild.owner} \n'
                                                               , inline=False)


        embed.add_field(name="\n\n\n__Statistics__", value= f'**Member count : ** {ctx.guild.member_count}\n'
                                                 f'**Role count : ** {roles} \n'
                                                 f'**Channel count : ** {channels}\n'
                                                 f'**Text channels :** {text}\n'
                                                 f'**Voice channels :** {voice}\n'
                                                 f'**Emoji count : ** {emojis}\n'
                                                 f'**Server boosts : ** {guild.premium_subscription_count}\n')

        embed.add_field(name="__Activity__", value= f'Online : {online}\n'
                                                    f'Idle : {idel}\n'
                                                    f'DND : {dnd}\n'
                                                    f'offline : {offline}')


        embed.set_footer(text=f"Requested by {ctx.author}",  icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["clean", "clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, limit: int = None):
            if limit is not None:
                await ctx.channel.purge(limit=limit + 1)

                await ctx.send(embed=discord.Embed(
                        title="🧹 Purge",
                        description=f"{ctx.author.mention} has deleted {limit} messages from {ctx.channel.mention}",
                        color=discord.Color.random()
                    )
                    )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            "🚫 You need to define the amount"
                            " to delete messages too! Make sure the amount is numerical."
                        ),
                        color=discord.Color.random()
                    ).add_field(
                        name="Format",
                        value=f"`{prefix}purge <amount>`"
                    )
                )

    @purge.error
    async def purge_error(self,ctx, error):
            if isinstance(error, commands.CommandInvokeError):
                await ctx.send(
                    embed=discord.Embed(
                        title="Permission error",
                        description="🚫 I don't have permissions to delete messages",
                        color=discord.Color.random()
                    )
                )

    
    @commands.command()
    async def ping(self,ctx):
        msg = await ctx.send("`Pinging bot latency...`")
        times = []
        counter = 0
        embed = discord.Embed(title="More information:", description="Pinged 4 times and calculated the average.", color=0x9208ea)
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Pinging... {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)

        embed.set_author(name="Pong!")
        embed.add_field(name="Bot latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Average speed", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)
    
    @commands.command(aliases= ["av"])
    @commands.guild_only()
    async def avatar(self,ctx, *,  avamember : discord.Member=None):
        if avamember==None:
            avamember= ctx.author
        userAvatarUrl = avamember.avatar_url
        embed = discord.Embed(title = f"{avamember.name}'s Avatar", color = avamember.color, timestamp= ctx.message.created_at,description = f'[PNG]({avamember.avatar_url_as(format="png")}) | [JPEG]({avamember.avatar_url_as(format="jpeg")}) | [WEBP]({avamember.avatar_url_as(format="webp")})')
        embed.set_image(url=str(avamember.avatar_url))
        embed.set_footer(text= f"Requested by : {ctx.author}")
        await ctx.send(embed=embed)
    
  

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embed(self,ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('Waiting for a title')
        title = await self.bot.wait_for('message', check=check)
    
        await ctx.send('Waiting for a description')
        desc = await self.bot.wait_for('message', check=check)
        
        embed = discord.Embed(title=title.content, description=desc.content,  color=0x72d345)
        
        await ctx.send(embed=embed)
    
    snipe_message_author = {}
    snipe_message_content = {}
    
    @commands.command(name = 'snipe')
    @commands.has_permissions(manage_messages=True)
    async def snipe(self,ctx):
        channel = ctx.message.author.channel
        try: 
            em = discord.Embed(name = f"Last deleted message in #{ctx.channel.name}", description = snipe_message_content[channel.id],color=0x9208ea)
            em.set_footer(text = f"This message was sent by {snipe_message_author[ctx.channel.id]}")
            await ctx.send(embed = em)
        except: 
            await ctx.send(f"There are no recently deleted messages in #{channel.name}")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def move(self,ctx,member: discord.Member):
        await member.edit(voice_channel=ctx.message.author.voice.channel)
        await ctx.reply("Done!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def createvc(self,ctx, channelname):
        guild = ctx.guild
        embed=discord.Embed(title="Success",description=f"```{channelname}``` has been successfully created ",color=discord.Color.random())
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False)
        }
        await guild.create_voice_channel(name=channelname,overwrites=overwrites)
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def deletevc(self,ctx, vc: discord.VoiceChannel):
        embed=discord.Embed(title="Success",description=f"```{vc}``` has been successfully deleted ",color=discord.Color.random())
        await vc.delete()
        await ctx.reply(embed=embed)
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self,ctx, channelname):
        guild = ctx.guild
        embed=discord.Embed(title="Success",description=f"```{channelname}``` has been successfully created ",color=discord.Color.random())
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        await guild.create_text_channel(name=channelname,overwrites=overwrites)
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self,ctx, channel: discord.TextChannel):
        embed=discord.Embed(title="Success",description=f"```{channel}``` has been successfully deleted ",color=discord.Color.random())
        await channel.delete()
        await ctx.reply(embed=embed)

    @commands.command(aliases= ["mcvc"])
    @commands.has_permissions(manage_channels=True)
    async def multicreatevc(self,ctx,* names):
        guild = ctx.guild
        for name in names:
            embed=discord.Embed(title="Success",description=f"```{name}``` has been successfully created ",color=discord.Color.random())
            overwrites = {
            guild.default_role: discord.PermissionOverwrite(connecy=False)
        }
            await guild.create_voice_channel(name,overwries=overwrites)
            await ctx.reply(embed=embed)

    @commands.command(aliases= ["mdvc"])
    @commands.has_permissions(manage_channels=True)
    async def multideletevc(self,ctx,* voicechannels: discord.VoiceChannel):
            for vc in voicechannels:
                embed=discord.Embed(title="Success",description=f"```{vc.name}``` has been successfully deleted ",color=discord.Color.random())
                await vc.delete()
                await ctx.reply(embed=embed)
        
    @commands.command(aliases= ["mctc"])
    @commands.has_permissions(manage_channels=True)
    async def multicreatechannel(self,ctx,* names):
        guild = ctx.guild
        for name in names:
            embed=discord.Embed(title="Success",description=f"```{name}``` has been successfully created ",color=discord.Color.random())
            overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
            await guild.create_text_channel(name,overwrites=overwrites)
            await ctx.reply(embed=embed)

    @commands.command(aliases= ["mdc"])
    @commands.has_permissions(manage_channels=True)
    async def multideletechannel(self,ctx,*channels: discord.TextChannel):
        for ch in channels:
            embed=discord.Embed(title="Success",description=f"```{ch.name}``` has been successfully deleted ",color=discord.Color.random())
            await ch.delete()
            await ctx.reply(embed=embed)
    
    @commands.command(aliases=["mah"])
    @commands.has_permissions(manage_messages=True)
    async def moveallhere(self,ctx):
            server = ctx.guild
            author = ctx.author
            all_members = server.members

            if author.voice:
                move_channel = author.voice.channel
            else:
                await ctx.send(f"You have to be in a Voice Channel to use this command, {ctx.author.mention}")
                return
            for member in all_members:
                if(member.voice and not member.voice.afk and member != author):
                     await ctx.reply(f"Mass moved everyone to `{str(move_channel)}`")
                     await member.move_to(move_channel)
           
            await ctx.message.delete()
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def renamevc(self,ctx, channel: discord.VoiceChannel, *, new_name):
        await channel.edit(name=new_name)
        await ctx.reply(f"Successfully Changed  Voice channel name  ` {new_name}`")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def renametc(self,ctx, channel: discord.TextChannel, *, new_name):
        await channel.edit(name=new_name)
        await ctx.reply(f"Successfully Changed  text channel name  ` {new_name}`")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def dc(self,ctx,member: discord.Member):
        await member.move_to(None)
        await ctx.reply("Done!")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def dcall(self,ctx):
        for members in ctx.author.voice.channel.members:
            await ctx.reply("Done")
            await members.move_to(None)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def drag(self,ctx, *, channel : discord.VoiceChannel):
        for members in ctx.author.voice.channel.members:
            await ctx.reply("Done")
            await members.move_to(channel)
            
    @drag.error
    async def drag_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that!")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def dropall(self,ctx, *, channel : discord.VoiceChannel):
        for members in ctx.author.voice.channel.members:
            await ctx.reply("Done")
            await members.move_to(None)
            
        

    @dropall.error
    async def dropall_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kickallvc(self,ctx):
        if ctx.author.voice: 
            canale = ctx.message.author.voice.channel
            utenti = canale.members
            for utente in utenti:
                await utente.edit(voice_channel = None)
            await ctx.send("Kicked all the members from the voice channel!")
        else:
            await ctx.send("You need to be in a voice channel!")
            return

    @kickallvc.error
    async def kickallvc_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that!")
    
    format = "%a, %d %b %Y | %H:%M:%S %ZGMT"


    @commands.command(aliases=['whois', 'ui'], description='To see information of a user.')
    @commands.guild_only()
    async def userinfo(self,ctx, member: discord.Member=None):

        member = member or ctx.author
        a = 0
        if a == 0:

            uroles = []
            for role in member.roles[1:]:
                if role.is_default():
                    continue
                uroles.append(role.mention)

                uroles.reverse()
            timestamp = 'ㅤ'
            time = member.created_at
            time1= member.joined_at
            if member.status == discord.Status.online:
                status= '<:online:769826555073003521>'
            elif member.status == discord.Status.idle:
                status= '<:idle:769826555479588864>'
            elif member.status== discord.Status.dnd:
                status = '<:dnd:769826555865989153>'
            else:
                status = '<:offline:769826555643691041>'
            if member.activity == None:
                activity = 'None'
            else:
                activity = member.activities[-1].name
                try:
                    timestamp = member.activities[0].details
                except:
                    timestamp ='ㅤ'
            embed=discord.Embed(color=discord.Color.random(), timestamp=ctx.message.created_at, type="rich")
            embed.set_thumbnail(url= f"{member.avatar_url}")
            embed.set_author(name=f"{ctx.author.name}'s information",icon_url=f'{ctx.me.avatar_url}')
            embed.add_field(name="__General information__",value=f'**Nickname :** {member.display_name}\n'
                                                            f'**ID :** {member.id}\n'
                                                            f'**Account created :** {human(time, 4)}\n'
                                                            f'**Server joined :** {human(time1, 3)}\n'
                                                            ,inline=False)
            embed.add_field(name="__Role info__", value= f'**Highest role :** {member.top_role.mention}\n'
                                                        f'**Color** : {member.color}\n'
                                                        f'**Role(s) :** {", ".join(uroles)}\n'
                                               , inline=False)

            embed.add_field(name="__Presence__", value =f'**Status : ** {status}\n'
                                                        f'**Activity : ** {activity}  \nㅤㅤㅤㅤ{timestamp}')
            embed.set_footer(text=f"Requested by {ctx.author.name}",  icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def poll(self,ctx, *, pollInfo):
            emb = (discord.Embed(description=pollInfo, color=0x9C84EF))
            emb.set_author(name=f"Poll by {ctx.message.author}", icon_url="https://lh3.googleusercontent.com/7ITYJK1YP86NRQqnWEATFWdvcGZ6qmPauJqIEEN7Cw48DZk9ghmEz_bJR2ccRw8aWQA=w300")
            try:
                await ctx.message.delete()
            except discord.Forbidden:
                pass
            try:
                pollMessage = await ctx.send(embed=emb)
                await pollMessage.add_reaction("\N{THUMBS UP SIGN}")
                await pollMessage.add_reaction("\N{THUMBS DOWN SIGN}")
            except Exception as e:
                await ctx.send(f"Oops, I couldn't react to the poll. Check that I have permission to add reactions! ```py\n{e}```")
    
    @commands.command()
    async def invite(self,ctx):
            try:
                await ctx.author.send("**https://discord.com/api/oauth2/authorize?client_id=920659567736680509&permissions=8&scope=bot**\n*Here's my invite link!*")
                helpMsg = await ctx.send("**I sent my invite link in your DMs :mailbox_with_mail:**")
            except Exception:
                helpMsg = await ctx.send(f"**{ctx.author.mention} https://discord.com/api/oauth2/authorize?client_id=920659567736680509&permissions=8&scope=bot**\n*Here's my invite link!*")
            await helpMsg.add_reaction("a:SpectrumOkSpin:4664808980498350")
    
    @commands.command(aliases=['embedder'])
    @commands.has_permissions(manage_messages=True)
    async def Visualembed(self,ctx):
            displayable = 'https://embed.rauf.wtf/'

            def check(m):
                return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

            try:
                a = await ctx.send(
                    'Alright, send me the embed title text. Note: this is a required argument. PS: Try avoiding using characters other than a-Z and 0-9 since this can cause errors.')
                msg = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send("You didn't reply in 30 seconds, so the request timed out.")
            else:
                displayable += f"{msg.content.replace(' ', '+')}?"
                try:
                    await msg.delete()
                    await a.delete()
                except discord.Forbidden:
                    pass
            b = await ctx.send(
                'Alright, recorded your embed title. Next, send me the author of the embed. Say "None" to leave this field blank. PS: Try avoiding using characters other than a-Z and 0-9 since this can cause errors.')

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send("You didn't reply in 30 seconds, so the request timed out.")
            else:
                if not msg.content.lower() == 'none':
                    displayable += f"&author={msg.content.replace(' ', '+')}"
                try:
                    await msg.delete()
                    await b.delete()
                except discord.Forbidden:
                    pass
            c = await ctx.send(
                'Alright, next I need the colour of your embed in hex form. This will default to black. Say "None" to leave this field blank.')

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send("You didn't reply in 30 seconds, so the request timed out.")
            else:
                if not msg.content.lower() == 'none':
                    displayable += f"&color={msg.content.replace(' ', '+').replace('#', '')}"
                try:
                    await msg.delete()
                    await c.delete()
                except discord.Forbidden:
                    pass
            d = await ctx.send(
                'Alright, next I need the image URL of the embed that will be displayed below the title. Say "None" to leave this field blank.')

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send("You didn't reply in 30 seconds, so the request timed out.")
            else:
                if not msg.content.lower() == 'none':
                    displayable += f"&image={msg.content.replace(' ', '+')}"
                try:
                    await msg.delete()
                    await d.delete()
                except discord.Forbidden:
                    pass
            e = await ctx.send(
                'Alright, finally I need the redirect URL of the embed, the website users will go to when they click the link. Say "None" to leave this field blank.')

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send("You didn't reply in 30 seconds, so the request timed out.")
            else:
                if not msg.content.lower() == 'none':
                    displayable += f"&url={msg.content.replace(' ', '+')}"
                try:
                    await msg.delete()
                    await e.delete()
                except discord.Forbidden:
                    pass
                await ctx.send(
                    f'Alright, I have all I need. To send this embed anywhere, copy this link and paste it wherever you want.\n\n```fix\n{displayable}\n```\n\nHere is a visual representation of your embed:')
            return await ctx.send(displayable)
    
    @commands.command(aliases=["membercount", "count", "mcount"])
    async def members(self,ctx):
            embed = discord.Embed(colour=discord.Colour.orange(),timestamp = ctx.message.created_at)

            embed.set_author(name="Member Count", icon_url=ctx.guild.icon_url)
            embed.add_field(name="Current Member Count:", value=ctx.guild.member_count)
            embed.set_footer(text=ctx.guild, icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)
    
    bot.launch_time = datetime.utcnow()
    
    @commands.command(aliases=["about", "info"])
    async def botinfo(self,ctx):
        delta_uptime = datetime.utcnow() - bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        counts = (
                        f"I'm in {len(self.bot.guilds):,d} guilds",
                        f'Seeing {len(set(self.bot.get_all_channels())):,d} channels',
                        f'Listening to {len(set(self.bot.get_all_members())):,d} users')
        embed = discord.Embed(title=str("⚡ Bot Info"),description="Get Some Usefull (or not) Information About The Bot", color=discord.Color(value=0xc904e2))
        embed.add_field(name="Owner:",value=f"**<@910939726482141204>**", inline=True)
        embed.add_field(name="Python Version:",value=f"Python version: {platform.python_version()}", inline=True)
        embed.add_field(name="Discord Api Version:",value=f"discord API version: {discord.__version__}", inline=True)
        embed.add_field(name="Counts", value="\n".join(counts))
        embed.add_field(name="Running On:",value=f"{platform.system()} {platform.release()} ({os.name})", inline=True)
        embed.add_field(name="Prefix: ",value=f"{ctx.prefix}",inline=False)
        embed.add_field(name="Uptime",value=f"{days}d: {hours}h: {minutes}m",inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)
                
def setup(bot):
    bot.add_cog(utiles(bot))
    print("utiles Cog is Loaded")