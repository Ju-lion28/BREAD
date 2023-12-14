import json
import random
import disnake
import requests
from disnake.ext import commands

with open("secrets.json", "r") as open_file:
    secrets = json.load(open_file)

token = secrets["token"]
api_key = secrets["api_key"]



bot = commands.InteractionBot(
    command_sync_flags=commands.CommandSyncFlags.default(), reload=True
)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=disnake.Activity(type=disnake.ActivityType.listening, name="BREAD")
    )

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.slash_command(name="bread", description="Get a random bread gif.")
async def bread(ctx):
    response = requests.get(
        f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q=bread&limit=50&offset={random.randint(0, 100)}&rating=g&lang=en"
    )
    json_data = json.loads(response.text)
    url = json_data["data"][random.randint(0, 50)]["url"]

    await ctx.send(url)

    print(f"sent a gif: {ctx.guild.name} ({ctx.guild.id})")

    try:
        # Load the existing data again before updating
        with open("guildList.json", "r") as open_file:
            existing_data = json.load(open_file)
    except json.JSONDecodeError:
        # Handle the case where the file is empty or not in a valid JSON format
        existing_data = {}

    existing_data.update({ctx.guild.name: ctx.guild.id})

    # Write the updated data back to the file
    with open("guildList.json", 'w') as outfile:
        json.dump(existing_data, outfile, indent=3)

bot.run(token)
