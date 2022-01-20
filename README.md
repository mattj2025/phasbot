# phasbot

A discord bot to assist you when playing phasmophobia.

### [Add phasbot to your server here!](https://discord.com/oauth2/authorize?client_id=914221450586644481&scope=bot)

### [Test phasbot here!](https://discord.gg/U2nckekKW8)

## Bot Commands

- ```?help``` - shows commands

- ```?info [ghost name]``` - shows a list of ghosts to select to see details about it, or type a ghost after instead (ex: ?info banshee)

- ```?evidence``` - shows list of all evidences for you to select and then shows possible ghosts

- ```?map [map name]``` - shows a list of maps to select to see details and maps, or type a map's name after instead (ex: ?info prison)


## Get Started
1. Clone the repository
```
git clone https://github.com/SavageMeatballz/phasbot.git
```
2. Install dependencies
```
pip install discord.py discord-components python-dotenv pymongo pymongo[srv]
```
3. Add a ```.env``` file to the root directory of the repository with the following properties:
```
DISCORD_TOKEN=<insert Discord bot token here>
DATABASE_URI=<insert MongoDB URI here> 
```
4. Run the bot!
```
python bot.py
```

