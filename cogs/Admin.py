import time
import aiohttp
import discord
import importlib
import os
import sys
import json
import textwrap
import traceback
from datetime import datetime, timedelta
from discord.ext import commands




class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def is_owner(ctx):
        return ctx.author.id == 910939726482141204
    
    @commands.command(aliases= ["devc"])
    @commands.check(is_owner)
    async def devcommands(self,ctx):
        embed=discord.Embed(title="Devs Commands List",color=discord.Color.random())
        embed.add_field(name="**Owner\dev**", value="**```Toggle```, ```Left```, ```ServerList```,  ```Dm```,  ```Find_Owner```, ```GrabInv```,  ```Maintenance```,   `blacklist`,   `log`,   `search`,   `adduser`,   `remuser`,   `_eval`,   load`,   `unload`,   `reload`,   `reloadall`,   `reloadutiles`,   `reboot`,   `change`,   `change_playing`,   `change_username`,   `change_nickname`,   `change_avatar`**")
        await ctx.reply(embed=embed)
    
    @commands.command(aliases=['invgrab', 'makeinv'])
    @commands.check(is_owner)
    async def grabinv(self, ctx, guild: int = None):
        guild = self.bot.get_guild(guild) if guild else ctx.guild
        gchannel = None
        for channel in guild.text_channels:
            if ctx.me.permissions_in(channel).create_instant_invite:
                gchannel = channel
                break
        if not gchannel:
            raise commands.BotMissingPermissions
        invite = await gchannel.create_invite(reason='Invite for logging and testing purposes. Expires in 1 hour.',
                                              max_age=3600)
        await ctx.send('👍')
        dicted = {}
        for i in dir(invite):
            if not str(i).startswith('__') and not str(getattr(invite, i)).startswith('<'):
                dicted[i] = str(getattr(invite, i))
        dicted = json.dumps(dicted, indent=4)
        dicted = str(dicted)
        embed = discord.Embed(
            title=f'Successfully generated invite for {guild.name}',
            description=f'```json\n{dicted}\n```',
            colour=discord.Color.random()
        )
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.author.send(embed=embed)
        sent = await ctx.author.send('Say "del" or "delete" to delete this invite link')

        def check(m):
            return m.author.id == ctx.author.id and type(m.channel) == discord.DMChannel and m.content.lower() in [
                'del', 'delete']

        try:
            await self.bot.wait_for('message', check=check, timeout=3600)
        except asyncio.TimeoutError:
            pass
        else:
            await sent.delete()
            await invite.delete()
            await ctx.author.send('Done!')

    @commands.group(invoke_without_command=True, aliases=['bl'])
    @commands.check(is_owner)
    async def blacklist(self, ctx):
        """Blacklisting commands"""
        pass

    @commands.group(invoke_without_command=True, aliases=['log'])
    @commands.check(is_owner)
    async def logs(self, ctx):
        cat = self.bot.get_command('jishaku cat')
        await ctx.invoke(cat, 'LOG.log')

    @logs.command()
    @commands.check(is_owner)
    async def search(self, ctx, *, search_term):
        _ctx = ctx
        _ctx.message.content = f"{ctx.prefix}jsk sh grep -rn '{search_term}' LOG.log"
        await self.bot.process_commands(_ctx.message)

    @blacklist.command(aliases=['addmember'])
    @commands.check(is_owner)
    async def adduser(self, ctx, member: discord.Member, *, reason: str = 'None Provided'):
        with open('blacklist.json', 'r') as f:
            blacklist = json.load(f)

        blacklist[str(member.id)] = reason.capitalize()
        blacklist[str(member.id)] = reason.capitalize()

        with open('blacklist.json', 'w') as f:
            json.dump(blacklist, f, indent=4)

        await ctx.send('Done.')

        try:
            embed = discord.Embed(title=f'You have been blacklisted from utilising my commands.',
                                  colour=self.bot.colour,
                                  description=f'Reason: `{reason.capitalize()}`')
            await member.send(embed=embed)
            await ctx.send('DM sent successfully.')
        except:
            await ctx.send('DM failed to send.')

    @blacklist.command(aliases=['remmember'])
    @commands.check(is_owner)
    async def remuser(self, ctx, member: discord.Member):
        with open('blacklist.json', 'r') as f:
            blacklist = json.load(f)

        try:
            blacklist.pop(str(member.id))
            blacklist.pop(str(member.id))
        except:
            return await ctx.send('`Member` not found in blacklist.')

        with open('blacklist.json', 'w') as f:
            json.dump(blacklist, f, indent=4)

        await ctx.send('Done.')

        try:
            embed = discord.Embed(
                title=f'You have been unblacklisted from utilising my commands.', colour=self.bot.colour)
            await member.send(embed=embed)
            await ctx.send('DM sent successfully.')
        except:
            await ctx.send('DM failed to send.')

    @commands.command(name='eval')
    @commands.check(is_owner)
    async def _eval(self, ctx, *, code):
        if "import os" in code or "import sys" in code:
            return await ctx.send(f"You Can't Do That!")

        code = code.strip('` ')

        env = {
            'bot': self.bot,
            'BOT': self.bot,
            'client': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.guild,
            'guild': ctx.message.guild,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'print': ctx.send  
        }
        env.update(globals())

        new_forced_async_code = f'async def code():\n{textwrap.indent(code, "    ")}'

        exec(new_forced_async_code, env)
        code = env['code']
        try:
            await code()
        except:
            await ctx.send(f'```{traceback.format_exc()}```')
    
    @commands.command(aliases=["ccount"])
    @commands.check(is_owner)
    async def commandcount(self,ctx):
        counter = 0
        for command in self.bot.commands:
            counter += 1
        await ctx.send(f"There are `{counter}` commands!")
    
        
    @commands.command(aliases=['tm'])
    @commands.check(is_owner)
    async def togglemaintenance(self, ctx):
        """Toggles bot maintenance mode"""
        for c in self.bot.walk_commands():
            if c.name != 'togglemaintenance':
                if not c.enabled:
                    c.enabled = True
                else:
                    c.enabled = False
        print('Maintenance has been toggled.')
        return await ctx.send('Successfully `toggled` maintenance mode.')

    @commands.command()
    @commands.check(is_owner)
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"Loaded extension **{name}.py**")

    @commands.command()
    @commands.check(is_owner)
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"Unloaded extension **{name}.py**")

    @commands.command()
    @commands.check(is_owner)
    async def hmm(self,ctx):
            gelbooru = Gelbooru('&api_key=ca610a787ec9caff38d84e0ac7cca6b90b26e2c08ec449b9c2fdd611dbea025c&user_id=736918', '736918')
            results = await gelbooru.search_posts(tags=['breasts','milf', '1girl', 'nude'],exclude_tags=['loli', 'shota'], page = 1)
            for url in results:
                await ctx.send(url)
                
    
            
    @commands.command()
    @commands.check(is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"Reloaded extension **{name}.py**")

    @commands.command()
    @commands.check(is_owner)
    async def reloadall(self, ctx):
        """ Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    error_collection.append(
                        [file, default.traceback_maker(e, advance=False)]
                    )

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.send("Successfully reloaded all extensions")

    @commands.command()
    @commands.check(is_owner)
    async def reloadutils(self, ctx, name: str):
        """ Reloads a utils module. """
        name_maker = f"utiles/{name}.py"
        try:
            module_name = importlib.import_module(f"utils.{name}")
            importlib.reload(module_name)
        except ModuleNotFoundError:
            return await ctx.send(f"Couldn't find module named **{name_maker}**")
        except Exception as e:
            error = default.traceback_maker(e)
            return await ctx.send(f"Module **{name_maker}** returned error and was not reloaded...\n{error}")
        await ctx.send(f"Reloaded module **{name_maker}**")

    @commands.command()
    @commands.check(is_owner)
    async def reboot(self, ctx):
        """ Reboot the bot """
        await ctx.send("Rebooting now...")
        time.sleep(1)
        sys.exit(0)

    @commands.command()
    @commands.check(is_owner)
    async def dm(self, ctx, user: discord.User, *, message: str):
        """ DM the user of your choice """
        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{user}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")

    @commands.group()
    @commands.check(is_owner)
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @change.command(name="playing")
    @commands.check(is_owner)
    async def change_playing(self, ctx, *, playing: str):
        """ Change playing status. """
        status = self.config["status_type"].lower()
        status_type = {"idle": discord.Status.idle, "dnd": discord.Status.dnd}

        activity = self.config["activity_type"].lower()
        activity_type = {"listening": 2, "watching": 3, "competing": 5}

        try:
            await self.bot.change_presence(
                activity=discord.Game(
                    type=activity_type.get(activity, 0), name=playing
                ),
                status=status_type.get(status, discord.Status.online)
            )
            self.change_config_value("playing", playing)
            await ctx.send(f"Successfully changed playing status to **{playing}**")
        except discord.InvalidArgument as err:
            await ctx.send(err)
        except Exception as e:
            await ctx.send(e)

    @change.command(name="username")
    @commands.check(is_owner)
    async def change_username(self, ctx, *, name: str):
        """ Change username. """
        try:
            await self.bot.user.edit(username=name)
            await ctx.send(f"Successfully changed username to **{name}**")
        except discord.HTTPException as err:
            await ctx.send(err)

    @change.command(name="nickname")
    @commands.check(is_owner)
    async def change_nickname(self, ctx, *, name: str = None):
        """ Change nickname. """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"Successfully changed nickname to **{name}**")
            else:
                await ctx.send("Successfully removed nickname")
        except Exception as err:
            await ctx.send(err)

    @change.command(name="avatar")
    @commands.check(is_owner)
    async def change_avatar(self, ctx, url: str = None):
        """ Change avatar. """
        if url is None and len(ctx.message.attachments) == 1:
            url = ctx.message.attachments[0].url
        else:
            url = url.strip("<>") if url else None

        try:
            bio = await http.get(url, res_method="read")
            await self.bot.user.edit(avatar=bio)
            await ctx.send(f"Successfully changed the avatar. Currently using:\n{url}")
        except aiohttp.InvalidURL:
            await ctx.send("The URL is invalid...")
        except discord.InvalidArgument:
            await ctx.send("This URL does not contain a useable image")
        except discord.HTTPException as err:
            await ctx.send(err)
        except TypeError:
            await ctx.send("You need to either provide an image URL or upload one with the command")
    
    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def find_owner(self,ctx):
        guild_owner = self.bot.get_user(int(ctx.guild.owner.id))
        await ctx.send(f'The owner of this server is: {guild_owner}')
    
    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def serverlist(self,ctx):
        activeservers = self.bot.guilds
        for guild in activeservers:
            embed = discord.Embed(title=str("⚡ Bot  Servers List"),color=discord.Color(value=0xc904e2))
            embed.add_field(name="Guilds Name",value=f'{guild.name}', inline=True)
            embed.add_field(name="Guilds Id",value=f'{guild.id}', inline=True)
            embed.add_field(name="Owners Name",value=f'{guild.owner}', inline=True)
            embed.add_field(name="Owners Id",value=f'{guild.owner.id}', inline=True)
            embed.add_field(name="Created At",value=f'{guild.created_at}', inline=True)
            embed.add_field(name="Server Count",value=f"I'm in {len(self.bot.guilds):,d} guilds", inline=True)
            await ctx.send(embed=embed)
    
    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def left(self,ctx,*, guild_id):
        await self.bot.get_guild(int(guild_id)).leave()
        await ctx.send(f"I left: {guild_id}")
    
    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def dm(self,ctx, user: discord.User, *, message: str):
            try:
                await user.send(message)
                await ctx.send(f"✉️ Sent a DM to **{user}**")
            except discord.Forbidden:
                await ctx.send("This user might be having DMs blocked or it's a bot account...")
    
    @commands.command()
    @commands.guild_only()
    async def mods(self,ctx):
            message = ""
            all_status = {
                "online": {"users": [], "emoji": "🟢"},
                "idle": {"users": [], "emoji": "🟡"},
                "dnd": {"users": [], "emoji": "🔴"},
                "offline": {"users": [], "emoji": "⚫"}
            }

            for user in ctx.guild.members:
                user_perm = ctx.channel.permissions_for(user)
                if user_perm.kick_members or user_perm.ban_members:
                    if not user.bot:
                        all_status[str(user.status)]["users"].append(f"**{user}**")

            for g in all_status:
                if all_status[g]["users"]:
                    message += f"{all_status[g]['emoji']} {', '.join(all_status[g]['users'])}\n"
                    embed=discord.Embed(title="Thinking",color=0x9C84EF)
                    embed.add_field(name=f"**Checking Mods Of {ctx.guild.name}**",value=f"{message}")
                    await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Admin(bot))
    print("Admin Cog is Loaded")