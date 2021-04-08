import discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
import random
from gtts import gTTS
from bs4 import BeautifulSoup

# gonna add things like showing which song currently playing, status stuff like that
# moderation commands tommorow


prefix = '.'
embed_color = discord.Color.blue()

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

key = 'AIzaSyCkx - pQ2BBOq3pamBsv90t20Dt4DIbEaxY'

async def r(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            t = await r.json()
            t = t['items'][0]['id']['videoId']
    link = f'https://www.youtube.com/watch?v={t}'
    return link


async def em(ctx, text, r=False):
    global embed_color
    embed = discord.Embed(title=text, color=embed_color)
    if r == False:
        await ctx.send(embed=embed)
    else:
        return embed


@client.event
async def on_ready():
    global prefix
    await client.change_presence(activity=discord.Game(f'{prefix}help'))
    print(f'Logged in as {client.user}')

@client.event
async def on_member_join(member):
    if not member.bot:
        guild = client.get_guild(829709301630369862)
        role = get(guild.roles, name="unverified")
        channel = client.get_channel(829709301630369865)
        embed = discord.Embed(title="Welcome To StuxNet!",description=f"Make sure to check out ***self-roles*** <@!{member.id}>", color=discord.Color.blurple()) # Let's make an embed!
        await channel.send(embed=embed)
        channel = client.get_channel(829800785084284979)
        embed = discord.Embed(title="Welcome To StuxNet!",description=f"Make sure to check out ***self-roles*** <@!{member.id}>", color=discord.Color.blurple()) # Let's make an embed!
        await channel.send(embed=embed)

        await member.add_roles(role)
        
    else:
        guild = client.get_guild(829709301630369862)
        role = get(guild.roles, name="Bots")
        await member.add_roles(role)

emojis = {
    '👶': '👶 13-',
    '🧑': '🧑 13+',
    '👦': '👦 18+',
    '🇵🇰': '🇵🇰 Pakistan',
    '🚫': '🚫 Not Pakistan',
    '♂️': '♂️ Male',
    '♀️': '♀️ Female',
    '❤️': '❤️ Red',
    '🧡': '🧡 Orange',
    '💛': '💛 Yellow',
    '💚': '💚 Green',
    '💙': '💙 Blue',
    '💜': '💜 Purple',
    '🖤': '🖤 Black',
    '🤎': '🤎 Brown',
    '🤍': '🤍 White',
    '☑️': 'members'
}

@client.event
async def on_raw_reaction_add(payload):
    global emojis
    if payload.channel_id in (829745111109337088, 829745133913636894, 829793396335444059):
        guild = client.get_guild(payload.guild_id)
        e = payload.emoji.name
        
        if e == '☑️':
            role = get(guild.roles, name="unverified")
            await payload.member.remove_roles(role)

        a = emojis[e]
        role = get(guild.roles, name=a)
        await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    global emojis
    if payload.channel_id in (829745111109337088, 829745133913636894, 829793396335444059):
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        e = payload.emoji.name

        if e == '☑️':
            role = get(guild.roles, name="unverified")
            await member.add_roles(role)

        a = emojis[e]
        role = get(guild.roles, name=a)
        await member.remove_roles(role)




@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command()
async def help(ctx):
    global prefix, embed_color
    embed = discord.Embed(
        title='Currently There are these commands:',
        color=embed_color
    )
    embed.set_author(name='Help!', icon_url=ctx.author.avatar_url)
    embed.add_field(name=f'{prefix}play or {prefix}p', value='Plays a song')
    embed.add_field(name=f'{prefix}pause', value='Pauses a song')
    embed.add_field(name=f'{prefix}resume', value='Resumes a song')
    embed.add_field(
        name=f'{prefix}stop or {prefix}skip or {prefix}s', value='stops/skips a song')
    embed.add_field(name=f'{prefix}leave {prefix}l',
                    value='leaves the voice channel')
    embed.add_field(name=f'{prefix}say',value='new text to speech feature', inline = False)
    # embed.add_field(name=f'{prefix}change_prefix', value='Change bot prefix')
    # embed.add_field(name=f'{prefix}change_embed', value='Change embed color')
    # embed.add_field(name=f'{prefix}Application or {prefix}apply',
    #                 value='You\'ll be asked certain question in dms, answer those and application will be')
    # embed.add_field(name=f'{prefix}accept @user',
    #                 value='Accept someones application (can only be used by administrators')
    embed.add_field(name=f'{prefix}purge',value=f'purges n amount of messages\nExample: {prefix}purge 10', inline = False)
    embed.add_field(name=f'{prefix}poll', value='make a poll')
    embed.add_field(name=f'{prefix}av', value='Check someones avatar', inline=False)
    embed.add_field(name=f'{prefix}wanted', value='shows wanted image with user av', inline=False)
    embed.add_field(name=f'{prefix}slap', value='slap some user', inline=False)
    embed.add_field(name=f'{prefix}meme', value='show a random meme', inline=False)
    embed.add_field(name=f'{prefix}userinfo/whois', value='check user info', inline=False)
    embed.add_field(name=f'{prefix}idinfo', value='check user info', inline=False)
    embed.add_field(name=f'{prefix}ping', value='shows ping in milli seconds', inline = False)
    embed.add_field(name=f'{prefix}img',value='search an image', inline = False)
    embed.add_field(name=f'{prefix}emojify',value='emojify some letters', inline = False)
    embed.add_field(name=f'{prefix}covid_countries',value='check countries avialble for search in covid_stats. --covid_countries 1', inline = False)
    embed.add_field(name=f'{prefix}covid_stats',value=f'search covid stats for a specefic country, by default will give pakistans result. {prefix}covid_stats russia', inline = False)
    embed.add_field(name=f'{prefix}covid_pakistan_stats',value='***VERY DETAILED PAKISTAN COVID STATS***', inline = False)
    await ctx.send(embed=embed)


@client.command(aliases=['p'])
async def play(ctx, *, video_link):
    global key, embed_color

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
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if not voice.is_playing():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=False)
        URL = info['formats'][0]['url']
        embed = discord.Embed(title='Playing!', color=embed_color)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name='Link:', value=video_link)
        await ctx.send(embed=embed)

        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        # print(voice.is_playing())
    else:
        await em(ctx, "Already playing song, currently i dont support queues")
        return


# @client.command()
# async def change_prefix(ctx, cprefix):
#     global prefix
#     prefix = cprefix


# @client.command()
# async def change_embed_color(ctx, cembed):
#     global embed_color
#     embed_color = cembed


@client.command()
async def pause(ctx):
    voice = ctx.guild.voice_client
    await voice.pause()


@client.command()
async def resume(ctx):
    voice = ctx.guild.voice_client
    await voice.resume()


@client.command(aliases=['s', 'skip'])
async def stop(ctx):
    voice = ctx.guild.voice_client
    await voice.stop()


@client.command(aliases=['l'])
async def leave(ctx):
    v = ctx.guild.voice_client
    await v.disconnect()


@client.command()
async def poll(ctx, *, message=None):
    global embed_color

    if message == None:
        await em(ctx, "Please provide some text")
    else:
        embed = discord.Embed(title=message, color=embed_color)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        m = await ctx.send(embed=embed)
        await m.add_reaction('👍')
        await m.add_reaction('👎')


@client.command()
async def av(ctx, *,  avamember: discord.Member=None):
    global embed_color

    if avamember == None:
        avamember = ctx.author
    userAvatarUrl = avamember.avatar_url

    embed = discord.Embed(color=embed_color)
    embed.set_author(name=avamember.display_name, icon_url=userAvatarUrl)
    embed.set_image(url=userAvatarUrl)
    await ctx.send(embed=embed)


@client.command()
async def meme(ctx):
    global embed_color

    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/meme') as r:
            r = await r.json()
            imgurl = r['image']
    embed = discord.Embed(colour=embed_color)
    embed.set_image(url=imgurl)
    await ctx.send(embed=embed)


@client.command()
async def wanted(ctx, user: discord.Member = None):
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


@client.command()
async def slap(ctx, user: discord.Member = None):
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


@client.command(aliases=["whois", ])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    embed = discord.Embed(colour=embed_color, timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)
    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    await ctx.send(embed=embed)

@client.command()
async def idinfo(ctx, user_id):
    global embed_color
    member = await client.fetch_user(user_id)
    embed = discord.Embed(colour=embed_color, timestamp=ctx.message.created_at,
    title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)
    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    await ctx.send(embed=embed)


# @client.command()
# async def accept(ctx, user: discord.Member = None):
#     global embed_color
#     if ctx.message.author.guild_permissions.administrator:
#         channel = client.get_channel(816286236457041966)
#         embed = discord.Embed(
#             title='Application Accepted!',
#             description=f'<@!{user.id}> Your Application Has Been Accepted Contact Ceo For Role',
#             color=embed_color
#         )
#         await channel.send(embed=embed)
#     else:
#         await em(ctx, 'You Dont Have Perms!')


@client.command()
async def purge(ctx, num=1):
    global embed_color
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        if num < 1000:
            a = await ctx.channel.purge(limit=num)
            embed = discord.Embed(title='Deleted {} message(s)'.format(
                len(a)), color=embed_color)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

        else:
            await em(ctx, 'Max 999 messages can be deleted at a time')
    else:
        await em(ctx, 'You dont have perms!')




@client.command()
async def img(ctx, *, m):
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


# q_list = [
#     'How much Experience do you have on discord?',
#     'For how much time can you be active in the server and chat?',
#     'You must use our tag on your name. [ !🅵🆉YOUR NAME ]',
#     'How will you handle abuse raid in the server?'
# ]

# a_list = []


# @client.command(aliases=['apply'])
# async def application(ctx):

#     global embed_color

#     a_list = []
#     submit_channel = client.get_channel(810284722059870228)
#     channel = await ctx.author.create_dm()

#     await ctx.send(embed=await em(ctx, 'Application has been started Check Dm', r=True))

#     def check(m):
#         return m.content is not None and m.channel == channel and m.author.id != 814881819849392138

#     for question in q_list:
#         question = await em(ctx, question, r=True)
#         await channel.send(embed=question)
#         try:
#             msg = await client.wait_for('message', timeout=60.0, check=check)
#         except asyncio.TimeoutError:
#             await channel.send(embed=await em(ctx, 'Timeout, You didnt reply in 60 seconds', r=True))
#             return
#         a_list.append(msg.content)

#     await channel.send(embed=await em(ctx, 'End of questions - say "yes" to finish/submit it or "no" to leave it.', r=True))

#     try:
#         msg = await client.wait_for('message', timeout=60.0, check=check)
#     except asyncio.TimeoutError:
#         await channel.send(embed=await em(ctx, 'Timeout, You didnt reply in 60 seconds', r=True))
#         return

#     if "yes" in msg.content.lower():
#         embed = discord.Embed(
#             title='Application By:',
#             description=f'<@!{ctx.author.id}>',
#             color=embed_color
#         )
#         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

#         for n, answer in enumerate(a_list):
#             embed.add_field(name=f'{q_list[n]}',
#                             value=f'{answer}', inline=False)

#         await submit_channel.send(embed=embed)

#         embed = await em(ctx, 'Your application has been sent successfully!', r=True)
#         await channel.send(embed=embed)

#     elif "no" in msg.content.lower():
#         embed = await em(ctx, 'Discarded successfully', r=True)
#         await channel.send(embed=embed)

#     else:
#         embed = await em(ctx, 'You had to answer a yes or no, application wasn\'t sent!', r=True)
#         await channel.send(embed=embed)

@client.command()
async def emojify(ctx, *, msg):
    d = {
    "A": "🇦",
    "B": "🇧",
    "C": "🇨",
    "D": "🇩",
    "E": "🇪",
    "F": "🇫",
    "G": "🇬",
    "H": "🇭",
    "I": "🇮",
    "J": "🇯",
    "K": "🇰",
    "L": "🇱",
    "M": "🇲",
    "N": "🇳",
    "O": "🇴",
    "P": "🇵",
    "Q": "🇶",
    "R": "🇷",
    "S": "🇸",
    "T": "🇹",
    "U": "🇺",
    "V": "🇻",
    "W": "🇼",
    "X": "🇽",
    "Y": "🇾",
    "Z": "🇿",
    " ": "  "
    }
    msg = msg.upper()
    print(msg)
    l = []
    s = ''
    for m in msg:
        try:
            l.append(d[m] + '|')
        except:
            s = '***Only Letters***'
            break
    if s:
        await ctx.send(s)
    else:
        l = ''.join(l)
        await ctx.send(l)


@client.command()
async def say(ctx, *, text):
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


@client.command()
async def covid_stats(ctx, country='pakistan'):

    global embed_color

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



@client.command()
async def covid_countries(ctx, page=1):
    with open('countries.txt', 'r') as f:
        r = f.read()

    r = r.split('\n')

    a = "\n".join(r[((50*page)-50):(50*page)])
    if page >= 1 and page <= 5:
        a += f'\n\nPage: {page} out of 5'
        await ctx.send(f'```Ranked By Highest Number of Cases\n\n{a}```')
    else:
        await em(ctx, 'Only 5 pages')



@client.command()
async def covid_pakistan_stats(ctx, page=1):
    global embed_color

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


@client.command()
async def nick_all(ctx, *, n):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        for m in ctx.guild.members:
            try:
                await m.edit(nick=n)
            except:
                continue

        await ctx.send('***Done***')



@client.command()
async def reset_nick_all(ctx):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        for m in ctx.guild.members:
            try:
                await m.edit(nick="")
            except:
                continue

        await ctx.send('***Done***')


@client.command()
async def kick(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        try:
            await member.kick()
            await em(ctx, f'{member.name} was kicked')
        except:
            await em(ctx, f'I am not able to kick {member.name}')


@client.command()
async def ban(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        try:
            await member.ban()
            await em(ctx, f'{member.name} was banned')
        except:
            await em(ctx, f'I am not able to ban {member.name}')


@client.command()
async def create_role_menu(ctx, *, m):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        await ctx.send(m)

@client.command()
async def create_embed(ctx, *, m):
    global embed_color
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        await em(ctx, m)

@client.command()
async def add_reaction(ctx, m_id, *, r):
    global embed_color

    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:

        r = r.split(' ')

        msg = await ctx.fetch_message(m_id)
        for _ in r:
            await msg.add_reaction(_)
        
        await em(ctx, 'Done')


@client.command()
async def create_role(ctx, *, rname):
    # a,b,c = [int(_) for _ in str(color).split(',')]
    # if color.lower() != 'n':
    #     await ctx.guild.create_role(name=rname, color=discord.Color.from_rgb(a,b,c))
    # else:
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        await ctx.guild.create_role(name=rname)


@client.command()
async def chperms(ctx):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)





client.run('ODI5NzM5MDQyNjU1Njk4OTY1.YG8gsw.ZwZywjA43Dwnv4ckuaoZFlri-wY')