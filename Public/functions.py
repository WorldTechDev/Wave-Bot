from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageFile
import requests
from io import BytesIO
import json
import os

def get_size(url):
    resp = requests.get(url, stream=True).headers['content-length']
    return resp

def get_mb(bytes):
    lol = (bytes / 1e+6)
    return lol

def hex_to_rgb(hex):
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def read_json(filename):
    jsonFile = open(f"{os.getcwd()}\Public\Storage\guilds.json", 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def write_json(data):
    jsonFile = open(f'{os.getcwd()}\Public\Storage\guilds.json', 'w+') 
    jsonFile.write(json.dumps(data, indent=4))
    jsonFile.close()

def pretty_json(guild):
    jsonFile = open(f'{os.getcwd()}\Public\Storage\guilds.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    return json.dumps(data[str(guild)], indent=4, sort_keys=True)

def add_guild(guild):
    with open(f'{os.getcwd()}\Public\Storage\guilds.json') as jsonFile: 
        data = json.load(jsonFile)
        x = {
            guild: {
                "message": "You are member %memberCount%",
                "welcome_color": "ffffff",
                "text_color": "ffffff",
                "welcome_channel": "default",
                "regular_message": "Welcome %member%!"
            }
        }
        data.update(x)
        write_json(data)

def generate_banner(member, guild):
    if member == None:
        response = requests.get(member.avatar_url)
    else:
        response = requests.get(member.avatar_url)
    
    # Width, Height Variables
    W, H = (1650,1050)
    W1, H1 = (1650,1180)
    W2, H2 = (1650, 850)

    # Avatar Square -> Circle Conversion
    try:
        im = Image.open(BytesIO(response.content))
        if im.is_animated:
            im = Image.open(BytesIO(response.content)).convert('RGB').save(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}PFP.png')
        else:
            im = Image.open(BytesIO(response.content)).convert('RGB').save(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}PFP.png')
        im = Image.open(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}PFP.png')
        im = im.resize((300, 300))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}CirclePFP.png')
    except IOError as error:
        print(error)

    # Json Stuff
    data = read_json("guilds")
    textcolor = hex_to_rgb(data[str(guild.id)]["text_color"])
    welcomecolor = hex_to_rgb(data[str(guild.id)]["welcome_color"])

    # Stuff
    try:
        backgroundImg = Image.open(f'{os.getcwd()}\Public\Storage\guild_backgrounds\{guild.id}_background.png')
    except FileNotFoundError as error:
        backgroundImg = Image.open(f'{os.getcwd()}\Public\Storage\default_background.png')
    
        
    newProfilePic = Image.open(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}CirclePFP.png')
    backgroundImg.paste(newProfilePic, (675, 45), newProfilePic)

    # Messages
    msg = f"{member.name} to {guild.name}"
    msg2 = data[str(guild.id)]["message"].replace("%memberCount%", str(guild.member_count))
    msg3 = "Welcome"
    
    draw = ImageDraw.Draw(backgroundImg)

    # Fonts
    if len(msg) >= 50:
        font = ImageFont.truetype(f"Enigmatic.ttf", 42)
    elif len(msg) >= 75:
        font = ImageFont.truetype(f"Enigmatic.ttf", 32)
    elif len(msg) >= 100:
        font = ImageFont.truetype(f"Enigmatic.ttf", 24)
    else:
        font = ImageFont.truetype(f"Enigmatic.ttf", 64)
    #font = ImageFont.truetype("C:/Users/A/Desktop/Discord/Image Manipulation/fonts/Enigmatic.ttf", 64)
    font2 = ImageFont.truetype(f"Enigmatic.ttf", 55)
    font3 = ImageFont.truetype(f"commando.ttf", 150)

    # Font Size Management
    w, h = font.getsize(msg)
    w1, h1 = font2.getsize(msg2)
    w2, h2 = font3.getsize(msg3)

    # Text Drawing
    draw.text(((W-w)/2,(H-h)/2), msg, font=font, fill=textcolor)
    draw.text(((W1-w1)/2,(H1-h1)/2), msg2, font=font2, fill=textcolor)
    draw.text(((W2-w2)/2,(H2-h2)/2), msg3, font=font3, fill=welcomecolor)

    #Misc
    backgroundImg.save(f'{os.getcwd()}\Public\Storage\pfp_dump\{member.id}_background.png', quality=95)
    #image = Image.open(f"C:/Users/A/Desktop/Discord/Image Manipulation/Public/pfp_dump/{member.id}_background.png")
    
    #return image

def remove_shit(member):
    os.remove(f"{os.getcwd()}\Public\Storage\pfp_dump\{member.id}_background.png")
    os.remove(f"{os.getcwd()}\Public\Storage\pfp_dump\{member.id}CirclePFP.png")
    os.remove(f"{os.getcwd()}\Public\Storage\pfp_dump\{member.id}PFP.png")

def resize_calculator(image): #Code by https://stackoverflow.com/users/223092/mark-longair
    width  = image.size[0]
    height = image.size[1]

    aspect = width / float(height)

    ideal_width = 1650
    ideal_height = 710

    ideal_aspect = ideal_width / float(ideal_height)

    if aspect > ideal_aspect:
        new_width = int(ideal_aspect * height)
        offset = (width - new_width) / 2
        resize = (offset, 0, width - offset, height)
    else:
        new_height = int(width / ideal_aspect)
        offset = (height - new_height) / 2
        resize = (0, offset, width, height - offset)

    return resize

def check_guild(guild):
    data = read_json('guilds')
    if str(guild.id) in data.keys():
        return True
    else:
        add_guild(guild.id)

def read_global_config(filename):
    jsonFile = open(f'config.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def get_dir(type):
    data = read_global_config('config')
