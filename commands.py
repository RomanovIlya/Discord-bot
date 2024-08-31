from discord.ext import commands
from main import bot
from discord.utils import get
from youtube_dl import YoutubeDL
import discord
import asyncio

YDL_OPTIONS={'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True','preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

#command clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx,messages=100):
    await ctx.channel.purge(limit=messages+1)

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason==None:
        reason="того захотелось"
    await ctx.guild.kick(member)
    await ctx.send(f'Пользователь {member.mention} был выгнан из-за {reason}')

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, user: discord.Member, time: int,*, reason):
    role = user.guild.get_role()#Role ID
    channel=bot.get_channel()#Chanel ID
    emb = discord.Embed( title = '✅Получилось', description=f"Пользователю {user} выдали мут!\nВремя пробывания в муте: {time} минут\nПричина выдачи мута: {reason}!", colour = discord.Color.green())
    emb.set_footer(text = 'Действие выполнено админом - ' + ctx.author.name)

    await channel.send( embed = emb)
    await user.add_roles(role) #выдает мьют роль
    await asyncio.sleep(time * 60) #ждет нужное кол-во секунд умноженных на 60(вы выдаете мут на минуты. Допустим time = 10, то вы выдали мут на 10 минут)
    await user.remove_roles(role) #снимает мьют роль
    await user.send(embed=discord.Embed(title="✅Вернитесь в строй", description="С вас был снят мут", colour=discord.Color.green()))


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user: discord.Member, time: int,*, reason): 
    channel=bot.get_channel()#Chanel ID
    emb = discord.Embed( title = '✅Получилось', description=f"Пользователю {user} выдали бан!\nВремя пробывания в бане: {time} минут\nПричина выдачи бана: {reason}!", colour = discord.Color.green())
    emb.set_footer(text = 'Действие выполнено админом - ' + ctx.author.name)
    await channel.send(embed = emb)
    await user.guild.ban(user) 
    await asyncio.sleep(time * 60)
    await user.guild.unban(user)

@bot.command()
async def join(ctx):
    global voice
    channel=ctx.message.author.voice.channel
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice=await channel.connect()
        await ctx.send(f"Я с вами🥱")   

@bot.command()
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice: 
        await voice.disconnect()
        await ctx.send("Я ливнул😑")
    else: 
        await ctx.send("Меня и так нет🙄")

@bot.command()
async def play(ctx,url):
    vc=await ctx.author.voice.channel.connect()
    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://'in url:
            info=ydl.extract_info(url,download=False)
        else:
            info=ydl.extract_info(f'ytsearch:{url}',download=False)['entries'][0]

    url = info['formats'][0]['url']
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))

