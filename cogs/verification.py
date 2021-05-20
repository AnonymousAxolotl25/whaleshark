import os
import random
import datetime
import discord
from discord.ext import commands

class Verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.verify_url = ('https://discord.com/api/oauth2/authorize?response_type=code&client_id=533382783427674152' +
                           '&scope=identify%20email%20connections%20guilds&redirect_uri=https%3A%2F%2Fwhaleshark.glitch.me%2F&prompt=consent')

    @commands.command()
    @commands.guild_only()
    async def check(self, ctx):
        embed = discord.Embed(color=0x72A6CE)

        if False:
            embed.color = 0x2ecc71
            embed.description = f'You\'re verified, {ctx.author.mention}.'
        else:
            embed.description = (f'You\'re not currently verified, {ctx.author.mention}.\n' +
                                 f'Ask <@273212712698249216> to whitelist your account or [verify yourself]({self.verify_url}).')

        string = 'henlo'
        string = self.bot.users.find_one({'_id': ctx.author.id})
        embed.description = str(string)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def verify(self, ctx):
        embed = discord.Embed(color=0x72A6CE)
        embed.description = f'Ask <@273212712698249216> to whitelist your account or [verify yourself]({self.verify_url}).'
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Verification(bot))
