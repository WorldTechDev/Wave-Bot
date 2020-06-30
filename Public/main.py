from discord import utils, Embed
from discord.ext import commands
from discord.utils import get
import discord
import re
import os

bot = commands.Bot(command_prefix=commands.when_mentioned_or("w!"), owner_id=623915291142914068)
extensions = ['general','config','events']
bot.remove_command('help')
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f"{extension} cannot be loaded. [{error}]")
            

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="w!help | Dev Build"))
    print("Wave Beta Release")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """Load a module"""
    await ctx.message.delete()
    try:
        if extension == "modules":
            await ctx.send(":x: You cannot load this module.")
        else:
            bot.load_extension(extension)
            await ctx.send(f":white_check_mark: Loaded `{extension}`")
    except Exception as error:
        c = discord.Embed(description=f"{extension} cannot be loaded.\n`{error}`", colour=0x2f3136)
        c.set_author(name=f"Wave", icon_url="https://cdn.discordapp.com/attachments/723573416963211305/727649420275089418/pngfind.com-hand-emoji-png-288401.png")
        await ctx.send(embed=c)

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Unload a module"""
    await ctx.message.delete()
    try:
        if extension == "modules":
            await ctx.send(":x: You cannot unload this module.")
        else:
            bot.unload_extension(extension)
            await ctx.send(f":white_check_mark: Unloaded `{extension}`")
    except Exception as error:
        c = discord.Embed(description=f"{extension} cannot be unloaded.\n`{error}`", colour=0x2f3136)
        c.set_author(name=f"Wave", icon_url="https://cdn.discordapp.com/attachments/723573416963211305/727649420275089418/pngfind.com-hand-emoji-png-288401.png")
        await ctx.send(embed=c)

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Reload a module"""
    await ctx.message.delete()
    try:
        if extension == "modules":
            await ctx.send(":x: You cannot reload this module.")
        else:
            bot.unload_extension(extension)
            bot.load_extension(extension)
            c = discord.Embed(description=f":white_check_mark: Reloaded Extension `{extension}`", colour=0x2f3136)
            await ctx.send(embed=c)
    except Exception as error:
        c = discord.Embed(description=f"{extension} cannot be reloaded.\n`{error}`", colour=0x2f3136)
        c.set_author(name=f"Wave", icon_url="https://cdn.discordapp.com/attachments/723573416963211305/727649420275089418/pngfind.com-hand-emoji-png-288401.png")
        await ctx.send(embed=c)

token = open(f"token.txt", "r").read()
bot.run(token)