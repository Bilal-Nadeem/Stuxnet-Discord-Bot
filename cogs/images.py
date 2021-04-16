import discord
from discord.ext import commands
import aiohttp
from PIL import Image
from io import BytesIO
import random
from global_functions import prefix, em, embed_color


class Images(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def meme(self, ctx):

	    async with aiohttp.ClientSession() as session:
	        async with session.get('https://some-random-api.ml/meme') as r:
	            r = await r.json()
	            imgurl = r['image']
	    embed = discord.Embed(colour=embed_color)
	    embed.set_image(url=imgurl)
	    await ctx.send(embed=embed)


	@commands.command()
	async def wanted(self, ctx, user: discord.Member = None):
	    if user == None:
	        user = ctx.author

	    wanted = Image.open('wanted.jpg')

	    av_url = user.avatar_url_as(size=128)
	    data = BytesIO(await av_url.read())
	    av = Image.open(data)
	    av = av.resize((177, 177))
	    wanted.paste(av, (120, 212))
	    wanted.save('av.jpg')
	    await ctx.send(file=discord.File('av.jpg'))


	@commands.command()
	async def slap(self, ctx, user: discord.Member = None):
	    if user == None:
	        user = ctx.author

	    slap = Image.open('slap.jpg')

	    av_url = user.avatar_url_as(size=128)
	    data = BytesIO(await av_url.read())
	    av = Image.open(data)
	    av = av.resize((200, 200))
	    slap.paste(av, (92, 278))
	    slap.save('av.jpg')
	    await ctx.send(file=discord.File('av.jpg'))

	@commands.command()
	async def av(self, ctx, *,  avamember: discord.Member=None):
	    global embed_color

	    if avamember == None:
	        avamember = ctx.author
	    userAvatarUrl = avamember.avatar_url

	    embed = discord.Embed(color=embed_color)
	    embed.set_author(name=avamember.display_name, icon_url=userAvatarUrl)
	    embed.set_image(url=userAvatarUrl)
	    await ctx.send(embed=embed)


	@commands.command()
	async def img(self, ctx, *, m):
	    global p
	    search = m
	    url = 'https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI'
	    querystring = {"q":m,"pageNumber":"1","pageSize":"10","autoCorrect":"true"}
	    headers = {
	    'x-rapidapi-key': "3f1e388716msh65e428495fb4fc7p1107ebjsne523fc561130",
	    'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
	    }
	    async with aiohttp.ClientSession() as session:
	        async with session.get(url, params=querystring, headers=headers) as r:
	            j = await r.json()
	            val = j['value']
	            ran = random.randint(0, len(val))
	            imgurl = val[ran]['url']
	    embed = discord.Embed(colour=discord.Colour.red())
	    embed.set_image(url=imgurl)
	    await ctx.send(embed=embed)


def setup(client):
	client.add_cog(Images(client))