import sys

from discord import Client, DMChannel

from ancient_mediterranean import AdministrativeException, AncientMediterranean, InvalidOrderException, \
    InvalidPlayerException

client = Client()
games = {}
player_focus = {}  # game with focus


async def _valid_channel(channel):
    if isinstance(channel, DMChannel):
        await channel.send('command can only be used in the text channel associated with the game it effects')
    elif str(channel) not in games.keys():
        await channel.send('there is no game associated with this channel. use **!new_game** to start one')
    else:
        return True
    return False


async def _focused(channel, auth):
    if isinstance(channel, DMChannel):
        if player_focus.get(auth):
            if games.get(player_focus[auth]):
                return True
            else:
                await channel.send("the channel you're focused on doesn't have an associated game.\n"
                                   "start one by using the command **!new_game** in that channel.")
        else:
            await channel.send("you aren't focused on any game. use **!focus** to focus on a game")
    else:
        await channel.send('this command can only be used in DMs')
    return False


@client.event
async def on_message(msg):
    auth = str(msg.author)
    channel = str(msg.channel)
    if auth == 'diplomacybot#4346':
        return
    print(auth)
    print(channel)

    if isinstance(channel, DMChannel) and auth not in player_focus:
        player_focus[auth] = None

    if msg.content.startswith('!override'):
        try:
            if await _valid_channel(msg.channel):
                await msg.channel.send(games[channel].override(auth, str(msg.content)[10:].strip().upper()))
        except AdministrativeException as e:
            await msg.channel.send(str(e))
        return
    lines = str(msg.content).splitlines()
    for line in lines:
        try:
            if line == '!help':
                await msg.author.send(
                    "orders are any line that start with an a or f (not case sensitive) of the form:\n"
                    "'f aaa-bbb' for a move from aaa to bbb\n"
                    "'a ccc-ddd via convoy' for a convoyed move from ccc to ddd\n"
                    "'a eee h' for a unit in eee to hold\n"
                    "'f fff c ggg-hhh' to order a fleet in fff to convoy an army from ggg to hhh\n"
                    "'f iii s jjj' for a unit in iii to support jjj's hold\n"
                    "'a kkk s lll-mmm' for kkk to support lll's move into mmm\n"
                    "'a nnn s ooo-ppp via convoy' for nnn to support ooo's convoyed move into ppp\n"
                    "'a ccc-ddd via convoy' for a convoyed move from ccc to ddd\n"
                    "all units in diplomacy are referred to using three letter codes.\n"
                    "this bot currently doesn't support use of the territories' full names (and probably never will).\n"
                    "**!more_help**: for a list of administrative commands use\n"
                    "**!admin help**: for admin only commands")
            elif line == '!more_help':
                await msg.author.send(
                    "**!hello**: to greet the bot\n"
                    "**!focus** <channel id>: to set your focus on that channel\n"
                    "your focus determines which game your DM commands affect.\n"
                    "**!get_focus**: returns the name of the channel you're currently focused on\n"
                    "**!assign** <color>: take control of one of the 5 colors (red, blue, green, black, and yellow)\n"
                    "**!resign**: removes you from the game (your units and supply centers remain unchanged)\n"
                    "**!my_units**: returns a list of your units\n"
                    "**!all_units**: returns a list of everyone's units\n"
                    "**!my_supply_centers**: returns a list of your supply centers\n"
                    "**!all_supply_centers**: returns a list of everyone's supply centers\n"
                    "**!my_orders**: ofr a list of your units with their corresponding orders\n"
                    "**!get** xxx: returns the order issued to the unit in xxx\n"
                    "**!reset_orders**: removes all orders submitted this season\n"
                    "**!admin**: use to claim admin power\n"
                    "**!relinquish_admin**: removes your admin power (why you would do this is beyond me)\n"
                    "use **!admin_help** for a list of admin only commands")
            elif line == '!admin_help':
                await msg.author.send(
                    "**!lock_players**: stop players from claiming colors\n"
                    "**!unlock_players**: allow players to claim colors\n"
                    "**!kick_player** <user id>: removes player from their assigned color\n"
                    "**!status**: displays how many orders each player has submitted\n"
                    "**!step**: advances the game state one phase\n"
                    "**!set_season** <season>: self-explanatory\n"
                    "**!set_year** ##: ditto\n"
                    "**!clear_orders**: deletes all orders submitted by all players\n"
                    "**!override** <color>: **ADMIN ONLY** all following lines in the message will be\n"
                    "immediately resolved to adjust the game state of the specified color. moves can\n"
                    "be move, build, or disband orders to modify color's units or special\n"
                    "'add supply center' or 'remove supply center' orders that add and remove\n"
                    "control of supply centers, respectively")
            elif line == '!hello':
                await msg.channel.send('Fuck off {}, ya cunt!\n'.format(auth))
            elif line.startswith('!focus'):
                if isinstance(msg.channel, DMChannel):
                    focus_target = str(msg.content)[7:]
                    if focus_target in games.keys():
                        player_focus[auth] = focus_target
                    else:
                        await channel.send('there is no game associated with that channel.\n'
                                           'use **!new_game** in a text channel to start one.')
                else:
                    await msg.channel.send('focus can only be changed in DMs')
            elif line.startswith('!get_focus'):
                if _focused(msg.channel, auth):
                    await msg.channel.send('focus is currently on {}'.format(player_focus[auth]))
            elif line == '!new_game':
                if isinstance(channel, DMChannel):
                    await channel.send('a new game cannot be started in a DM channel')
                elif channel in games.keys():
                    await msg.channel.send("can't start a new game in a channel with a running game")
                else:
                    games[channel] = AncientMediterranean()
                    await msg.channel.send('new game started in {}'.format(str(channel)))
            elif line == '!save':
                if await _valid_channel(msg.channel):
                    games[channel].save(channel)
                    await msg.channel.send('game state saved')
            elif line == '!load':
                if isinstance(channel, DMChannel):
                    await channel.send(
                        'command can only be used in the text channel associated with the game it effects')
                else:
                    games[channel] = AncientMediterranean()
                    games[channel].load(channel)
                    await msg.channel.send('game state loaded')
            elif line == '!admin':
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].assign_admin(auth))
            elif line == '!relinquish_admin':
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].relinquish_admin(auth))
            elif line == '!lock_players':
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].lock_players(auth))
            elif line == '!unlock_players':
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].unlock_players(auth))
            elif line.startswith('!kick_player'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].kick_player(auth, line[13:]))
            elif line == '!status':
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].orders_status(auth))
            elif line == '!step':
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].game_step(auth))
            elif line.startswith('!set_season'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].set_season(auth, line[12:]))
            elif line.startswith('!set_year'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].set_year(auth, line[10:]))
            elif line == '!clear_orders':
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].clear_orders(auth))
            elif line.startswith('!assign'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].assign_player(auth, line[8:].lower()))
            elif line.startswith('!resign'):
                if await _valid_channel(msg.channel):
                    await msg.channel.send(games[channel].remove_player(auth))
            elif line == '!my_units':
                if isinstance(msg.channel, DMChannel):
                    if _focused(msg.channel, auth):
                        await msg.channel.send(games[player_focus[auth]].get_my_units(auth))
                else:
                    if await _valid_channel(msg.channel):
                        await msg.channel.send(games[channel].get_my_units(auth))
            elif line == '!all_units':
                if isinstance(msg.channel, DMChannel):
                    if _focused(msg.channel, auth):
                        await msg.channel.send(games[player_focus[auth]].get_all_units())
                else:
                    if await _valid_channel(msg.channel):
                        await msg.channel.send(games[channel].get_all_units())
            elif line == '!my_supply_centers':
                if isinstance(msg.channel, DMChannel):
                    if _focused(msg.channel, auth):
                        await msg.channel.send(games[player_focus[auth]].get_my_supply_centers(auth))
                else:
                    if await _valid_channel(msg.channel):
                        await msg.channel.send(games[channel].get_my_supply_centers(auth))
            elif line == '!all_supply_centers':
                if isinstance(msg.channel, DMChannel):
                    if _focused(msg.channel, auth):
                        await msg.channel.send(games[player_focus[auth]].get_all_supply_centers())
                else:
                    if await _valid_channel(msg.channel):
                        await msg.channel.send(games[channel].get_all_supply_centers())
            elif line == '!my_orders':
                if _focused(msg.channel, auth):
                    await msg.channel.send(games[player_focus[auth]].get_my_orders(auth))
            elif line.startswith('!get'):
                if _focused(msg.channel, auth):
                    await msg.channel.send(games[player_focus[auth]].get_order(auth, line[5:8].upper()))
            elif line.startswith('!reset_orders'):
                if _focused(msg.channel, auth):
                    await msg.channel.send(games[player_focus[auth]].reset_orders(auth))
            elif line[0:2] in ['A ', 'a ', 'F ', 'f ']:
                if _focused(msg.channel, auth):
                    await msg.channel.send(games[player_focus[auth]].add_order(auth, line.strip().upper()))
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

# TODO: generate maps after each game step
