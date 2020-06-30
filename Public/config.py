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

class imageGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True)
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def config(self, ctx):
        #await ctx.message.delete()
        check_guild(ctx.message.guild)
        generate_banner(ctx.message.author, ctx.message.guild)
        embed=discord.Embed(description=f"Current Configuration```json\n{pretty_json(ctx.message.guild.id)}```\n**Arguments**\n• image - Change the background image of your welcome message.\n• textcolor - change the color of the text in the welcome image\n• welcomecolor - change the color of the welcome text in the welcome image\n• message - Change the 3rd line of text on your welcome message\n\n**Reminder:** *You can use the placeholder %memberCount% to display the member count in your custom messages*\n\n**Current Background Image**", colour=0x2f3136)
        embed.set_author(name="Configuration", icon_url="https://cdn.discordapp.com/avatars/723573933521109083/6ffeb622ab2e1a33ba7c2ab916dca3ad.webp?size=1024")
        file = discord.File(f"C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{ctx.message.author.id}_background.png")
        embed.set_image(url=f"attachment://{ctx.message.author.id}_background.png")
        await ctx.send(file=file, embed=embed)
        remove_shit(ctx.message.author)
    
    @config.command()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def image(self, ctx, url=None):
        await ctx.message.delete()
        if url == None:
            embed=discord.Embed(description=":no_entry: Invalid Args, please enter an image URL. (https://gifyu.com/)", colour=0x2f3136)
            await ctx.send(embed=embed)
        else:
            check = re.compile(r'(?:http(s)?:\/\/)?[\w.-]+\/images\/[A-z 0-9].+[.](?:jpg|gif|png)')
            if check.match(url):
                if int(get_size(url)) > 8e+6:
                    await ctx.send(":x: The image provided is larger than 8 MB.")
                im = Image.open(BytesIO(requests.get(url).content)).convert('RGB').save(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/guild_backgrounds/{ctx.message.guild.id}_background.png')
                im = Image.open(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/guild_backgrounds/{ctx.message.guild.id}_background.png')
                im = im.crop(resize_calculator(im)).resize((1650, 710), Image.ANTIALIAS)
                im.save(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/guild_backgrounds/{ctx.message.guild.id}_background.png')
                generate_banner(ctx.message.author, ctx.message.guild)
                file = discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{ctx.message.author.id}_background.png')
                embed=discord.Embed(description=":white_check_mark: Your background image has been successfully set.\n\n**Preview**", colour=0x2f3136)
                embed.set_image(url=f"attachment://{ctx.message.author.id}_background.png")
                await ctx.send(file=file, embed=embed)
                remove_shit(ctx.message.author)
            else:
                embed=discord.Embed(description=":no_entry: Invalid URL, please upload your image to https://gifyu.com/", colour=0x2f3136)
                await ctx.send(embed=embed)
    
    @config.command()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def message(self, ctx, *, args):
        #await ctx.message.delete()
        check_guild(ctx.message.guild)
        if len(args) > 50:
            embed=discord.Embed(description=":no_entry: Error! Please use less than 50 characters.", colour=0x2f3136)
            await ctx.send(embed=embed)
        else:
            data = read_json('guilds')
            data[str(ctx.message.guild.id)]['message'] = args
            write_json(data)
            generate_banner(ctx.message.author, ctx.message.guild)
            file = discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{ctx.message.author.id}_background.png')
            embed=discord.Embed(description=f":white_check_mark: Your message has been changed.\n\n**Preview**", colour=0x2f3136)
            embed.set_image(url=f"attachment://{ctx.message.author.id}_background.png")
            await ctx.send(file=file,embed=embed)
            remove_shit(ctx.message.author)

    @config.command(aliases=['regularmessage', 'regularmsg'])
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def regular_message(self, ctx, *, args):
        #await ctx.message.delete()
        check_guild(ctx.message.guild)
        data = read_json('guilds')
        data[str(ctx.message.guild.id)]['regular_message'] = args
        write_json(data)
        embed=discord.Embed(description=f":white_check_mark: Your regular message has been changed. ({args})", colour=0x2f3136)
        await ctx.send(embed=embed)

    @config.command(aliases=['welcomechannel', 'welcome_channel'])
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def channel(self, ctx, channel : discord.TextChannel):
        #await ctx.message.delete()
        check_guild(ctx.message.guild)
        data = read_json('guilds')
        data[str(ctx.message.guild.id)]['welcome_channel'] = channel.id
        write_json(data)
        embed=discord.Embed(description=f":white_check_mark: Your welcome channel has been set to {channel.mention}", colour=0x2f3136)
        await ctx.send(embed=embed)
        

    @config.command(aliases=['text_color','text_colour', 'textcolour'])
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def textcolor(self, ctx, hex="ffffff"):
        #await ctx.message.delete()
        check_guild(ctx.message.guild)
        check = re.compile(r'([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        if check.match(hex):
            data = read_json('guilds')
            data[str(ctx.message.guild.id)]['text_color'] = hex
            write_json(data)
            generate_banner(ctx.message.author, ctx.message.guild)
            file = discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{ctx.message.author.id}_background.png')
            embed=discord.Embed(description=f":white_check_mark: Your text color has been changed. `#{hex} | {hex_to_rgb(hex)}`\n\n**Preview**", colour=0x2f3136)
            embed.set_image(url=f"attachment://{ctx.message.author.id}_background.png")
            await ctx.send(file=file,embed=embed)
            remove_shit(ctx.message.author)
        else:
            embed=discord.Embed(description=f":no_entry: Invalid Hex Colour Code Passed. ({hex})", colour=0x2f3136)
            await ctx.send(embed=embed)

    @config.command(aliases=['welcome_color','welcomecolour', 'welcome_colour'])
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def welcomecolor(self, ctx, hex="ffffff"):
        #await ctx.message.delete()
        check_guild(ctx.message.guild)
        check = re.compile(r'([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        if check.match(hex):
            data = read_json('guilds')
            data[str(ctx.message.guild.id)]['welcome_color'] = hex
            write_json(data)
            generate_banner(ctx.message.author, ctx.message.guild)
            file = discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{ctx.message.author.id}_background.png')
            embed=discord.Embed(description=f":white_check_mark: Your welcome text color has been changed. `#{hex} | {hex_to_rgb(hex)}`\n\n**Preview**", colour=0x2f3136)
            embed.set_image(url=f"attachment://{ctx.message.author.id}_background.png")
            await ctx.send(file=file,embed=embed)
            remove_shit(ctx.message.author)
        else:
            embed=discord.Embed(description=f":no_entry: Invalid Hex Colour Code Passed. ({hex})", colour=0x2f3136)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def wtest(self, ctx, member : discord.Member):
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

        embed=discord.Embed(description=f"**About**\n• Wave is an image based welcome bot, which provides customizability and premium support for **FREE**.\n\n**Commands**\n{configCmds}\n**Reminders**\n\n• The regular message option can be disabled by typing: \nw!config regular_message off\n\n**Information**\n• Due to system limitations we require all images to not exceed the maximum file size of 8 MB and that they be uploaded via https://gifyu.com/ in order to set your background image.", colour=0x2f3136)
        embed.set_author(name="Help", icon_url="https://cdn.discordapp.com/avatars/723573933521109083/6ffeb622ab2e1a33ba7c2ab916dca3ad.webp?size=1024")
        embed.set_image(url=f"attachment://tutorial.png")
        file = discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/tutorial.png')
        await ctx.send(file=file,embed=embed)
    
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

            embed=discord.Embed(description=f"**About**\n• Wave is an image based welcome bot, which provides customizability and premium support for **FREE**.\n\n**Commands**\n{configCmds}\n**Reminders**\n\n• The regular message option can be disabled by typing: \nw!config regular_message off\n\n**Information**\n• Due to system limitations we require all images to not exceed the maximum file size of 8 MB and that they be uploaded via https://gifyu.com/ in order to set your background image.", colour=0x2f3136)
            embed.set_author(name="Thank you for adding Wave.", icon_url="https://cdn.discordapp.com/avatars/723573933521109083/6ffeb622ab2e1a33ba7c2ab916dca3ad.webp?size=1024")
            embed.set_image(url=f"attachment://tutorial.png")
            file = discord.File(f'C:/Users/A/Desktop/Discord/Image Manipulation/Public/tutorial.png')
            await default_channel.send(file=file,embed=embed)
        except Exception as error:
            error.send(f"```\nGUILD: {guild.name}\n{error}```")

def setup(bot):
    bot.add_cog(imageGen(bot))