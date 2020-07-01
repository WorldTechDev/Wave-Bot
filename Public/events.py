import asyncio
import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageFile
import requests
from io import BytesIO
import os, sys
import aiohttp
from cv2 import cv2
import numpy as np 
import urllib
import re
import json
from functions import get_size, get_mb, hex_to_rgb, read_json, write_json, pretty_json, add_guild, generate_banner, remove_shit, resize_calculator, check_guild

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        check_guild(member.guild)
        generate_banner(member, member.guild)
        default_channel = member.guild.system_channel
        data = read_json('guilds')
        _channel = data[str(member.guild.id)]['welcome_channel']
        welcome_channel = self.bot.get_channel(_channel)
        msg = data[str(member.guild.id)]['regular_message'].replace("%member%", member.mention)
        if data[str(member.guild.id)]['welcome_channel'] == "default":
            if data[str(member.guild.id)]['regular_message'] == "off":
                await default_channel.send(file=discord.File(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}_background.png'))
            else:
                await default_channel.send(msg, file=discord.File(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}_background.png'))
        else:
            if data[str(member.guild.id)]['regular_message'] == "off":
                await welcome_channel.send(file=discord.File(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}_background.png'))
            else:
                await welcome_channel.send(msg, file=discord.File(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}_background.png'))
        remove_shit(member)

    #@commands.Cog.listener()
    #async def on_command_error(self, ctx, error):
    #    error = self.bot.get_channel(727193674714448034)
    #    if isinstance(error, commands.CommandOnCooldown):
    #        embed=discord.Embed(description=f":no_entry: {error}", colour=0x2f3136)
    #        await ctx.send(embed=embed)
    #    elif isinstance(error, commands.BadArgument):
    #        embed=discord.Embed(description=f":no_entry: {error}", colour=0x2f3136)
    #        await ctx.send(embed=embed)
    #    else:
    #        await error.send(f"```\nGUILD: {ctx.guild.name}\n{error}```")
    #        print(error)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        lol = self.bot.get_channel(727193750694264954)
        error = self.bot.get_channel(727193674714448034)
        await asyncio.sleep(2)
        try:
            await lol.send(f":envelope_with_arrow: Joined guild: {guild.name} ({guild.id})")
            default_channel = guild.system_channel
            configCmds = """**w!config image <url>** - Change background image
    **w!config message <args>** - Change the message on the welcome image
    **w!config regular_message <args>** - Change the regular messaged displayed on user join
    **w!config channel <#channel>** - Change the channel welcome messages will be sent to
    **w!config welcome_color <hex>** - Change the colour of the Welcome text
    **w!config text_color <hex>** - Change the color of the lines below Welcome"""

            embed=discord.Embed(description=f"To get started set your welcome channel by typing **w!config channel #channel-name**.\nFor instructions on fully fledged bot usage please type **w!help**.\n\nHave any questions or concerns? Join our support discord, https://discord.gg/RhkBuFt.", colour=0x2f3136)
            embed.set_author(name="Thank you for adding Wave.", icon_url="https://cdn.discordapp.com/avatars/723573933521109083/6ffeb622ab2e1a33ba7c2ab916dca3ad.webp?size=1024")
            await default_channel.send(embed=embed)
        except Exception as error:
            await error.send(f"```\nGUILD: {guild.name}\n{error}```")


def setup(bot):
    bot.add_cog(events(bot))
