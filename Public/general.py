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

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, member : discord.Member):
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

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    async def help(self, ctx):
        configCmds = """**w!config image <url>** - Change background image
**w!config message <args>** - Change the message on the welcome image
**w!config regular_message <args>** - Change the regular messaged displayed on user join
**w!config channel <#channel>** - Change the channel welcome messages will be sent to
**w!config welcome_color <hex>** - Change the colour of the Welcome text
**w!config text_color <hex>** - Change the color of the lines below Welcome"""

        embed=discord.Embed(description=f"**About**\n• Wave is an image based welcome bot, which provides customizability and premium support for **FREE**.\n\n**Commands**\n{configCmds}\n\n**Reminders**\n• The regular message option can be disabled by typing: \nw!config regular_message off\n\n**Information**\n• Due to system limitations we require all images to not exceed the maximum file size of 8 MB and that they be uploaded via https://gifyu.com/ in order to set your background image.", colour=0x2f3136)
        embed.set_author(name="Help", icon_url="https://cdn.discordapp.com/avatars/723573933521109083/6ffeb622ab2e1a33ba7c2ab916dca3ad.webp?size=1024")
        embed.set_image(url=f"attachment://tutorial.png")
        file = discord.File(f'{os.getcwd()}\Public\tutorial.png')
        await ctx.send(file=file,embed=embed)

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, args):
        await ctx.send(f"```{eval(args)}```")
def setup(bot):
    bot.add_cog(general(bot))