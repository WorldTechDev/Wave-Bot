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
                await default_channel.send(file=discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{member.id}_background.png'))
            else:
                await default_channel.send(msg, file=discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{member.id}_background.png'))
        else:
            if data[str(member.guild.id)]['regular_message'] == "off":
                await welcome_channel.send(file=discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{member.id}_background.png'))
            else:
                await welcome_channel.send(msg, file=discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{member.id}_background.png'))
        remove_shit(member)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(description=f":no_entry: {error}", colour=0x2f3136)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(description=f":no_entry: {error}", colour=0x2f3136)
            await ctx.send(embed=embed)

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

            embed=discord.Embed(description=f"**About**\n• Wave is an image based welcome bot, which provides customizability and premium support for **FREE**.\n\n**Commands**\n{configCmds}\n\n**Reminders**\n• The regular message option can be disabled by typing: \nw!config regular_message off\n\n**Information**\n• Due to system limitations we require all images to not exceed the maximum file size of 8 MB and that they be uploaded via https://gifyu.com/ in order to set your background image.", colour=0x2f3136)
            embed.set_author(name="Thank you for adding Wave.", icon_url="https://cdn.discordapp.com/avatars/723573933521109083/6ffeb622ab2e1a33ba7c2ab916dca3ad.webp?size=1024")
            embed.set_image(url=f"attachment://tutorial.png")
            file = discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/tutorial.png')
            await default_channel.send(file=file,embed=embed)
        except Exception as error:
            error.send(f"```\nGUILD: {guild.name}\n{error}```")

def setup(bot):
    bot.add_cog(events(bot))
