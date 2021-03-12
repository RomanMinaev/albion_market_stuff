import discord
from aoparsers import AOParsers
import re

bot_token_file = open('DISCORD TOKEN_test.txt', 'r')
GUILD = 'SuSliK'
bot_token = bot_token_file.readline()
client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to {guild.name} (id: {guild.id})')


@client.event
async def on_message(message):
    username = message.author
    if message.author == client.user:
        return

    channel = message.channel
    if message.content.startswith('..get_rich'):
        while True:
            flips = AOParsers.get_rich('caerleon', 10000)
            try:
                if flips['itemId'] is None:
                    continue
                else:
                    itemId = flips['itemId']
                    quality = flips['quality']
                    bm_price = flips['bm_price']
                    bm_date = flips['bm_date']
                    caerleon_price = flips['caerleon_price']
                    caerleon_date = flips['caerleon_date']
                    profit = flips['profit']
                    print(f'AOParser responded with {itemId}')
                    embed_msg = discord.Embed(
                        title=f'Test',
                        description=f'**Item ID:** {itemId}\n'
                                    f'**Black Market:** {bm_price} '
                                    f'**Last seen at:** {bm_date}\n'
                                    f'**Caerleon:** {caerleon_price} '
                                    f'**Last seen at:** {caerleon_date}\n'
                                    f'**Flip profit:** {profit}'
                    )
                    print(f'http://render.albiononline.com/v1/item/{itemId}.png?count=1&quality={quality}')
                    embed_msg.set_image(
                        url=f'http://render.albiononline.com/v1/item/{itemId}.png?count=1&quality={quality}')
                    embed_msg.set_author(name=username.display_name,
                                         icon_url=username.avatar_url)
                    embed_msg.set_footer(text='Contact OopsieDoopsie#0412 if you need help with a bot.')
                    await channel.send(embed=embed_msg)
            except TypeError:
                continue

client.run(bot_token)
