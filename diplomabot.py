import json
import os
import sys

from discord import Client, DMChannel, File

from ancient_mediterranean import AdministrativeException, AncientMediterranean, InvalidOrderException, \
    InvalidPlayerException

from cleanup import register_exit_fun

client = Client()
games = {}
game_save_folder = 'game_saves'
player_focus = {}  # game with focus

# TODO: need method for testing without internet connection like passing fake messages


def _valid_channel(channel):
    if isinstance(channel, DMChannel):
        return 'command can only be used in the text channel associated with the game it effects'
    elif str(channel) not in games.keys():
        return 'there is no game associated with this channel. use **!new_game** to start one'
    else:
        return None


def _focused(channel, author):
    if isinstance(channel, DMChannel):
        if player_focus.get(author.id):
            if games.get(player_focus[author.id]):
                return None
            else:
                return "the channel you're focused on doesn't have an associated game. start one by using the " \
                       "command **!new_game** in that channel."
        else:
            return "you aren't focused on any game. use **!focus** to focus on a game"
    else:
        return 'this command can only be used in DMs'


def _check_both(channel, author):
    if isinstance(channel, DMChannel):
        if player_focus.get(author.id):
            if games.get(player_focus[author.id]):
                return games[player_focus[author.id]], None
            else:
                return None, "the channel you're focused on doesn't have an associated game. start one by using the " \
                       "command **!new_game** in that channel."
        else:
            return None, "you aren't focused on any game. use **!focus** to focus on a game"
    elif str(channel) not in games.keys():
        return None, 'there is no game associated with this channel. use **!new_game** to start one'
    else:
        return games[str(channel)], None


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    auth = msg.author
    channel = str(msg.channel).lower()
    print(str(auth))
    print(auth.id)
    print(channel)
    # hardcoded so only i can kill the bot
    if msg.content == '!kill' and auth.id == 480300800518782996:
        # sys.exit()
        await client.logout()
    if msg.content.startswith('!override'):
        try:
            error_msg = _valid_channel(msg.channel)
            if error_msg:
                await msg.channel.send(error_msg)
            else:
                save_path = game_save_folder + '/' + channel
                overview, map_path = games[channel].override(str(auth), str(msg.content)[10:], save_path)
                await msg.channel.send(overview)
                await msg.channel.send(file=File(map_path))
        except AdministrativeException as e:
            await msg.channel.send(str(e))
        return
    replies = []
    attachment_paths = []
    for line in str(msg.content).splitlines():
        line = line.strip().lower()
        try:
            if line == '!help':
                await auth.send(
                    "before trying to send orders, focus on a game and assign yourself to a color. instructions in "
                    "**!more_help**\n"
                    "orders are any line that start with an a or f of the form:\n"
                    "**f aaa-bbb** for a move from aaa to bbb\n"
                    "**a ccc-ddd via convoy** for a convoyed move from ccc to ddd\n"
                    "**a eee h** for a unit in eee to hold\n"
                    "**f fff c ggg-hhh** to order a fleet in fff to convoy an army from ggg to hhh\n"
                    "**f iii s jjj** for a unit in iii to support jjj's hold\n"
                    "**a kkk s lll-mmm** for kkk to support lll's move into mmm\n"
                    "**a nnn s ooo-ppp via convoy** for nnn to support ooo's convoyed move into ppp\n"
                    "**a qqq b** to build a unit at a supply center in qqq\n"
                    "**f rrr d** to disband the unit in rrr\n"
                    "(orders are not case sensitive and do not start with an **!**)\n"
                    "orders may only be submitted via DM (you wouldn't want others to see your orders after all)\n"
                    "all units in diplomacy are referred to using three letter codes. this bot currently doesn't "
                    "support use of the territories' full names (and probably never will).\n"
                    "if you're lazy, use the **!hold_rest** command to make all of your unordered units hold.\n"
                    "**!more_help**: for a list of administrative commands use\n"
                    "**!admin help**: for admin only commands")
            elif line == '!more_help':
                await auth.send(
                    "**!hello**: to greet the bot\n"
                    "**!focus**: if sent in a text channel, your focus is set to that channel. if sent in DMs, you "
                    "need to include a <channel name> to focus on. your focus determines which game your DM commands "
                    "affect.\n"
                    "**!get_focus**: returns the name of the channel you're currently focused on\n"
                    "**!assign** <color>: take control of one of the 5 colors (red, blue, green, black, and yellow)\n"
                    "**!resign**: removes you from the game (your units and supply centers remain unchanged)\n"
                    "**!map**\n"
                    "**!status**: returns the season, year, and how many orders each player has submitted\n"
                    "**!my_orders**: ofr a list of your units with their corresponding orders **DM ONLY**\n"
                    "**!get** xxx: returns the order issued to the unit in xxx **DM ONLY**\n"
                    "**!reset_orders**: removes all orders submitted this season **DM ONLY**\n"
                    "**!my_units**: returns a list of your units\n"
                    "**!all_units**: returns a list of everyone's units\n"
                    "**!my_supply_centers**: returns a list of your supply centers\n"
                    "**!all_supply_centers**: returns a list of everyone's supply centers\n"
                    "**!admin**: use to claim admin power\n"
                    "**!relinquish_admin**: removes your admin power (why you would do this is beyond me)\n"
                    "use **!admin_help** for a list of admin only commands")
            elif line == '!admin_help':
                await auth.send(
                    "all admin commands are only usable in the text channels the game the commands are meant for. this "
                    "is meant to stop admins from doing stuff behind the players' backs.\n"
                    "**!lock_players**: stop players from claiming colors\n"
                    "**!unlock_players**: allow players to claim colors\n"
                    "**!kick_player** <user id>: removes player from their assigned color\n"
                    "**!step**: advances the game state one phase\n"
                    "**!clear_orders**: deletes all orders submitted by all players\n"
                    "**!override** use **!override_help** to learn more")
            elif line == "!override_help":
                await auth.send(
                    "override is an extremely powerful command with fer checks on correct usage. misuse will mess up "
                    "the game state and require soren to manually fix it.\n"
                    "**!override** <color>: an override order is one message comprised of several lines. each line "
                    "after the override command is equivalent to one order that is immediately resolved to adjust the "
                    "game state of the specified color. orders can be move, build, or disband to modify <color>'s "
                    "units (hold, convoy, and support orders are invalid). override also allows for the following "
                    "special orders to be used:\n"
                    "**add supply center sss** to take control of a supply center in sss\n"
                    "**remove supply center in ttt** to remove control of a supply center in ttt\n"
                    "**set season** <season> self-explanatory\n"
                    "**set year** ## ditto\n"
                    "**a uuu retreat vvv** to tell the game that in the previous season a unit from vvv dislodged a"
                    "unit from uuu\n"
                    "**remove retreat www** to remove the game state associated with a unit that was dislodged from "
                    "www\n"
                    "**add standoff xxx** to tell the game that in the previous season a standoff occurred at xxx\n"
                    "**remove standoff yyy** to remove a standoff that occurred in yyy")
            elif line == '!hello':
                await msg.channel.send('Fuck off {}, ya cunt!\n'.format(str(auth)))
            elif line.startswith('!focus'):
                if isinstance(msg.channel, DMChannel):
                    focus_target = line[7:].strip()
                    for c in client.get_all_channels():
                        if focus_target == c.name:
                            player_focus[auth.id] = focus_target
                            replies.append('focusing on {}'.format(focus_target))
                            break
                    else:
                        replies.append('no channel named {} to focus on'.format(focus_target))
                else:
                    replies.append('focusing on {}'.format(channel))
            elif line == '!get_focus':
                if player_focus.get(auth.id):
                    replies.append('focus is currently on {}'.format(player_focus[auth.id]))
                else:
                    replies.append("you aren't focused on any game. use **!focus** to focus on a game")
            elif line == '!new_game':
                if isinstance(channel, DMChannel):
                    replies.append('a new game cannot be started in a DM channel')
                elif games.get(channel):
                    replies.append("can't start a new game in a channel with a running game")
                else:
                    games[channel] = AncientMediterranean()
                    replies.append('new game started in {}'.format(channel))
            elif line == '!admin':
                error_msg = _valid_channel(msg.channel)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[channel].assign_admin(str(auth)))
            elif line == '!relinquish_admin':
                error_msg = _valid_channel(msg.channel)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[channel].relinquish_admin(str(auth)))
            elif line == '!lock_players':
                error_msg = _valid_channel(msg.channel)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[channel].lock_players(str(auth)))
            elif line == '!unlock_players':
                error_msg = _valid_channel(msg.channel)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[channel].unlock_players(str(auth)))
            elif line.startswith('!kick_player'):
                error_msg = _valid_channel(msg.channel)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[channel].kick_player(str(auth), line[13:]))
            elif line == '!step':
                error_msg = _valid_channel(msg.channel)
                if error_msg:
                    replies.append(error_msg)
                else:
                    save_path = game_save_folder + '/' + channel
                    overview, map_paths = games[channel].game_step(str(auth), save_path)
                    replies.append(overview)
                    for map_path in map_paths:
                        attachment_paths.append(File(map_path))
            elif line == '!clear_orders':
                error_msg = _valid_channel(msg.channel)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[channel].clear_orders(str(auth)))
            elif line.startswith('!assign'):
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    replies.append(game.assign_player(str(auth), line[8:].lower()))
            elif line.startswith('!resign'):
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    replies.append(game.resign_player(str(auth)))
            elif line == '!status':
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    replies.append(game.status())
            elif line == '!map':
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    attachment_paths.append(File(game.map_path))
            elif line == '!my_units':
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    replies.append(game.get_my_units(str(auth)))
            elif line == '!all_units':
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    replies.append(game.get_all_units())
            elif line == '!my_supply_centers':
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    replies.append(game.get_my_supply_centers(str(auth)))
            elif line == '!all_supply_centers':
                game, error_msg = _check_both(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                elif game:
                    replies.append(game.get_all_supply_centers())
            elif line == '!my_orders':
                error_msg = _focused(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[player_focus[auth.id]].get_my_orders(str(auth)))
            elif line.startswith('!get'):
                error_msg = _focused(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[player_focus[auth.id]].get_order(str(auth), line[5:].upper()))
            elif line == '!reset_orders':
                error_msg = _focused(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[player_focus[auth.id]].reset_orders(str(auth)))
            elif line == '!hold_rest':
                error_msg = _focused(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[player_focus[auth.id]].hold_rest(str(auth)))
            elif line[0:2] in {'a ', 'f '}:
                error_msg = _focused(msg.channel, auth)
                if error_msg:
                    replies.append(error_msg)
                else:
                    replies.append(games[player_focus[auth.id]].add_order(str(auth), line))
        except (AdministrativeException, InvalidOrderException, InvalidPlayerException) as e:
            replies.append(str(e))
    if replies:
        await msg.channel.send('\n'.join(replies))
    if attachment_paths:
        await msg.channel.send(files=attachment_paths)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # search game saves folder for save files and load them
    print('games found on startup:')
    for filename in os.listdir('game_saves'):
        if filename.endswith('.json'):
            game_name = filename[:-5]
            # don't load over in-play game
            # this would happen if the bot has to reconnect after the internet connection is lost temporarily
            if games.get(game_name):
                print('{} already in-play'.format(game_name))
                continue
            print(game_name)
            load_path = game_save_folder + '/' + game_name
            games[game_name] = AncientMediterranean(load_path=load_path)
    # load in players' focus so they don't have to refocus every time the bot is reset
    with open('player_focus.json', 'r') as file:
        pf = json.load(file)
        for player, focus in pf.items():
            player_focus[int(player)] = focus


def cleanup():
    print('\nsaved player focuses')
    with open('player_focus.json', 'w') as file:
        json.dump(player_focus, file)
    games_saved_msg = ['saved games:']
    for channel, game in games.items():
        games_saved_msg.append(channel)
        game.save(game_save_folder + '/' + channel)
    print('\n'.join(games_saved_msg))


register_exit_fun(cleanup)

assert len(sys.argv) == 2, "must provide only one input, the bot's token"
TOKEN = sys.argv[1]
client.run(TOKEN)

# TODO: remove !my_units, !all_units, !my_supply_centers, and !all_supply_centers once map generation code is stable.
#  put territories into their own files which correspond to the game variants
#  one for classic diplomacy, and one for ancient mediterranean
