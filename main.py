from discord.ext import commands
from config.read import read_token, read_bad
import discord

bot = discord.Client()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Имя бота:{bot.user.name}")

@bot.event
async def on_message(message):
    for i in range(0, len(read_bad("config/config.json"))):
        if read_bad("config/config.json")[i] in message.content.lower():
            await message.delete()
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MemberNotFound):
        channel=bot.get_channel()#Channel ID
        await channel.send(embed = discord.Embed(title="❌Не получилось",description="Такого пользователя нету на это сервере", colour=discord.Color.green()))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed = discord.Embed(title="❌Не получилось",description="Чел на это у тебя нет прав🙄, ты не админ", colour=discord.Color.green()))
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(embed = discord.Embed(title="❌Не получилось",description="Чел такой комманды нету. Иди лучше в майн поиграй😒", colour=discord.Color.green()))

# start
if __name__ == '__main__':
    from commands import bot
    bot.run(read_token("config/config.json"))
