import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
from global_functions import prefix, em, embed_color


class Covid(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def covid_countries(self, ctx, page=1):
	    with open('countries.txt', 'r') as f:
	        r = f.read()

	    r = r.split('\n')

	    a = "\n".join(r[((50*page)-50):(50*page)])
	    if page >= 1 and page <= 5:
	        a += f'\n\nPage: {page} out of 5'
	        await ctx.send(f'```Ranked By Highest Number of Cases\n\n{a}```')
	    else:
	        await em(ctx, 'Only 5 pages')

	@commands.command()
	async def covid_stats(self, ctx, country='pakistan'):

	    country = country.lower()

	    url = f'https://www.worldometers.info/coronavirus/country/{country}/'

	    try:

	        async with aiohttp.ClientSession() as session:
	            async with session.get(url) as r:
	                r = await r.text()

	        s = BeautifulSoup(r, 'lxml')

	        stats = [_.contents[-2].text.strip() for _ in s.findAll(id='maincounter-wrap')]

	        stats_dict = {
	            'Country': str(s.find(id='page-top').contents[-1])[3:],
	            'Coronavirus Cases': stats[0],
	            'Deaths': stats[1],
	            'Recovered': stats[2],
	            'Link': url
	        }

	        embed = discord.Embed(
	            title=f'Covid Stats:',
	            color=embed_color
	        )
	        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
	        embed.add_field(name='Country', value=stats_dict['Country'], inline=False)
	        embed.add_field(name='Coronavirus Cases', value=stats_dict['Coronavirus Cases'], inline=False)
	        embed.add_field(name='Deaths', value=stats_dict['Deaths'], inline=False)
	        embed.add_field(name='Recovered', value=stats_dict['Recovered'], inline=False)
	        embed.add_field(name='Link', value=stats_dict['Link'], inline=False)

	        await ctx.send(embed=embed)


	    except:
	        await em(ctx, 'Some Error Occured, Please check if you specefied the correct inputs like country name. To check all the avialable countries use --covid_countries command')

	@commands.command()
	async def covid_pakistan_stats(self, ctx, page=1):

	    async with aiohttp.ClientSession() as session:
	        async with session.get('https://covid.gov.pk') as r:
	            r = await r.text()
	    s = BeautifulSoup(r, 'lxml')

	    stats = {
	        'Cases':{
	            'total_cases': s.find(class_='tests').contents[1].contents[5].text,
	            'last_24_hours_cases': s.find(class_='tests').contents[3].contents[1].contents[1].text
	        },
	        'Deaths':{
	            'total_deaths': s.find(class_='deaths').contents[1].contents[5].text,
	            'last_24_hours_deaths': s.find(class_='deaths').contents[3].contents[1].contents[1].text
	        },
	        'Recovered':{
	            'total_recovered': s.find(class_='recovered').contents[1].contents[5].text,
	            'last_24_hours_recovered': s.find(class_='recovered').contents[3].contents[1].contents[1].text
	        },
	        'Tests':{
	            'total_tests': s.find(class_='active').contents[1].contents[5].text,
	            'last_24_hours_tests': s.find(class_='active').contents[3].contents[1].contents[1].text
	        },
	        'Critical':{
	            'total_critical': s.find(class_='total').contents[1].contents[5].text,
	            'last_24_hours_critical': s.find(class_='total').contents[3].contents[1].contents[1].text
	        }
	    }

	    p = s.findAll(class_='boxx')
	    provinces = {}
	    for _ in range(6):
	        if _ != 5:
	            provinces[p[_].contents[1].contents[3].text] = p[_].contents[1].contents[1].text
	        else:
	            provinces[p[_].contents[1].contents[3].text[:3]] = p[_].contents[1].contents[1].text[0:6]
	            provinces[p[_].contents[1].contents[3].text[4:]] = p[_].contents[1].contents[1].text[-5:]

	    skeys = ('Cases', 'Deaths', 'Recovered', 'Tests', 'Critical')
	    embed = discord.Embed(
	        title=f'Pakistan Covid Stats:',
	        color=embed_color
	    )
	    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

	    for _ in skeys:
	        l = _.lower()
	        t = f'total_{l}'
	        v = f'{t}: ***{stats[_][t]}***'

	        t2 = f'last_24_hours_{l}'
	        v2 =  f'{t2}: ***{stats[_][t2]}***'

	        embed.add_field(name=_, value=v + '\n' + v2, inline=False)


	    embed.add_field(name='Provincial Stats:', value='\u200b', inline=False)


	    for _ in provinces.keys():
	        embed.add_field(name=_, value=provinces[_])


	    await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Covid(client))
