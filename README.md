# ETG Discord Bot
## What does it do?
Currently, the bot has the capability to search the ETG mod workshop for mods. 

## What are the commands?
The prefix for the bot is `etg:` or `etg!`. Here is a full list of commands and their descriptions:
* mods (aliases: mod, modlist, mod_list) -- displays a list of mods from the mod workshop which match the search criteria.

## I get an error when I run it
1. Make sure you have put your bot's token in the TOKEN variable in Discord.py.
2. Check to see if you have discord.py installed; if you don't, run the command `python -m pip install -U discord.py`
3. Check to see if you have BeautifulSoup installed; if you don't, run the command `pip install beautifulsoup4`
4. Check to see if you have requests installed; if you don't, run the command `pip install requests`
5. The discord.py API is not compatible with Python 3.7, make sure you are using an earlier version of Python.