# ETG Wiki Web Scraper bot
# @author PlaguedPixel
import asyncio
import re
import discord
from discord import Game
from discord.ext.commands import Bot
from requests import get
import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

BOT_PREFIX = ("etg!", "etg:")
TOKEN = ""

MOD_ICON_URL = "https://i.imgur.com/SBs5A4v.png"

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name="modlist",
                aliases=["mods","mod_list","mod"],
                pass_context=True)
async def modlist(ctx, *args):
    url = "https://modworkshop.net/mydownloads.php?action=browse_cat&cid=286&name=&page=1"
    modname = ""
    prefix = ""
    if args is not ():
        modname = " ".join(args)
        prefix = "**Search Results:**\n"
    output = web_request_mods("", url, modname, 0, "")
    embed = discord.Embed(color=discord.Color.dark_orange())
    embed.description = prefix+output[0]
    footer = output[1]
    embed.set_footer(text=footer)
    embed.set_author(name="Mods", url=url, icon_url=MOD_ICON_URL)
    await client.send_message(ctx.message.channel, embed=embed)

@client.event
async def on_ready():
    subnevernamed = Game(name="Nevernamed's videos", url="https://www.youtube.com/channel/UCes-sakT2ts-SxFXYlK-CBw", type=3)
    await client.change_presence(game=subnevernamed)
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return resp.status_code == 200 and content_type is not None and content_type.find('html') > -1

def log_error(e):
    print(e)

def web_request_mods(message, url, args, i, footer):
    modname = args
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                dl = "**Most Downloaded:**\n"
                view = "**Most Viewed:**\n"
                rate = "**Most Rated:**\n"
                if modname is "":
                    message = dl
                html = BeautifulSoup(resp.content, 'html.parser')
                if "No Mods found." in str(resp.content):
                    return [message, footer]
                for a in html.findAll('a', attrs={'href': re.compile("^https://")}):
                    if a.get('href').startswith("https://modworkshop.net/mydownloads.php?action=view_down&did="):
                        mod = a.text.replace('\n', '').replace('\r', '')
                        if modname is not "":
                            if i is 0:
                                i = 1
                            if modname.lower() in mod.lower():
                                r = requests.get(a.get('href'))
                                key = "Last Updated: "
                                date = "".join([x.strip() for x in (str(r.content)[str(r.content).find(key)+len(key):str(r.content).find(key)+len(key)+10].split('-'))])
                                if date.isnumeric():
                                    date = int(date[len(date)-4:len(date)]+date[0:len(date)-4])
                                else:
                                    date = 99999999
                                addendum = "[" + mod + "](" + a.get('href') + ")\n"
                                if len(message + addendum) <= 2000 and addendum not in message:
                                    if date > 20180719:
                                        message += addendum
                                    else:
                                        footer = "Pre-AG&D mod(s) hidden."
                        else:
                            if mod is not '':
                                addendum = "["+mod+"]("+a.get('href')+")\n"
                                if len(message+addendum) <= 2000:
                                    message += addendum
                            i += 1
                            if i == 5:
                                message += view
                            elif i == 10:
                                message += rate
                            elif i == 15:
                                break
                if modname is not "":
                    i += 1
                    message = web_request_mods(message, url[:-len(str(i - 1))] + str(i), args, i, footer)
                    footer = message[1]
                    message = message[0]
                    if message is "":
                        message += "No results found! Try narrowing your search criteria.\n"
                message = message[:2000]
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} :\n{1}'.format(url, str(e)))
        return None
    #message = "".join(message)
    return [message, footer]

client.loop.create_task(list_servers())
client.run(TOKEN)