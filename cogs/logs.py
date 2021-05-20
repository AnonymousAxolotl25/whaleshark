import discord
from discord.ext import commands


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def logs(self, ctx, log_type='', toggle=''):
        log_type = log_type.lower()
        toggle = toggle.lower()
        embed = discord.Embed()

        if log_type == '':
            embed.color = 0x03A9F4
            embed.description = 'What logging do you want to configure?\nSyntax: `logs <message/member/invite> [enable/disable]`'
            await ctx.reply(embed=embed)
            return
        elif log_type in {'member', 'invite'}:
            embed.color = 0x673AB7
            embed.description = f'Oops, I don\'t support {log_type} logging yet.'
            await ctx.reply(embed=embed)
            return
        elif not log_type in {'message', 'member', 'invite'}:
            embed.color = 0xF44336
            embed.description = 'I don\'t recognize the log type you specified.\nSyntax: `logs <message/member/invite> [enable/disable]`'
            await ctx.reply(embed=embed)
            return

        if not ctx.author.guild_permissions.ban_members:
            embed.color = 0xF44336
            embed.description = f'You do not have permission to configure logging, {ctx.author.mention}.'
            await ctx.reply(embed=embed)
            return
        elif toggle == 'on':
            toggle = 'enable'
        elif toggle == 'off':
            toggle = 'disable'
        elif not toggle in {'', 'enable', 'disable'}:
            embed.color = 0xF44336
            embed.description = f'Enable or disable? I don\'t know what "{toggle}" means.\nSyntax: `logs <message/member/invite> [enable/disable]`'
            await ctx.reply(embed=embed)
            return

        if f'cogs.{log_type}-logging' in self.bot.extensions:
            if toggle == '':
                embed.color = 0x03A9F4
                embed.description = f'{log_type.title()} logging is currently enabled.'
            elif toggle == 'enable':
                embed.color = 0xe67e22
                embed.description = f'{log_type.title()} logging is already enabled.'
            elif toggle == 'disable':
                self.bot.unload_extension(f'cogs.{log_type}-logging')
                embed.color = 0xc0392b
                embed.description = f'Disabled {log_type} logging.'
        else:
            if toggle == '':
                embed.color = 0x03A9F4
                embed.description = f'{log_type.title()} logging is currently disabled.'
            elif toggle == 'disable':
                embed.color = 0xe67e22
                embed.description = f'{log_type.title()} logging is already disabled.'
            elif toggle == 'enable':
                self.bot.load_extension(f'cogs.{log_type}-logging')
                embed.color = 0x27ae60
                embed.description = f'Enabled {log_type} logging.'

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Logs(bot))
