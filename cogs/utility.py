import random
import discord
from discord.ext import commands


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.verify_url = ('https://discord.com/api/oauth2/authorize?response_type=code&client_id=533382783427674152' +
                           '&scope=identify%20email%20connections%20guilds&redirect_uri=https%3A%2F%2Fwhaleshark.glitch.me%2F&prompt=consent')

    @commands.command(aliases=['says', 'speak'])
    @commands.guild_only()
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def say(self, ctx, *, args=''):
        embed = discord.Embed(color=0x72A6CE)

        if args == '':
            words = ['friendly', 'wholesome', 'positive', 'random', 'heavy', 'famous', 'strange', 'secret']
            embed.description = '\💬 **Say Command Syntax**\n```ws say <' + random.choice(words) + '-message-here>```'
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        elif True:
            embed.description = ('Sorry, this command is restricted to verified users.\n' +
                                 f'Ask <@273212712698249216> to whitelist your account or [verify yourself]({self.verify_url}).')
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        elif len(args) < 20 or len(args) > 300:
            await ctx.message.add_reaction('🦑')
            ctx.command.reset_cooldown(ctx)
            return

        embed = discord.Embed(color=0x2C2F33)
        embed.description = discord.utils.remove_markdown(
            args.replace('\n', ' '))
        await ctx.send(embed=embed)
        await ctx.send('<:whaleshark:838131079965048864><:says:838264594869911562>')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 300, commands.BucketType.user)
    async def poll(self, ctx, *, args=''):
        embed = discord.Embed(color=0x72A6CE)

        if args == '':
            embed.description = ('<:checkmark:733162472160100373> <:xmark:733162479143616522> **Yes/No Poll Syntax**\n```ws poll <question>```\n' +
                                 '1️⃣ 2️⃣ 3️⃣ **Multi-Option Poll Syntax**\n```ws poll <question> | [option1] | [option2] | ...```')
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        elif len(args) < 20 or len(args) > 1000:
            await ctx.message.add_reaction('🦑')
            return

        if not '|' in args:
            embed.description = '❓ **' + \
                discord.utils.remove_markdown(args.replace('\n', ' ')) + '**'
            embed.set_footer(
                text=f'Poll started by {ctx.author.name}#{ctx.author.discriminator}')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('<:checkmark:733162472160100373>')
            await msg.add_reaction('<:xmark:733162479143616522>')
            return

        options = args.replace('\n', ' ').split('|')
        if len(options) - 1 < 2:
            embed.description = 'A multi-option poll should have at least 2 options'
            msg = await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        elif len(options) - 1 > 10:
            embed.description = 'There is a maximum of 10 options for multi-option polls'
            msg = await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return

        embed.set_footer(
            text=f'Poll started by {ctx.author.name}#{ctx.author.discriminator}')
        embed.description = '❓ **' + options[0] + '**\n\n'

        emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣',
                  '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for i in range(1, len(options)):
            embed.description += f'> **{i}. ** {discord.utils.remove_markdown(options[i])}\n'

        msg = await ctx.send(embed=embed)

        for i in range(1, len(options)):
            await msg.add_reaction(emojis[i])


def setup(bot):
    bot.add_cog(Utility(bot))
