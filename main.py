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
    if message.content.startswith('..hello'):
        await channel.send('Hello, fellow silver sinker! *wink-wink*')

    if message.content.startswith('..JSON_items_pull'):  # Pulls new itemlist. Shouldn't be commonly used
        if discord.utils.get(username.roles, name='Mechanic') is None:
            await message.add_reaction('❌')
        else:
            AOParsers.JSON_items_pull()
            await message.add_reaction('✅')

    if message.content.startswith('..item'):
        print('..item was called')
        item = message.content[7:]
        saved_item = item
        quality = str(1)  # placeholer value
        if '@' in saved_item:
            point = re.findall('(?<=@)\S', saved_item)[0]
            if int(point) > 3:
                point = str(3)
            item = re.findall('.+(?= @)', item)[0]
        if '#' in saved_item:
            print(saved_item)
            quality = re.findall('(?<=#).', saved_item)[0]
            print(quality)
        print(f'Sending {item} to AOParser...')
        itemId = AOParsers.item_to_itemid(item)
        if '@' in saved_item:
            itemId = itemId + '@' + point
        flips = AOParsers.black_market_flip(itemId, quality)
        bm_price = flips['bm_price']
        bm_date = flips['bm_date']
        caerleon_price = flips['caerleon_price']
        caerleon_date = flips['caerleon_date']
        profit = flips['profit']
        print(f'AOParser responded with {itemId}')
        embed_msg = discord.Embed(
            title=f'{item}',
            description=f'**Item ID:** {itemId}\n'
                        f'**Black Market:** {bm_price} '
                        f'**Last seen at:** {bm_date}\n'
                        f'**Caerleon:** {caerleon_price} '
                        f'**Last seen at:** {caerleon_date}\n'
                        f'**Flip profit:** {profit}'
        )
        print(f'http://render.albiononline.com/v1/item/{itemId}.png?count=1&quality={quality}')
        embed_msg.set_image(url=f'http://render.albiononline.com/v1/item/{itemId}.png?count=1&quality={quality}')
        embed_msg.set_author(name=username.display_name,
                             icon_url=username.avatar_url)
        embed_msg.set_footer(text='Contact OopsieDoopsie#0412 if you need help with a bot.')
        await channel.send(embed=embed_msg)

    if message.content.startswith('..get_rich'):
        while True:
            flips = AOParsers.get_rich()
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
