import discord
from discord.ext import commands
import creds
import rps



bot = discord.ext.commands.Bot(command_prefix = '')

rps_channel_id = 991569860154904627


@bot.event
async def on_message(message):
    if message.channel.id == rps_channel_id:
        response = rps.get_response_string_from_guess(message.author.name, message.content.lower().strip())
        if response:
            await message.channel.send(response, reference=message)


bot.run(creds.token)