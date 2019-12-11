import sys

from discord import Client, DMChannel, TextChannel

from ancient_mediterranean import AncientMediterranean

client = Client()
am = AncientMediterranean()


@client.event
async def on_message(message):
    if str(message.author) == 'diplomacybot#4346':
        return
    print(message.author)
    channel = message.channel
    if isinstance(channel, TextChannel):
        if str(channel) != 'bot-testing':
            return
    if message.content == '!help':
        await channel.send('list of commands:\n'
                           '!hello: to greet the bot\n'
                           '!admin: use to claim admin power\n'
                           '!relinquish_admin: removes your admin power (why you would do this is beyond me)\n'
                           '!lock_players: *ADMIN ONLY* stop players from claiming colors\n'
                           '!unlock_players: *ADMIN ONLY* allow players to claim colors\n'
                           '!kick_player AAAAA#0000: *ADMIN ONLY* removes player from their assigned color\n'
                           '!my_units: returns a list of your units\n'
                           '!all_units: returns a list of all units on the board\n'
                           '!my_supply_centers: returns a list of your supply centers\n'
                           '!all_supply_centers: returns a list of all owned supply centers on the board\n'
                           '!my_orders: returns a list of your units with their corresponding orders\n'
                           '!get XXX: returns the order issued to the unit in territory XXX\n'
                           '!reset_orders: removes all orders submitted this season'
                           '!assign <color>: use to assign yourself as one of the 5 players\n'
                           '!resign: removes you from the game (tho your units are unchanged)\n'
                           'supported colors are red, blue, green, black, and yellow\n'
                           'you may also type in any orders (one per line) to issue to your units\n'
                           'example: F Tha S Pun')
    elif message.content.startswith('!hello'):
        await channel.send('Fuck off {}, ya cunt!\n'.format(message.author))
    elif message.content.startswith('!admin'):
        await channel.send(am.assign_admin(str(message.author)))
    elif message.content.startswith('!relinquish_admin'):
        await channel.send(am.relinquish_admin(str(message.author)))
    elif message.content.startswith('!lock_players'):
        await channel.send(am.lock_players(str(message.author)))
    elif message.content.startswith('!unlock_players'):
        await channel.send(am.unlock_players(str(message.author)))
    elif message.content.startswith('!kick_player'):
        await channel.send(am.kick_player(str(message.author), str(message.content)[13:]))
    elif str(message.content) == '!my_units':
        await channel.send(am.get_my_units(str(message.author)))
    elif str(message.content) == '!all_units':
        await channel.send(am.get_all_units())
    elif str(message.content) == '!my_supply_centers':
        await channel.send(am.get_my_supply_centers(str(message.author)))
    elif str(message.content) == '!all_supply_centers':
        await channel.send(am.get_all_supply_centers())
    elif str(message.content) == '!my_orders':
        if isinstance(channel, DMChannel):
            await channel.send(am.get_my_orders(str(message.author)))
        else:
            await channel.send('you can only access your orders via DM')
    elif str(message.content).startswith('!get'):
        if isinstance(channel, DMChannel):
            await channel.send(am.get_order(str(message.author), str(message.content)[5:8].upper()))
        else:
            await channel.send('you can only access your orders via DM')
    elif message.content.startswith('!reset_orders'):
        await channel.send(am.reset_orders(str(message.author)))
    elif message.content.startswith('!assign'):
        await channel.send(am.assign_player(str(message.author), str(message.content)[8:].lower()))
    elif message.content.startswith('!resign'):
        await channel.send(am.remove_player(str(message.author)))
    elif str(message.content)[0:2] in ['A ', 'a ', 'F ', 'f ']:
        lines = str(message.content).splitlines()
        ret_mes = ''
        for line in lines:
            ret_mes += am.add_order(str(message.author), line.strip().upper()) + '\n'
        await channel.send(ret_mes)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


assert len(sys.argv) == 2, "must provide only one input, the bot's token"
TOKEN = sys.argv[1]
client.run(TOKEN)

# TODO: make administrator role with ability to lock and unlock color assignment which gets announced publicly
#  ability to generate maps
#  function to resolve conflicts and update unit positions
#  command for building units
#  calculate number of units to destroy or build
#  better error messages. explain why an order is incorrect instead of sending 'incorrect'
