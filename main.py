import discord
import sqlite3
import datetime
import os

my_secret = os.environ['token']

from discord.ext import commands

client = commands.Bot(command_prefix=';')

client.remove_command("help")


# ------------------
@client.command()
async def ping(ctx):
    ping = client.latency * 1000
    final = '%0.2f' % ping
    embed = discord.Embed(description="Pong! " + str(final) + " ms",
                          colour=discord.Colour.from_rgb(88, 101, 242))
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    member = ctx.author
    embed = discord.Embed(
        title="Help",
        description="All commands are listed below with descriptions",
        colour=discord.Colour.from_rgb(88, 101, 242))
    embed.add_field(name=";blacklist/;bl",
                    value="ID bans a user from the guild",
                    inline=True)
    embed.add_field(name=";whitelist/;wl",
                    value="ID unbans a user from the guild",
                    inline=True)
    embed.add_field(name=";blacklists/;bls",
                    value="See all current ID banned members from the guild")
    embed.add_field(name=";getuser",
                    value="Find a user's name based on id",
                    inline=True)
    embed.add_field(name=";ping",
                    value="Get current latency of the bot",
                    inline=True)
    embed.add_field(name=";info",
                    value="View additional information about Blacklists",
                    inline=True)
    embed.add_field(name=";fix",
                    value="If commands don't work, run this command",
                    inline=True)
    embed.timestamp = datetime.datetime.utcnow()
    await member.send(embed=embed)
    await ctx.message.add_reaction("<check:872541200811454555>")


@client.command()
async def info(ctx):
    member = ctx.author
    embed = discord.Embed(title="Blacklists Info",
                          colour=discord.Colour.from_rgb(88, 101, 242))
    embed.add_field(name="Guilds",
                    value="Blacklists is currently in " +
                    str(len(client.guilds)) + " Guilds!",
                    inline=True)
    embed.add_field(name="Credits",
                    value="The bot was made by Luminous#4617",
                    inline=True)
    embed.add_field(
        name="Invite Bot",
        value=
        "[Invite](https://discord.com/oauth2/authorize?client_id=794291479161077761&scope=bot&permissions=347220) me to your server",
        inline=True)
    embed.add_field(
        name="Support Server",
        value=
        "[Join](https://discord.gg/sGfRZH5rAz) the server for Blacklists support",
        inline=True)
    embed.add_field(name="Vote",
                    value="[Top.gg](https://top.gg/bot/794291479161077761)",
                    inline=True)
    embed.timestamp = datetime.datetime.utcnow()
    await member.send(embed=embed)
    await ctx.message.add_reaction("<check:872541200811454555>")


# ------------------


@client.command()
@commands.has_permissions(administrator=True)
async def fix(ctx):
    await ctx.message.add_reaction("<check:872541200811454555>")
    server = ctx.message.guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("CREATE TABLE {} (id interger)".format("server" + str(server)))
    conn.commit()
    conn.close()


@client.command()
@commands.has_permissions(ban_members=True)
async def blacklists(ctx):
    server = ctx.channel.guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format("server" + str(server)))
    result = ''.join(str(c.fetchall()))
    conn.commit()
    conn.close()
    ending = result.replace('(', '').replace(')', '').replace("'", '').replace(
        '[', '').replace(']', '').replace(",", " ")
    embed = discord.Embed(title="All ID Blacklists",
                          description="`" + str(ending) + "`",
                          colour=discord.Colour.from_rgb(88, 101, 242))
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def bls(ctx):
    server = ctx.channel.guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format("server" + str(server)))
    result = ''.join(str(c.fetchall()))
    conn.commit()
    conn.close()
    ending = result.replace('(', '').replace(')', '').replace("'", '').replace(
        '[', '').replace(']', '').replace(",", " ")
    embed = discord.Embed(title="All ID Blacklists",
                          description="`" + str(ending) + "`",
                          colour=discord.Colour.from_rgb(88, 101, 242))
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)


@client.command()
async def getuser(ctx, id):
    embed = discord.Embed(title="ID Check",
                          description="Username: " +
                          str(await client.fetch_user(id)),
                          colour=discord.Colour.from_rgb(88, 101, 242))
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)


# ------------------


@client.command()
@commands.has_permissions(ban_members=True)
async def blacklist(ctx, id):
    server = ctx.channel.guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {} WHERE id={}".format("server" + str(server),
                                                    id))
    datacheck = (c.fetchall())
    if datacheck != []:
        await ctx.send('That user is already blacklisted!')
    else:
        c.execute("INSERT INTO {} VALUES ({})".format("server" + str(server),
                                                      id))
        conn.commit()
        conn.close()
        embed = discord.Embed(title="Blacklisted User",
                              description=id +
                              " has been added to the blacklist",
                              colour=discord.Colour.from_rgb(0, 0, 0))
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def bl(ctx, id):
    server = ctx.channel.guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {} WHERE id={}".format("server" + str(server),
                                                    id))
    datacheck = (c.fetchall())
    if datacheck != []:
        await ctx.send('That user is already blacklisted!')
    else:
        c.execute("INSERT INTO {} VALUES ({})".format("server" + str(server),
                                                      id))
        conn.commit()
        conn.close()
        embed = discord.Embed(title="Blacklisted User",
                              description=id +
                              " has been added to the blacklist",
                              colour=discord.Colour.from_rgb(0, 0, 0))
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def whitelist(ctx, id):
    server = ctx.channel.guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {} WHERE id={}".format("server" + str(server),
                                                    id))
    datacheck = (c.fetchall())
    if datacheck == []:
        await ctx.send('That user is not on the blacklist!')
    else:
        c.execute("DELETE FROM {} WHERE id={}".format("server" + str(server),
                                                      id))
        conn.commit()
        conn.close()
        embed = discord.Embed(title="Whitelisted User",
                              description=id + " has been whitelisted",
                              colour=discord.Colour.from_rgb(255, 255, 255))
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def wl(ctx, id):
    server = ctx.channel.guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {} WHERE id={}".format("server" + str(server),
                                                    id))
    datacheck = (c.fetchall())
    if datacheck == []:
        await ctx.send('That user is not on the blacklist!')
    else:
        c.execute("DELETE FROM {} WHERE id={}".format("server" + str(server),
                                                      id))
        conn.commit()
        conn.close()
        embed = discord.Embed(title="Whitelisted User",
                              description=id + " has been whitelisted",
                              colour=discord.Colour.from_rgb(255, 255, 255))
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


@client.event
async def on_guild_join(guild):
    server = guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("CREATE TABLE {} (id interger)".format("server" + str(server)))
    conn.commit()
    conn.close()


@client.event
async def on_guild_remove(guild):
    server = guild.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("DROP TABLE {}".format("server" + str(server)))
    conn.commit()
    conn.close()


@client.event
async def on_member_join(member):
    server = member.guild.id
    id = member.id
    conn = sqlite3.connect('blacklists.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {} WHERE id={}".format("server" + str(server),
                                                    id))
    datacheck = (c.fetchall())
    if datacheck != []:
        await member.ban(reason="Blacklisted")
    conn.commit()
    conn.close()


#-------------------
# Error Handling


@blacklist.error
async def blacklist_error(ctx, error):
    if isinstance(error, sqlite3.OperationalError):
        server = ctx.channel.guild.id
        conn = sqlite3.connect('blacklists.db')
        c = conn.cursor()
        c.execute("CREATE TABLE {} (id interger)".format("server" +
                                                         str(server)))
        await ctx.send(
            "We couldn't find your guild's blacklist. We have created a new one, please retry this command"
        )
    elif isinstance(error,
                    discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(
            "You are missing arguments! Format: `;blacklist <userid>`")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("❌ You are missing ban permissions!")
    else:
        raise error


@bl.error
async def bl_error(ctx, error):
    if isinstance(error, sqlite3.OperationalError):
        server = ctx.channel.guild.id
        conn = sqlite3.connect('blacklists.db')
        c = conn.cursor()
        c.execute("CREATE TABLE {} (id interger)".format("server" +
                                                         str(server)))
        await ctx.send(
            "We couldn't find your guild's blacklist. We have created a new one, please retry this command"
        )
    elif isinstance(error,
                    discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing arguments! Format: `;bl <userid>`")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("❌ You are missing ban permissions!")
    else:
        raise error


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, sqlite3.OperationalError):
        server = ctx.channel.guild.id
        conn = sqlite3.connect('blacklists.db')
        c = conn.cursor()
        c.execute("CREATE TABLE {} (id interger)".format("server" +
                                                         str(server)))
        await ctx.send(
            "We couldn't find your guild's blacklist. We have created a new one, please retry this command"
        )
    elif isinstance(error,
                    discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(
            "You are missing arguments! Format: `;whitelist <userid>`")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("❌ You are missing ban permissions!")
    else:
        raise error


@wl.error
async def wl_error(ctx, error):
    if isinstance(error, sqlite3.OperationalError):
        server = ctx.channel.guild.id
        conn = sqlite3.connect('blacklists.db')
        c = conn.cursor()
        c.execute("CREATE TABLE {} (id interger)".format("server" +
                                                         str(server)))
        await ctx.send(
            "We couldn't find your guild's blacklist. We have created a new one, please retry this command"
        )
    elif isinstance(error,
                    discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing arguments! Format: `;wl <userid>`")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("❌ You are missing ban permissions!")
    else:
        raise error


@blacklists.error
async def blacklists_error(ctx, error):
    if isinstance(error, sqlite3.OperationalError):
        server = ctx.channel.guild.id
        conn = sqlite3.connect('blacklists.db')
        c = conn.cursor()
        c.execute("CREATE TABLE {} (id interger)".format("server" +
                                                         str(server)))
        await ctx.send(
            "We couldn't find your guild's blacklist. We have created a new one, please retry this command"
        )
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("❌ You are missing ban permissions!")
    else:
        raise error


@bls.error
async def bls_error(ctx, error):
    if isinstance(error, sqlite3.OperationalError):
        server = ctx.channel.guild.id
        conn = sqlite3.connect('blacklists.db')
        c = conn.cursor()
        c.execute("CREATE TABLE {} (id interger)".format("server" +
                                                         str(server)))
        await ctx.send(
            "We couldn't find your guild's blacklist. We have created a new one, please retry this command"
        )
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("❌ You are missing ban permissions!")
    else:
        raise error


#----------------
# Additonal handlers


@getuser.error
async def getuser_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing arguments! Format: `;getuser <userid>`"
                       )
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("❌ That user doesn't exist!")
    else:
        raise error


@fix.error
async def fix_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("❌ You are missing administrator permissions!")


@help.error
async def help_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("🚫 Your direct messages are off!")
    else:
        raise error


@info.error
async def info_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("🚫 Your direct messages are off!")
    else:
        raise error


# ------------------


@client.event
async def on_connect():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(';help'))


@client.event
async def on_ready():
    print('Online!')


# ______________________________________________________________________________________________________________________

client.run(my_secret)
