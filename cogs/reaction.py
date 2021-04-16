import discord
from discord.ext import commands
from discord.utils import get
from global_functions import prefix, em


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

class Reaction(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global emojis
        if payload.channel_id in (829745111109337088, 829745133913636894, 829793396335444059):
            guild = self.client.get_guild(payload.guild_id)
            e = payload.emoji.name
            
            if e == '☑️':
                role = get(guild.roles, name="unverified")
                await payload.member.remove_roles(role)

            a = emojis[e]
            role = get(guild.roles, name=a)
            await payload.member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global emojis
        if payload.channel_id in (829745111109337088, 829745133913636894, 829793396335444059):
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            e = payload.emoji.name

            if e == '☑️':
                role = get(guild.roles, name="unverified")
                await member.add_roles(role)

            a = emojis[e]
            role = get(guild.roles, name=a)
            await member.remove_roles(role)

def setup(client):
    client.add_cog(Reaction(client))

