import sys

from discord import Client, DMChannel, TextChannel

from ancient_mediterranean import AncientMediterranean, AdministrativeException, InvalidOrderException, InvalidPlayerException

client = Client()
games = {}
players = {}


async def _valid_channel(channel):
    if isinstance(channel, DMChannel):
        await channel.send('command can only be used in the text channel associated with the game it effects')
    elif str(channel) not in games.keys():
        await channel.send('there is no game associated with this channel. use !new_game to start one')
    else:
        return True
    return False


async def idk(channel, auth):
    if isinstance(channel, DMChannel):
        pass
    elif str(channel) not in games.keys():
        await channel.send('there is no game associated with this channel. use !new_game to start one')
    elif auth not in players.keys() or str(channel) not in players[auth]:
        await channel.send("you are not a part of this channel's game")


@client.event
async def on_message(msg):
    auth = str(msg.author)
    channel = str(msg.channel)
    if auth == 'diplomacybot#4346':
        return
    print(auth)
    print(channel)
    lines = str(msg.content).splitlines()
    for line in lines:
        try:
            if line == '!help':
                await msg.channel.send('list of commands:\n'
                                       '!hello: to greet the bot\n'
                                       '!admin: use to claim admin power\n'
                                       '!relinquish_admin: removes your admin power (why you would do this is beyond me)\n'
                                       '!lock_players: **ADMIN ONLY** stop players from claiming colors\n'
                                       '!unlock_players: **ADMIN ONLY** allow players to claim colors\n'
                                       '!kick_player AAAAA#0000: **ADMIN ONLY** removes player from their assigned color\n'
                                       '!status: **ADMIN ONLY** displays how many orders each player has submitted\n'
                                       '!step: **ADMIN ONLY** advances the game state one phase\n'
                                       '!assign <color>: use to assign yourself as one of the 5 players\n'
                                       '!resign: removes you from the game (tho your units are unchanged)\n'
                                       'supported colors are red, blue, green, black, and yellow\n'
                                       'THOSE BELOW ARE CURRENTLY UNAVAILABLE CUZ SORENS DUMB\n'
                                       '!my_units: returns a list of your units\n'
                                       '!all_units: returns a list of all units on the board\n'
                                       '!my_supply_centers: returns a list of your supply centers\n'
                                       '!all_supply_centers: returns a list of all owned supply centers on the board\n'
                                       '!my_orders: returns a list of your units with their corresponding orders\n'
                                       '!get XXX: returns the order issued to the unit in territory XXX\n'
                                       '!reset_orders: removes all orders submitted this season'
                                       'you may also type in any orders (one per line) to issue to your units\n'
                                       'example: F Tha S Pun')
            elif line.startswith('!hello'):
                await msg.channel.send('Fuck off {}, ya cunt!\n'.format(msg.author))
            elif line.startswith('!new_game'):
                if isinstance(channel, DMChannel):
                    await channel.send('a new game cannot be started in a DM channel')
                elif channel in games.keys():
                    await msg.channel.send("can't start a new game in a channel with a running game")
                else:
                    games[channel] = AncientMediterranean()
                    await msg.channel.send('new game started in {}'.format(str(channel)))
            elif line.startswith('!admin'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].assign_admin(auth))
            elif line.startswith('!relinquish_admin'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].relinquish_admin(auth))
            elif line.startswith('!lock_players'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].lock_players(auth))
            elif line.startswith('!unlock_players'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].unlock_players(auth))
            elif line.startswith('!kick_player'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].kick_player(auth, line[13:]))
                    # remove channel from player's game set
                    players[auth].remove(channel)
                    # # this may be necessary
                    # if len(players[auth]) == 0:
                    #     players.pop(auth)
            elif line.startswith('!status'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].get_num_orders_submitted(auth))
            elif line.startswith('!step'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].game_step(auth))
            elif line.startswith('!assign'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].assign_player(auth, line[8:].lower()))
                    # add to channel to player's game set
                    if auth in players.keys():
                        players[auth].add(channel)
                    else:
                        players[auth] = {channel}
            elif line.startswith('!resign'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].remove_player(auth))
                    # remove channel from player's game set
                    players[auth].remove(channel)
                    # # this may be necessary
                    # if len(players[auth]) == 0:
                    #     players.pop(auth)
            # TODO: figure out how to figure out which game this is referencing
            elif isinstance(msg.channel, DMChannel):
                await msg.channel.send('cant process commands given in DMs rn, sorry')
            elif line == '!my_units':
                await msg.channel.send(games[channel].get_my_units(auth))
            elif line == '!all_units':
                await msg.channel.send(games[channel].get_all_units())
            elif line == '!my_supply_centers':
                await msg.channel.send(games[channel].get_my_supply_centers(auth))
            elif line == '!all_supply_centers':
                await msg.channel.send(games[channel].get_all_supply_centers())
            elif line == '!my_orders':
                if isinstance(msg.channel, DMChannel):
                    await msg.channel.send(games[channel].get_my_orders(auth))
                else:
                    await msg.channel.send('you can only access your orders via DM')
            elif line.startswith('!get'):
                if isinstance(channel, DMChannel):
                    await msg.channel.send(games[channel].get_order(auth, line[5:8].upper()))
                else:
                    await msg.channel.send('you can only access your orders via DM')
            elif line.startswith('!reset_orders'):
                await msg.channel.send(games[channel].reset_orders(auth))
            elif line[0:2] in ['A ', 'a ', 'F ', 'f ']:
                await msg.channel.send(games[channel].add_order(auth, line.strip().upper()))
        except (AdministrativeException, InvalidOrderException, InvalidPlayerException) as e:
            await msg.channel.send(str(e))


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
