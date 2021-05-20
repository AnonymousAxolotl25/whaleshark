import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter
import datetime


class InviteLogging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.invite_log = Webhook.partial(
            834673574362087424, 'rIBsAQaLHgwJ4xDAREpWfFekxu0FSmiPcWbwkdpA43j1CBeN9QGEGi2ceN7kSmqpQ2kX', adapter=RequestsWebhookAdapter())

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        self.invite_log.send(f'{invite} created')

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        self.invite_log.send(f'{invite} deleted')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.invite_log.send(f'{member} joined')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.invite_log.send(f'{member} left')


def setup(bot):
    bot.add_cog(InviteLogging(bot))
