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
        bm = AOParsers.flip(itemId, quality, 'black_market')
        bm_price = bm['bm']
        bm_date = bm['city_date']
        caerleon = AOParsers.flip(itemId, quality, 'caerleon')
        caerleon_price = caerleon['city_price']
        caerleon_date = caerleon['city_date']
        fort_sterling = AOParsers.flip(itemId, quality, 'fort_sterling')
        fort_sterling_price = fort_sterling['city_price']
        fort_sterling_date = fort_sterling['city_date']
        lymhurst = AOParsers.flip(itemId, quality, 'lymhurst')
        lymhurst_price = lymhurst['city_price']
        lymhurst_date = lymhurst['city_date']
        bridgewatch = AOParsers.flip(itemId, quality, 'bridgewatch')
        bridgewatch_price = bridgewatch['city_price']
        bridgewatch_date = bridgewatch['city_date']
        martlock = AOParsers.flip(itemId, quality, 'martlock')
        martlock_price = martlock['city_price']
        martlock_date = martlock['city_date']
        thetford = AOParsers.flip(itemId, quality, 'thetford')
        thetford_price = thetford['city_price']
        thetford_date = thetford['city_date']
        print(f'AOParser responded with {itemId}')
        embed_msg = discord.Embed(
            title=f'{item}',
            description=f'🆔**Item ID:** {itemId}\n'
                        '\n'
                        f'🟥**Black Market:** {bm_price} '
                        f'**Last seen at:** {bm_date}\n'
                        '\n'
                        f'🟥**Caerleon:** {caerleon_price} '
                        f'**Last seen at:** {caerleon_date}\n'
                        '\n'
                        f'⬜**Fort Sterling:** {fort_sterling_price} '
                        f'**Last seen at:** {fort_sterling_date}\n'
                        '\n'
                        f'🟩**Lymhurst:** {lymhurst_price} '
                        f'**Last seen at:** {lymhurst_date}\n'
                        '\n'
                        f'🟧**Bridgewatch:** {bridgewatch_price} '
                        f'**Last seen at:** {bridgewatch_date}\n'
                        '\n'
                        f'🟦**Martlock:** {martlock_price} '
                        f'**Last seen at:** {martlock_date}\n'
                        '\n'
                        f'🟪**Thetford:** {thetford_price} '
                        f'**Last seen at:** {thetford_date}\n'
        )
        print(f'http://render.albiononline.com/v1/item/{itemId}.png?count=1&quality={quality}')
        embed_msg.set_image(url=f'http://render.albiononline.com/v1/item/{itemId}.png?count=1&quality={quality}')
        embed_msg.set_author(name=username.display_name,
                             icon_url=username.avatar_url)
        embed_msg.set_footer(text='Contact OopsieDoopsie#0412 if you need help with a bot.')
        await channel.send(embed=embed_msg)

client.run(bot_token)
