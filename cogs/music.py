import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from gtts import gTTS
from global_functions import prefix, em, r, key, embed_color


class Music(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.queue = []


	@commands.command(aliases=['p'])
	async def play(self, ctx, *, video_link):
		
		if video_link[:32] == 'https://www.youtube.com/watch?v=':
			pass
		else:
			query = video_link.replace(' ', '+')
			print(query)
			url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={key}'
			video_link = await r(url)

		try:
			vch = ctx.author.voice.channel
		except:
			await em(ctx, 'Please join a voice channel')
			return
		try:
			await vch.connect()
		except:
			pass

		voice = ctx.guild.voice_client

		ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True'}
		FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		if not voice.is_playing():
			with YoutubeDL(ydl_opts) as ydl:
				info = ydl.extract_info(video_link, download=False)
			URL = info['formats'][0]['url']
			duration = int(info['duration'])/60
			duration = f'{duration:.2f}min'
			thumbnail = info['thumbnail']
			title = info['title']
			embed = discord.Embed(title=title, color=embed_color, url=video_link)
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name='Duration:', value=duration)
			embed.set_thumbnail(url=thumbnail)
			await ctx.send(embed=embed)
			voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
			# print(voice.is_playing())
		else:
			await em(ctx, "Already playing song, currently i dont support queues")
			return

	@commands.command()
	async def pause(self, ctx):
		voice = ctx.guild.voice_client
		voice.pause()
		await em(ctx, 'Paused!')


	@commands.command()
	async def resume(self, ctx):
		voice = ctx.guild.voice_client
		voice.resume()
		await em(ctx, 'Resumed!')


	@commands.command(aliases=['s', 'skip'])
	async def stop(self, ctx):
		voice = ctx.guild.voice_client
		voice.stop()
		await em(ctx, 'Skipped!')


	@commands.command(aliases=['l'])
	async def leave(self, ctx):
		v = ctx.guild.voice_client
		await v.disconnect()
		await em(ctx, 'Left!')

	@commands.command()
	async def say(self, ctx, *, text):
	    """Plays a file from the local filesystem"""

	    try:
	        vch = ctx.author.voice.channel
	    except:
	        await em(ctx, 'Please join a voice channel')
	        return
	    try:
	        await vch.connect()
	    except:
	        pass

	    voice = ctx.guild.voice_client

	    if not voice.is_playing():
	        myobj = gTTS(text=text, lang='en', slow=False)
	        myobj.save("abc.mp3")

	        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("abc.mp3"))
	        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
	    else:
	        await em(ctx, "Already playing song, currently i dont support queues")
	        return





def setup(client):
	client.add_cog(Music(client))