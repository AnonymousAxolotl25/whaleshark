import os
import random
import datetime
import discord
from discord.ext import commands


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['docs', 'commands'])
    @commands.guild_only()
    async def help(self, ctx):
        embed = discord.Embed(color=0x2C2F33)
        embed.description = '`ping`, `info`, `say`, `poll`, `logs`, `shutdown`, `restart`'
        if ctx.message.content.startswith(f'<@!{self.bot.user.id}>'):
            embed.set_footer(
                text='You can also summon me with the prefix \'ws\'')
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        await ctx.reply(f'\🏓 `{ping}ms`')
        if ping < 100:
            messages = ['you underestimate me', 'full throttle', 'running like the wind',
                        'warp speed', 'warp speed', 'vroom', '299,792,458 m/s']
            await ctx.send(f'~~{random.choice(messages)}~~', delete_after=0.2)

    @commands.command()
    @commands.guild_only()
    async def info(self, ctx):
        embed = discord.Embed(color=0x2C2F33)
        embed.description = 'Hello! I\'m WhaleShark, a private bot created by <@273212712698249216>.'
        await ctx.send(embed=embed)
        await ctx.send('<:whaleshark:838131079965048864><:says:838264594869911562>')

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def shutdown(self, ctx):
        await ctx.reply(f'\❌ Shutdown requested')
        embed = discord.Embed(color=0x2ecc71, description='🥀',
                              timestamp=datetime.datetime.utcnow())
        await self.bot.get_channel(int(os.getenv('LOG_CHANNEL'))).send(embed=embed)
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def restart(self, ctx):
        await ctx.reply(f'\🔄 Restart requested')
        embed = discord.Embed(color=0x2ecc71, description='🥀',
                              timestamp=datetime.datetime.utcnow())
        await self.bot.get_channel(int(os.getenv('LOG_CHANNEL'))).send(embed=embed)
        await self.bot.close()
        quit()

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def error(self, ctx):
        raise discord.DiscordException


def setup(bot):
    bot.add_cog(General(bot))
