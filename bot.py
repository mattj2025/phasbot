# bot.py
import os
import re
import discord
from discord_components import interaction
from pymongo import MongoClient, collection
from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_components.interaction import Interaction
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_URI = os.getenv('DATABASE_URI')

client = MongoClient(DB_URI)
db = client["PhasbotDB"]

ghost_collection = db["GhostInfo"]
map_collection = db["MapInfo"]

evidences = ['Ghost Orb', 'Spirit Box', 'EMF Level 5', 'Fingerprints', 'Ghost Writing', 'D.O.T.S Projector', 'Freezing Temperatures']

bot = discord.ext.commands.Bot("?")
DiscordComponents(bot)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


@bot.command(name="info", description="Returns info about a certain ghost.", brief="Returns info about ghosts.")
async def info(ctx, arg = None):
    if arg is not None:
        try:
            ghostinfo = ghost_collection.find_one({ "name": arg })
            msginfo = "__**{}**__\n\n\t**Description:** `{}`\n\n\t**Strength:** `{}`\n\t**Weakness:** `{}`\n\n\t**Evidences:**\n".format(ghostinfo["name"].capitalize(), ghostinfo["about"], ghostinfo["strength"], ghostinfo["weakness"])
            for evidence in ghostinfo["evidence"]:
                msginfo += f"\t\t- `{evidence}`\n"
            await ctx.send(msginfo)
        except Exception as e:
            print(e)
            await ctx.send("I couldn't access the database.")
    else:
        # Retrieve ghost info from database
        ghosts = ghost_collection.find()
        await ctx.send(
            "Choose from one of these:",
            components = [
                Select(
                    placeholder = "Select something!",
                    # Generate select options based on the ghosts in database
                    options=[
                        SelectOption(
                            label=ghost['name'].capitalize(), value=ghost['name']
                        )
                        for ghost in ghosts
                    ],
                )
            ]
        )  
        
        interaction = await bot.wait_for("select_option")
        await interaction.send(content = "Loading")
        await info(ctx, interaction.values[0])


@bot.command(name="evidence", description="Asks for evidence and then returns information about possible ghosts.", brief="Input evidence for possible ghosts")
async def evidence(ctx, detailed = None):
    await ctx.send(
        "What evidence do you have?",
        components = [
            Select(
                placeholder = "Select something!",
                # Generate select options based on list of evidences
                options=[
                    SelectOption(
                        label=evidence, value=evidence
                    )
                    for evidence in evidences
                ],
                min_values = 1,
                max_values = 3
            )    
        ]
    )
    interaction = await bot.wait_for("select_option")
    await interaction.send(content = "Loading...")
    ghosts = ghost_collection.find()

    selected_evidence = interaction.values
    print(selected_evidence)

    possible_evidence = []

    # Matched ghosts include the ghosts with evidences that contain all of the selected evidences
    for ghost in ghosts:
        if set(selected_evidence).issubset(ghost['evidence']):

            msgInfo = f"__**{ghost['name'].capitalize()}**__\n"
            
            # send more details about each matching ghost
            if detailed == "detailed":
                msgInfo += "\n\t**Description:** `{}`\n\n\t**Strength:** `{}`\n\t**Weakness:** `{}`\n\n".format(ghost["about"], ghost["strength"], ghost["weakness"])
            
            msgInfo += "\t**Evidences:**\n"

            for evidence in ghost['evidence']:
                msgInfo += f"\t\t- `{evidence}`\n"

                if (evidence not in selected_evidence) and (evidence not in possible_evidence):
                    possible_evidence.append(evidence)                
                
            await ctx.send(msgInfo)
    
    msg = f'___Possible Remaining Evidence___: **{ ", ".join(possible_evidence) }**'
    await ctx.send(msg)
    
    
@bot.command(name="map", description="Displays map and shows info about each map.", brief="Displays map")
async def map(ctx, arg = None):
    if arg is not None:
        try:
            regex = re.compile(f".*{arg}.*", re.IGNORECASE)
            mapInfo = map_collection.find_one({ "name": { "$regex": regex } })
            msginfo = "__**{}**__\n\n**Size:** {}\n\n**Map:** {}\n".format(mapInfo["name"].title(), mapInfo["size"].capitalize(), mapInfo["image"])
            await ctx.send(msginfo)
        except Exception as error:
            print(error)
            await ctx.send(f"I couldn't access the database.\nError: {error}")
    else:
        maps = map_collection.find()
        await ctx.send(
            "Choose from one of these:",
            components = [
                Select(
                    placeholder = "Select something!",
                    options=[
                        SelectOption(
                            label=place['name'].title(), value=place['name']
                        )
                        for place in maps
                    ],
                )
            ]
        )  
        
        interaction = await bot.wait_for("select_option")
        await interaction.send(content = "Loading")
        await map(ctx, interaction.values[0])

bot.run(TOKEN)