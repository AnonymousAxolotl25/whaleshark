import os
import logging
import discord
import datetime
import asyncio

from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter

logging.basicConfig(level=logging.ERROR)

bot = commands.Bot(commands.when_mentioned_or('ws'), case_insensitive=True,
                   strip_after_prefix=True, help_command=None, max_messages=2000,
                   activity=discord.Game(name="ws help"))

@bot.event
async def on_ready():
    print('{0.user} connected!'.format(bot))
    embed = discord.Embed(color=0x2ecc71, description='🌱',
                          timestamp=datetime.datetime.utcnow())
    await bot.get_channel(int(os.getenv('LOG_CHANNEL'))).send(embed=embed)


@bot.event
async def on_error(event, *args, **kwargs):
    embed = discord.Embed(color=0xe74c3c)
    embed.description = f'❌ **Error**\n'

    if event == 'on_command_error':
        embed.description += (f'```ahk\n{args[1]}```\n[Message]({args[0].message.jump_url}) ' +
                              f'by {args[0].message.author.mention} `{args[0].message.author.name}#{args[0].message.author.discriminator}` ' +
                              f'in **{args[0].guild.name}**```plist\n{args[0].message.content}```\n')
    else:
        embed.description += f'```ahk\nEvent name: {event}```'
        for stuff in args:
            embed.description += f'```plist\n{str(stuff)}```'

    await bot.get_channel(int(os.getenv('LOG_CHANNEL'))).send(embed=embed)

    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')

    raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        if bot.user.id in ctx.message.raw_mentions:
            await ctx.message.add_reaction('❔')
            await asyncio.sleep(1)
            await ctx.message.remove_reaction('❔', ctx.bot.user)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.message.add_reaction('🐌')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('\❌ Missing required arguments.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply('\❌ Missing required permissions.')
    else:
        raise error


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.id in message.raw_mentions and not message.content.startswith(f'<@!{bot.user.id}>'):
        await message.add_reaction('<:whaleshark:838131079965048864>')
    elif 'whaleshark' in message.content.lower().replace(' ', ''):
        await message.add_reaction('🐳')
    elif message.content.lower() == 'ws':
        embed = discord.Embed(color=0x2C2F33)
        embed.description = 'Hello! I\'m WhaleShark, a private bot created by <@273212712698249216>.'
        await message.reply(embed=embed)
        await message.channel.send('<:whaleshark:838131079965048864><:says:838264594869911562>')

    await bot.process_commands(message)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.reply(f'\🟢 Loaded extension `{extension}`')


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.reply(f'\🔵 Reloaded extension `{extension}`')


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.reply(f'\🔴 Unloaded extension `{extension}`')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv('BOT_TOKEN'))
