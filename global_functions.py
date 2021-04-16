import discord
import aiohttp
import re


embed_color = discord.Color.blue() 
prefix = '.'
key = 'AIzaSyCkx - pQ2BBOq3pamBsv90t20Dt4DIbEaxY'


async def em(ctx, text, r=False):
    embed = discord.Embed(title=text, color=embed_color)
    if r == False:
        await ctx.send(embed=embed)
    else:
        return embed


async def r(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            t = await r.json()
            t = t['items'][0]['id']['videoId']
    link = f'https://www.youtube.com/watch?v={t}'
    return link

async def fe(ctx, emn):
    if type(emn) == str:
        if ':' in emn:
            emn = emn[1:-1]

        for _ in ctx.guild.emojis:
            if _.name == emn:
                a = _

        return str(a)

tof = re.compile(r':\w+:')

async def get_emo(ctx, m):
    global tof
    l = list(set(tof.findall(m)))
    if len(l) > 0:
        for _ in l:
            m = m.replace(_, await fe(ctx, _))

    return m