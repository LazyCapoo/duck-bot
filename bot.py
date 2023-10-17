import disnake as disnake
from disnake.ext import commands
from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config["BOT_TOKEN"]

command_sync_flags = commands.CommandSyncFlags.none()
command_sync_flags.sync_commands_debug = False
activity = disnake.Game(name="yeat's music")
bot = commands.Bot(
    command_prefix='.',
    sync_commands_debug=True,
    activity=activity,
    test_guilds=[1161052331882856498]
)

bot.load_extension("cogs.emotion")


bot.run(TOKEN)
