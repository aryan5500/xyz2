import discord
import json 
import asyncio
import random
import secrets
from io import BytesIO
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import clean_content
from discord.ext.commands.cooldowns import BucketType

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def spam(self,ctx, amount:int, *, message):
        await ctx.message.delete()
        for i in range(amount): 
            await ctx.send(message)
    
    @commands.command()
    async def say(self,ctx,*, saymsg=None):
        if saymsg==None:
            return await ctx.send("You Must Tell Me A Message To Say!")
        sayembed=discord.Embed(title=f"{ctx.author} Send A Message", description=f"{saymsg}", color=0x9208ea)
        await ctx.message.delete()
        await ctx.send(embed=sayembed)
    
    @commands.command(name="Meme")
    async def meme(self,ctx):
        embed = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed=discord.Embed(color=discord.Color.random())
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
    
    @commands.command()
    async def timer(self,ctx, timeInput,*, message):
        try:
            try:
                time = int(timeInput)
            except:
                convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
                time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
            if time > 86400:
                await ctx.send("I can\'t do timers over a day long")
                return
            if time <= 0:
                await ctx.send("Timers don\'t go into negatives :/")
                return
            if time >= 3600:
                message = await ctx.send(f"Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
            elif time >= 60:
                message = await ctx.send(f"Timer: {time//60} minutes {time%60} seconds")
            elif time < 60:
                message = await ctx.send(f"Timer: {time} seconds")
            while True:
                try:
                    await asyncio.sleep(5)
                    time -= 5
                    if time >= 3600:
                        await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")
                    elif time >= 60:
                        await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")
                    elif time < 60:
                        await message.edit(content=f"Timer: {time} seconds")
                    if time <= 0:
                        await message.edit(content="Ended!")
                        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!{message}")
                        break
                except:
                    break
        except:
            await ctx.send(f"Alright, first you gotta let me know how I\'m gonna time **{timeInput}**....")
    
    @commands.command()
    async def guess(self,ctx):
        
        await ctx.send('Guess my number')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        msg = await self.bot.wait_for("message", check=check)
        
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        correct_number = random.choice(number_list)
        if number == correct_number:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0xFF0000)
            embedVar.add_field(name='You Picked The Correct Number! You Won', value="Thanks For Playing!")
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0xFF0000)
            embedVar.add_field(name="Sorry, You Picked The Wrong Number", value="Thanks For Playing")
            await ctx.send(embed=embedVar)
    
    @commands.command(aliases=['8ball'])
    async def eightball(self,ctx, *, _ballInput: clean_content):
            choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
            if choiceType == "(Affirmative)":
                prediction = random.choice(["It is certain ", 
                                            "It is decidedly so ", 
                                            "Without a doubt ", 
                                            "Yes, definitely ", 
                                            "You may rely on it ", 
                                            "As I see it, yes ",
                                            "Most likely ", 
                                            "Outlook good ", 
                                            "Yes ", 
                                            "Signs point to yes "]) + ":8ball:"

                emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
            elif choiceType == "(Non-committal)":
                prediction = random.choice(["Reply hazy try again ", 
                                            "Ask again later ", 
                                            "Better not tell you now ", 
                                            "Cannot predict now ", 
                                            "Concentrate and ask again "]) + ":8ball:"
                emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
            elif choiceType == "(Negative)":
                prediction = random.choice(["Don't count on it ", 
                                            "My reply is no ", 
                                            "My sources say no ", 
                                            "Outlook not so good ", 
                                            "Very doubtful "]) + ":8ball:"
                emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
            emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
            await ctx.send(embed=emb)
    
    @commands.command()
    async def combine(self,ctx, name1: clean_content, name2: clean_content):
            name1letters = name1[:round(len(name1) / 2)]
            name2letters = name2[round(len(name2) / 2):]
            ship = "".join([name1letters, name2letters])
            emb = discord.Embed(color=0x9C84EF, description = f"{ship}")
            emb.set_author(name=f"{name1} + {name2}")
            await ctx.send(embed=emb)
    
    @commands.command(aliases=['gay-scanner', 'gayscanner', 'gay'])
    async def gay_scanner(self,ctx,* ,user: clean_content=None):
            if not user:
                user = ctx.author.name
            gayness = random.randint(0,100)
            if gayness <= 33:
                gayStatus = random.choice(["No homo", 
                                        "Wearing socks", 
                                        '"Only sometimes"', 
                                        "Straight-ish", 
                                        "No homo bro", 
                                        "Girl-kisser", 
                                        "Hella straight"])
                gayColor = 0xFFC0CB
            elif 33 < gayness < 66:
                gayStatus = random.choice(["Possible homo", 
                                        "My gay-sensor is picking something up", 
                                        "I can't tell if the socks are on or off", 
                                        "Gay-ish", 
                                        "Looking a bit homo", 
                                        "lol half  g a y", 
                                        "safely in between for now"])
                gayColor = 0xFF69B4
            else:
                gayStatus = random.choice(["LOL YOU GAY XDDD FUNNY", 
                                        "HOMO ALERT", 
                                        "MY GAY-SENSOR IS OFF THE CHARTS", 
                                        "STINKY GAY", 
                                        "BIG GEAY", 
                                        "THE SOCKS ARE OFF", 
                                        "HELLA GAY"])
                gayColor = 0xFF00FF
            emb = discord.Embed(description=f"Gayness for **{user}**", color=gayColor)
            emb.add_field(name="Gayness:", value=f"{gayness}% gay")
            emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
            emb.set_author(name="Gay-Scanner™")
            await ctx.send(embed=emb)
    
    @commands.command()
    async def ship(self,ctx, name1 : clean_content, name2 : clean_content):
            shipnumber = random.randint(0,100)
            if 0 <= shipnumber <= 10:
                status = "Really low! {}".format(random.choice(["Friendzone ;(", 
                                                                'Just "friends"', 
                                                                '"Friends"', 
                                                                "Little to no love ;(", 
                                                                "There's barely any love ;("]))
            elif 10 < shipnumber <= 20:
                status = "Low! {}".format(random.choice(["Still in the friendzone", 
                                                        "Still in that friendzone ;(", 
                                                        "There's not a lot of love there... ;("]))
            elif 20 < shipnumber <= 30:
                status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!", 
                                                        "But there's a small bit of love somewhere", 
                                                        "I sense a small bit of love!", 
                                                        "But someone has a bit of love for someone..."]))
            elif 30 < shipnumber <= 40:
                status = "Fair! {}".format(random.choice(["There's a bit of love there!", 
                                                        "There is a bit of love there...", 
                                                        "A small bit of love is in the air..."]))
            elif 40 < shipnumber <= 60:
                status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO", 
                                                            "It appears one sided!", 
                                                            "There's some potential!", 
                                                            "I sense a bit of potential!", 
                                                            "There's a bit of romance going on here!", 
                                                            "I feel like there's some romance progressing!", 
                                                            "The love is getting there..."]))
            elif 60 < shipnumber <= 70:
                status = "Good! {}".format(random.choice(["I feel the romance progressing!", 
                                                        "There's some love in the air!", 
                                                        "I'm starting to feel some love!"]))
            elif 70 < shipnumber <= 80:
                status = "Great! {}".format(random.choice(["There is definitely love somewhere!", 
                                                        "I can see the love is there! Somewhere...", 
                                                        "I definitely can see that love is in the air"]))
            elif 80 < shipnumber <= 90:
                status = "Over average! {}".format(random.choice(["Love is in the air!", 
                                                                "I can definitely feel the love", 
                                                                "I feel the love! There's a sign of a match!", 
                                                                "There's a sign of a match!", 
                                                                "I sense a match!", 
                                                                "A few things can be imporved to make this a match made in heaven!"]))
            elif 90 < shipnumber <= 100:
                status = "True love! {}".format(random.choice(["It's a match!", 
                                                            "There's a match made in heaven!", 
                                                            "It's definitely a match!", 
                                                            "Love is truely in the air!", 
                                                            "Love is most definitely in the air!"]))

            if shipnumber <= 33:
                shipColor = 0xE80303
            elif 33 < shipnumber < 66:
                shipColor = 0xff6600
            else:
                shipColor = 0x3be801

            emb = (discord.Embed(color=shipColor, \
                                title="Love test for:", \
                                description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                                                                                            ":sparkling_heart:", 
                                                                                                            ":heart_decoration:", 
                                                                                                            ":heart_exclamation:", 
                                                                                                            ":heartbeat:", 
                                                                                                            ":heartpulse:", 
                                                                                                            ":hearts:", 
                                                                                                            ":blue_heart:", 
                                                                                                            ":green_heart:", 
                                                                                                            ":purple_heart:", 
                                                                                                            ":revolving_hearts:", 
                                                                                                            ":yellow_heart:", 
                                                                                                            ":two_hearts:"]))))
            emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
            emb.add_field(name="Status:", value=(status), inline=False)
            emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
            await ctx.send(embed=emb)
    
    player1 = ""
    player2 = ""
    turn = ""
    gameOver = True

    board = []

    winningConditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    @commands.command()
    async def tictactoe(self,ctx, p1: discord.Member, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")

    @commands.command()
    async def place(self,ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                    board[pos - 1] = mark
                    count += 1

                    
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                   
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the !tictactoe command.")


    def checkWinner(winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True

    @tictactoe.error
    async def tictactoe_error(ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    @place.error
    async def place_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")
    
    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(1, 10, BucketType.user)
    async def spin(self,ctx):
            emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
            a = random.choice(emojis)
            b = random.choice(emojis)
            c = random.choice(emojis)

            slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

            if (a == b == c):
                await ctx.send(f"{slotmachine} All matching, you won! 🎉")
            elif (a == b) or (a == c) or (b == c):
                await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
            else:
                await ctx.send(f"{slotmachine} No match, you lost 😢")
    
    @commands.command(aliases=["howhot", "hot"])
    async def hotcalc(self,ctx, *, user: discord.Member = None):
            user = user or ctx.author

            random.seed(user.id)
            r = random.randint(1, 100)
            hot = r / 1.17

            if hot > 75:
                emoji = "💞"
            elif hot > 50:
                emoji = "💖"
            elif hot > 25:
                emoji = "❤"
            else:
                emoji = "💔"

            await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")
    
    @commands.command()
    async def beer(self,ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
            if not user or user.id == ctx.author.id:
                return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
            if user.id == self.bot.user.id:
                return await ctx.send("*drinks beer with you* 🍻")
            if user.bot:
                return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

            beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            msg = await ctx.send(beer_offer)

            def reaction_check(m):
                if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                    return True
                return False

            try:
                await msg.add_reaction("🍻")
                await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
                await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
            except asyncio.TimeoutError:
                await msg.delete()
                await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
            except discord.Forbidden:
                beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
                beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
                await msg.edit(content=beer_offer)
    
    @commands.command()
    async def password(self,ctx, nbytes: int = 18):
            if nbytes not in range(3, 15):
                embed=discord.Embed(title="Oops Something Is Wrong",color=0x9C84EF)
                embed.add_field(name="Oky Got It Its lenth Error",value="I only accept any numbers between 3-15")
                return await ctx.send(embed=embed)
            if hasattr(ctx, "guild") and ctx.guild is not None:
                embed2=discord.Embed(title="Oops Something Is Wrong",color=0x9C84EF)
                embed2.add_field(name="Check Dm",value=f"Sending you a private message with your random generated password **{ctx.author.name}**")
                await ctx.send(embed=embed2)
                embed3=discord.Embed(title="Thanks Me Later",color=0x9C84EF)
                embed3.add_field(name="Here Is Your Secrets Password", value=f"🎁 **{secrets.token_urlsafe(nbytes)}**")
                await ctx.author.send(embed=embed3)
    
    @commands.command()
    async def reverse(self,ctx, *, text: str):
            t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
            embed=discord.Embed(title="Reverse Text Verson",color=0x9C84EF)
            embed.add_field(name="Its Funny Or Not :astonished: ",value=f"🔁 {t_rev}")
            await ctx.send(embed=embed)
    
    @commands.command()
    async def send(self,ctx,*, saymsg=None):
        if saymsg==None:
            return await ctx.send("You Must Tell Me A Message To Say!")
        sayembed=discord.Embed(description=f"{saymsg}", color=0x9208ea)
        await ctx.message.delete()
        await ctx.send(embed=sayembed)
      
def setup(bot):
    bot.add_cog(fun(bot))
    print("fun Cog is Loaded")