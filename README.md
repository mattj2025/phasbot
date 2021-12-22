# phasbot

A discord bot to assist you when playing phasmophobia.
<br>
<br>
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
## Bot Commands

- ```?help``` - shows commands

- ```?info``` - shows a list of ghosts to select to see details about or type a ghost after instead(ex: ?info banshee)

- ```?evidence``` - shows list of all evidences for you to select and then shows possible ghosts

- ```?map``` - shows a list of maps to select to see details and maps or type a map's name after instead(ex: ?info prison)
