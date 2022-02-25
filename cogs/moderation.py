import discord
import json 
import asyncio
import time
import datetime
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import cooldown, BucketType

class moderation(commands.Cog):
    def __init__(self,bot):
          self.bot = bot
    
    @commands.command(aliases=['hban'])
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 15, BucketType.user)
    async def hackban(self,ctx, user: discord.User):
        if user in ctx.guild.members:
            embed = discord.Embed(description=f"Unsuccessful, the user is in this guild. [-help ban]", color=discord.Color.orange())
            await ctx.reply(embed=embed, mention_author=False)

        else:
            await ctx.guild.ban(user)
            embed = discord.Embed(title=f"Successfully hack banned {user.name}", color=discord.Color.orange())
            await ctx.reply(embed=embed, mention_author=False)
   
        
    @commands.command(
        name='warn',
        description="Warns a user in the server.",
    )
    @commands.has_permissions(manage_messages=True)
    async def warn(self,ctx, member: discord.Member, *, reason: str = "Not specified"):
            embed = discord.Embed(
                title="User Warned!",
                description=f"**{member}** was warned by **{ctx.author}**!",
                color=0x9C84EF
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await ctx.send(embed=embed)
            try:
                await member.send(f"You were warned by **{ctx.author}**!\nReason: {reason}")
            except discord.Forbidden:
                await ctx.send(f"{member.mention}, you were warned by **{ctx.author}**!\nReason: {reason}")
    
    @commands.command(aliases= ["timemute"])
    @commands.has_permissions(manage_messages=True)
    async def tmute(self,ctx, member: discord.Member,time,*,reason=None):
        guild = ctx.guild
        muted_role=discord.utils.get(ctx.guild.roles, name="Muted")
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        tempmute= int(time[0]) * time_convert[time[-1]]
        await ctx.message.delete()
        await member.add_roles(muted_role)
        embed = discord.Embed(title="muted", description=f"{member.mention} was muted  ", colour=discord.Colour.light_gray())
        embed.add_field(name="reason:", value=reason, inline=False)
        embed.add_field(name="Time",value=f"{time} ")
        embed.set_footer(text= f"Muted by : {ctx.author}")
        await ctx.send(embed=embed, delete_after=5)
        await member.send(f" you have been muted from: {guild.name} | reason: {reason} | Time {time}")
        await asyncio.sleep(tempmute)
        await member.remove_roles(muted_role)
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def banlist(self,ctx):
        bans = await ctx.guild.bans()
        loop = [f"{u[1]} ({u[1].id})" for u in bans]
        _list = "\r\n".join([f"[{str(num).zfill(2)}] {data}" for num, data in enumerate(loop, start=1)])
        embed=discord.Embed(title="Ban List",description=f"```ini\n{_list}```", color=discord.Color.random())
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

       
    @commands.command(name="massrole")
    @commands.has_permissions(manage_roles=True)
    async def mass_role(
        self, ctx, role: discord.Role = None, role2: discord.Role = None
    ):
        if role is not None and role2 is not None:
            bot_msg = await ctx.send(
                embed=discord.Embed(
                    title="Confirmation",
                    description=(
                        f"Are you sure you want to update all members"
                        f" with the role {role.mention} with {role2.mention}?"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name=(
                        "Note that this action is irreversible "
                        "and cannot be stopped once started"
                    ),
                    value=(
                        f"⬅️ to accept\n"
                        f"🔄to accept with live stats\n"
                        f"➡️ to decline\n"
                    )
                        
                )
            )

            await bot_msg.add_reaction("⬅️")
            await bot_msg.add_reaction("🔄")
            await bot_msg.add_reaction("➡️")

            def reaction_check(r, u):
                return u == ctx.author and r.message == bot_msg

            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=reaction_check
            )

            updates = False

            try:
                await bot_msg.clear_reactions()
            except Exception:
                pass

            if str(reaction.emoji) == "➡":
                return await ctx.send("Cancelled mass role update")

            if str(reaction.emoji) == "🔄":
                updates = True

            if (
                str(reaction.emoji) == "🔄"
                or str(reaction.emoji) == "⬅️"
            ):

                count = 0

                for member in [
                    member
                    for member in ctx.guild.members
                    if role in member.roles
                ]:
                    try:
                        await member.add_roles(role2)
                        count += 1

                        if updates:
                            await ctx.send(f"{member} updated")

                    except discord.Forbidden:
                        await ctx.send(
                            embed=discord.Embed(
                                description=(
                                    f"Error giving role to {member.mention}"
                                ),
                                color=discord.Color.random()
                            )
                        )

                    await asyncio.sleep(1)

                await ctx.send(
                    f"Done, updated **{count}** members "
                    f"with the {role2.name} role"
                )

        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description=(
                        "You need to define both Role 1 and Role 2\n`role1` "
                        "are the members having that role and `role2` is the"
                        " one to be given to them"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=f"```{ctx.prefix}massrole <role1> <role2>```"
                ).set_footer(
                    text="For role, either ping or ID can be used"
                )
            )
            
    @commands.command(name="massroleremove")
    @commands.has_permissions(manage_roles=True)
    async def mass_role_remove(
        self, ctx, role: discord.Role = None, role2: discord.Role = None
    ):
        if role is not None and role2 is not None:
            bot_msg = await ctx.send(
                embed=discord.Embed(
                    title="Confirmation",
                    description=(
                        f"Are you sure you want to update"
                        f" all members with the role {role.mention}"
                        f" by removing {role2.mention}?"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name=(
                        "Note that this action is irreversable"
                        " and cannot be stopped once started"
                    ),
                    value=(
                        f"⬅️ to accept\n🔄"
                        f" to accept with live stats\n➡️to decline"
                    )
                )
            )

            await bot_msg.add_reaction("⬅️")
            await bot_msg.add_reaction("🔄")
            await bot_msg.add_reaction("➡️")

            def reaction_check(r, u):
                return u == ctx.author and r.message == bot_msg

            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=reaction_check
            )

            updates = False

            try:
                await bot_msg.clear_reactions()

            except Exception:
                pass

            if str(reaction.emoji) =="➡":
                return await ctx.send("Cancelled mass role update")

            if str(reaction.emoji) == "🔄":
                updates = True

            if str(reaction.emoji) == "🔄" or str(
                    reaction.emoji) == "⬅️":
                count = 0
                for member in [
                    member
                    for member in ctx.guild.members
                    if role in member.roles
                ]:
                    try:
                        await member.remove_roles(role2)
                        count += 1
                        if updates:
                            await ctx.send(f"{member} updated")

                    except discord.Forbidden:
                        await ctx.send(
                            embed=discord.Embed(
                                description=(
                                    f"Error giving role to {member.mention}"
                                ),
                                color=discord.Color.random()
                            )
                        )
                    await asyncio.sleep(1)

                await ctx.send(
                    f"Done,"
                    f" updated **{count}** members with the {role2.name} role"
                )
        else:

            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description=(
                        "You need to define both Role 1 and Role 2\n"
                        "`role1` are the members having that role"
                        " and `role2` is the one to be removed from them"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=(
                        f"```{ctx.prefix}massroleremove"
                        f" <role1> <role2>```"
                    )
                ).set_footer(
                    text="For role, either ping or ID can be used"
                )
            )    
    
    @commands.command(description="Mutes the specified user.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self,ctx, member: discord.Member, *, reason=None):
                    if (not ctx.author.guild_permissions.manage_messages):
                        await ctx.reply("This Command Requires ``Manage_Message`` Permission")
                        return
                    guild = ctx.guild
                    mutedRole = discord.utils.get(guild.roles, name="Muted")
                    if not mutedRole:
                        await ctx.reply("No MuteRole Has Been Found. Creating MuteRole...")
                        mutedRole = await guild.create_role(name="Muted")
                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                            embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
                            embed.add_field(name="reason:", value=reason, inline=False)
                            await ctx.send(embed=embed)
                            await member.add_roles(mutedRole, reason=reason)
                            await member.send(f" you have been muted from: {guild.name} | reason: {reason}")
			
    
    
    @commands.command()
    async def slowmode(self,ctx, time:int):
        if (not ctx.author.guild_permissions.manage_messages):
                await ctx.send("This Command Requires ``Manage Messages`` Permissions")
                await ctx.channel.edit(slowmode_delay=0)
        try:
                if time == 0:
                    await ctx.send("Slowmode Off")
                    await ctx.channel.edit(slowmode_delay=0)
                elif time > 21600:
                    await ctx.send("You Can Not Set The Slowmode Above 6 Hours")
                    return
                else:
                    await ctx.channel.edit(slowmode_delay= time)
                    await ctx.reply(f"Slowmode Set To {time} seconds!")
        except Exception:
                await print("Oops!")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(
            self, ctx, user: discord.User = None, *, reason="No reason given"
    ):
        if user is not None and user != ctx.author:

            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Applied ban to `{user}` :ok_hand:")

            try:
                await user.send(
                    embed=discord.Embed(
                        title=f"You have been banned from {ctx.guild.name}",
                        description=(
                            "Sorry I'm just a bot and I follow orders :("
                        ),
                        color=discord.Color.random()
                    ).add_field(
                        name="Reason",
                        value=reason
                    ).add_field(
                        name="Banned by", value=ctx.author
                    )
                )

            except: 
                ctx.send("Failed to send dm")
            return
            await channel.send(embed=discord.Embed(title="🔨 Ban",description=f"{user.mention} has been banned by {ctx.author.mentio}",color=discord.Color.random()).add_field(name="Reason",value=reason))



        elif user == ctx.author:
            await ctx.send("You can't ban yourself :eyes:")

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the user to ban them,"
                        " reason is optional"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=f"`{ctx.prefix}ban <user> <reason>`"
                ).set_footer(
                    text="For user either User mention or User ID can be used")
                )

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to ban the user, "
                        "make sure that my I have ban members permission"
                        " and role is placed above the highest role which"
                        " the user has"
                    ),
                    color=discord.Color.random()
                )
            )
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User = None):
        if user is not None:
            bans = await ctx.guild.bans()
            banned_users = [ban.user for ban in bans]

            if user in banned_users:
                await ctx.guild.unban(user)
                await ctx.send(f'Successfully unbanned `{user}` :ok_hand:')

                try:
                    await user.send(
                        embed=discord.Embed(
                            title=(
                                f"You have been unbanned from {ctx.guild.name}!"
                            ),
                            description="Yay I would be happy to see you back!",
                            color=discord.Color.random()
                        ).add_field(
                            name="Unbanned by", value=ctx.author)
                        )

                except: 
                    ctx.send("Failed to send dm")
                    return
                
            
                
                await channel.send(embed=discord.Embed(
                    title="🔨 Unban",
                    description=f"{user.mention} has been unbanned by {ctx.author.mention}",
                    color=discord.Color.random()
                )
                )

            else:
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"The user `{user}` is not banned, "
                            "therefore cannot unban them."
                        ),
                        color=discord.Color.random()
                    )
                )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description="🚫 You need to define the user to unban them",
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=f"`{ctx.prefix}unban <user>`"
                ).set_footer(
                    text="For user either User mention or User ID can be used")
                )

    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to unban the user, make "
                        "sure that I have ban members permission and my role "
                        "is placed above the highest role which the user has"
                    ),
                    color=discord.Color.random()
                )
            )
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None):
        if member is not None:
            if not discord.utils.get(ctx.guild.roles, name='Muted'):
                muted_role = await ctx.guild.create_role(
                    name="Muted", colour=discord.Colour(0xa8a8a8)
                )

                for i in ctx.guild.text_channels:
                    await i.set_permissions(muted_role, send_messages=False)

            else:
                muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

            await member.add_roles(muted_role)
            await ctx.send(f"Applied chat mute to `{member}` :mute:")

            
                
            
        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define member in order to mute them"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=f"`{ctx.prefix}mute <member>`"
                ).set_footer(
                    text=(
                        "For user either Member mention "
                        "or Member ID can be used"
                    )
                )
            )

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to mute the member, make"
                        " sure that I have manage roles permission and my role"
                        " is placed above the highest role which the member has"
                    ),
                    color=discord.Color.random()
                )
            )
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the member to unmute them"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=f"`{ctx.prefix}unmute <member>`"
                ).set_footer(
                    text=(
                        "For user either Member mention "
                        "or Member ID can be used"
                    )
                )
            )
        elif not discord.utils.get(ctx.guild.roles, name='Muted'):
            await ctx.send(
                "There is no muted role yet hence I cannot unmute, "
                "Muting someone automatically makes one."
            )

        else:
            muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

            await member.remove_roles(muted_role)
            await ctx.send(f"Unmuted `{member}` :sound:")

            
                
            

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to unmute the user, "
                        "make sure that I have manage roles permission and "
                        "my role is placed above the highest role which the "
                        "user has"
                    ),
                    color=discord.Color.random()
                )
            )
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, ctx, member: discord.Member = None, *, reason="No reason provided"
    ):
        if member is not None and member != ctx.author:
            await member.kick(reason=reason)
            await ctx.send(f"`{member}` have been kicked from the server")
        

            try:
                await member.send(
                    embed=discord.Embed(
                        title=f"You have been kicked from {ctx.guild.name}",
                        color=discord.Color.random()
                    ).add_field(
                        name="Reason", value=reason
                    ).add_field(
                        name="Kicked by", value=ctx.author
                    )
                )

            except:
                ctx.send("Failed to send dm")
                return

            
                
        elif member == ctx.author:
            await ctx.send("You can't kick yourself :eyes:")

        else:
            await ctx.send(embed=discord.Embed(
                description="🚫 You need to define the member to kick them",
                color=discord.Color.random()
            ).add_field(
                name="Format",
                value=f"`{ctx.prefix}kick <member>`"
            ).set_footer(
                text="For user either Member mention or Member ID can be used")
            )

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to kick the member,"
                        " make sure that I have kick members permission"
                        " and my role is placed above the highest role "
                        "which the member has"
                    ),
                    color=discord.Color.random()
                )
            )
    
    @commands.command(aliases=["nickname", "changenick"])
    @commands.has_permissions(change_nickname=True)
    async def nick(self, ctx, member: discord.Member = None, *, nick=None):
        if member and nick is not None:
            previous_nick = member.nick
            await member.edit(nick=nick)
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        f"✔️ Nickname changed "
                        f"for `{member}` to {nick}"
                    ),
                    color=discord.Color.random()
                )
            )
            
                
        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define both the member"
                        " and their new nick"
                    ),
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=f"`{ctx.prefix}nick <member> <new nick>`"
                ).set_footer(
                    text="For Member either mention or Member ID can be used"
                )
            )

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to change the nickname "
                        "of the member, make sure that I have change nickname "
                        "permission and my role is placed above the highest "
                        "role which the member has"
                    ),
                    color=discord.Color.random()
                )
            )
    
    @commands.command(aliases=["giverole"])
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: discord.Member = None, role: discord.Role = None
    ):
        if member and role is not None:
            try:
                await member.add_roles(role)
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"Successfully updated {member.mention} "
                            f"with {role.mention} role"
                        ),
                        color=discord.Color.random()
                    )
                )

            except discord.Forbidden:
                await ctx.send(
                    embed=discord.Embed(
                        title="Missing permissions",
                        description=(
                            f"I don't have permissions to update the roles"
                            f" of {member.mention}, either I don't have the"
                            f" permission or the member is above me"
                        ),
                        color=discord.Color.random()
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description="You need to define both member and role",
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=f"```{ctx.prefix}addrole <member> <role>```"
                ).set_footer(
                    text=(
                        "For both member and role, "
                        "either ping or ID can be used"
                    )
                )
            )

    @commands.command(name="removerole")
    @commands.has_permissions(manage_roles=True)
    async def remove_role(
        self, ctx, member: discord.Member = None, role: discord.Role = None
    ):
        if member and role is not None:
            try:
                await member.remove_roles(role)
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"Successfully updated {member.mention} "
                            f"by removing {role.mention} role"
                        ),
                        color=discord.Color.random()
                    )
                )

            except discord.Forbidden:
                await ctx.send(
                    embed=discord.Embed(
                        title="Missing permissions",
                        description=(
                            f"I don't have permissions to update the roles of"
                            f" {member.mention}, either I don't have the"
                            f" permission or the member is above me"
                        ),
                        color=discord.Color.random()
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description="You need to define both member and role",
                    color=discord.Color.random()
                ).add_field(
                    name="Format",
                    value=(
                        f"```{ctx.prefix}removerole"
                        f" <member> <role>```"
                    )
                ).set_footer(
                    text=(
                        "For both member and role,"
                        " either ping or ID can be used"
                    )
                )
            )
    
        
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mroles(self,ctx, role: discord.Role, members: commands.Greedy[discord.Member]):
        for m in members:
            await m.add_roles(role)
            await asyncio.sleep(1) 
        await ctx.send("Done!")
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel=None,*,role: discord.Role):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False
        await channel.set_permissions(role,overwrite=overwrite)
        await ctx.reply('Channel locked.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None,*,role: discord.Role):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = True
        await channel.set_permissions(role,overwrite=overwrite)
        await ctx.reply('Channel unlocked.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel : discord.TextChannel=None,*,role: discord.Role):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False
        overwrite.view_channel= False
        await channel.set_permissions(role,overwrite=overwrite)
        await ctx.reply('Now Channel Is In Hidden Mod.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unhide(self,ctx, channel : discord.TextChannel=None,*,role: discord.Role):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = True
        overwrite.view_channel= True
        await channel.set_permissions(role,overwrite=overwrite)
        await ctx.reply('Channel Unhide Successful.')


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def close_all(self,ctx,role: discord.Role):
        guild=ctx.guild	
        for chan in guild.channels:
            await chan.set_permissions(role, send_messages=False,read_messages=False)
        await ctx.send("done")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def open_all(self,ctx,role: discord.Role):
        guild=ctx.guild	
        for i in ctx.guild.channels:
            await i.set_permissions(role, send_messages=True,read_messages=True)
        await ctx.send("done")
    
    @commands.command(aliases=['makerole'])
    @commands.has_permissions(manage_roles=True) 
    async def create_role(self,ctx, *, name):
        guild = ctx.guild
        await guild.create_role(name=name)
        await ctx.reply(f'Role `{name}` has been created')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True) 
    async def delrole(self,ctx, *,role_name):
        role = discord.utils.get(ctx.message.guild.roles, name=role_name)
        if role:
            try:
                await role.delete()
                await ctx.reply("The role `{}`has been deleted!".format(role.name))
            except discord.Forbidden:
                await ctx.reply("Missing Permissions to delete this role!")
            else:
                await ctx.reply("The role doesn't exist!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def vcmuteall(self,ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=True)
            await ctx.reply("`{} `told me to mute everyone in this channel".format(ctx.author))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def vcunmuteall(self,ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=False)
            await ctx.reply("`{} `told me to unmute everyone in this channel".format(ctx.author))

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def vcmute(self,ctx,member: discord.Member):
        await member.edit(mute=True)
        await ctx.reply("Muted")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def vcunmute(self,ctx,member: discord.Member):
        await member.edit(mute=False)
        await ctx.reply("UnMuted")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def vcundeafen(self,ctx,member: discord.Member):
        await member.edit(deafen=False)
        await ctx.reply("UnDeafen")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def vcdeafen(self,ctx,member: discord.Member):
        await member.edit(deafen=True)
        await ctx.reply("Deafen")

    
    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.has_permissions(administrator=True)
    async def toggle(self,ctx, *, command):
        command = self.bot.get_command(command)
        if command is None:
            embed = discord.Embed(title="ERROR", description="I can't find a command with that name!", color=0xff0000)
            await ctx.send(embed=embed)
        elif ctx.command == command:
            embed = discord.Embed(title="ERROR", description="You cannot disable this command.", color=0xff0000)
            await ctx.send(embed=embed)
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = discord.Embed(title="Toggle", description=f"I have {ternary} {command.qualified_name} for you!", color=0xff00c8)
            await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self,ctx, minutes: float = 30):
            seconds = minutes * 60
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    send_messages=False
                )
            }
            await ctx.send(f"Are you sure you want to lock down this guild for {minutes}m? Type 'yes' or 'no'.")

            def check(m):
                return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond, try again.")
            else:
                if msg.content.lower() in ['yes', 'y', ]:
                    channels = []

                    for channel in ctx.guild.text_channels:
                        if channel.overwrites_for(ctx.guild.default_role).read_messages != False:
                            if channel.overwrites_for(ctx.guild.default_role).send_messages != False:
                                await channel.edit(overwrites=overwrites)
                                channels.append(channel)

                    await ctx.send(f'Alright, I removed everyone\'s perms for the next {minutes}m.')
                    await asyncio.sleep(seconds)
                    overwrites_revert = {
                        ctx.guild.default_role: discord.PermissionOverwrite(
                            send_messages=True
                        )
                    }
                    for channel in channels:
                        await channel.edit(overwrites=overwrites_revert)
                    return await ctx.reply(f'{ctx.author.mention}, this guild is no longer in lockdown.')
                elif msg.content.lower() in ['no', 'n']:
                    return await ctx.reply('Alright, lockdown sequence cancelled.')
                else:
                    return await ctx.reply('That\'s not a valid option, try again.')
        

    
def setup(bot):
    bot.add_cog(moderation(bot))
    print("Mod Cog is Loaded")