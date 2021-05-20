import os
import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter
import datetime


class MessageLogging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.message_log = Webhook.partial(
            int(os.getenv('MESSAGE_LOG_WEBHOOK_ID')), os.getenv('MESSAGE_LOG_WEBHOOK_TOKEN'), adapter=RequestsWebhookAdapter())

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        if before.content == after.content:
            return

        embed = discord.Embed(
            color=0xf1c40f, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f'{before.author}',
                         icon_url=before.author.avatar_url)
        embed.description = f'**Before:** {before.content}\n** After:** {after.content}'
        embed.set_footer(
            text=f'Message Edited • #{before.channel} • {before.author.id}')

        self.message_log.send(embed=embed, username='WhaleShark Message Logging')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
    
        embed = discord.Embed(
            color=0xe74c3c, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f'{message.author}',
                         icon_url=message.author.avatar_url)
        embed.description = f'{message.content}'
        embed.set_footer(
            text=f'Message Deleted • #{message.channel} • {message.author.id}')

        if len(message.attachments) != 0:
            attachments = ''
            for i in message.attachments:
                url = str(i).replace('cdn.discordapp.com',
                                     'media.discordapp.net') if 'image' in i.content_type else str(i)
                attachments += f'[{i.filename} ({i.content_type})]({url})\n'
            embed.add_field(name='Attachments', value=attachments)
            embed.set_image(url=message.attachments[0])
            embed.color = 0x2980b9

        self.message_log.send(embed=embed, username='WhaleShark Message Logging')

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        channel = self.bot.get_channel(payload.channel_id)

        embed = discord.Embed(
            color=0x2d3436, timestamp=datetime.datetime.utcnow())
        embed.title = 'Bulk Delete'
        embed.set_footer(
            text=f'{len(payload.cached_messages)} message deleted • #{channel}')

        cached_messages = f'= {len(payload.cached_messages)} messages deleted in #{channel.name} =\n\n'
        for i in payload.cached_messages:
            date_time = i.created_at.strftime("%m/%d/%Y %H:%M:%S")
            cached_messages += f'{i.author} :: {i.author.id} :: {date_time}\n{i.content}\n\n'

        with open("temp.txt", "w") as file:
            file.write(cached_messages)

        self.message_log.send(embed=embed, username='WhaleShark Message Logging')

        with open("temp.txt", "rb") as file:
            self.message_log.send(file=discord.File(file, "logs.adoc"), username='WhaleShark Message Logging')


def setup(bot):
    bot.add_cog(MessageLogging(bot))
