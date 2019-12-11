from copy import deepcopy
import re

territories = {'GAU', 'RHA', 'SAM', 'VIN', 'ILL', 'LUS', 'ARM', 'GAL', 'DAM', 'ARA', 'CIR', 'SAH', 'PHA', 'MAR', 'SAG',
               'TAR', 'MAS', 'ETU', 'ROM', 'NEA', 'APU', 'RAV', 'VEN', 'DAL', 'EPI', 'ATH', 'SPA', 'MAC', 'BYZ', 'DAC',
               'CHE', 'SIP', 'BIT', 'MIL', 'ISA', 'CAP', 'ANT', 'SID', 'TYE', 'JER', 'SII', 'PET', 'NAB', 'MAU', 'CAR',
               'THA', 'NUM', 'LEP', 'CYR', 'ALE', 'MEM', 'BAY', 'THE', 'COR', 'SAD', 'SIC', 'CRE', 'CYP', 'IBE', 'BER',
               'LIG', 'TYN', 'PUN', 'ADR', 'ION', 'AUS', 'GOT', 'GOS', 'LIB', 'MES', 'AEG', 'BLA', 'MIN', 'EGY',
               'CIL', 'SYR', 'GOP', 'REE', 'BAL'}

inlands = ['GAU', 'RHA', 'SAM', 'VIN', 'ILL', 'LUS', 'ARM', 'GAL', 'DAM', 'ARA', 'CIR', 'SAH', 'PHA', 'MAR']
coasts = ['SAG', 'TAR', 'MAS', 'ETU', 'ROM', 'NEA', 'APU', 'RAV', 'VEN', 'DAL', 'EPI', 'ATH', 'SPA', 'MAC', 'BYZ',
          'DAC', 'CHE', 'SIP', 'BIT', 'MIL', 'ISA', 'CAP', 'ANT', 'SID', 'TYE', 'JER', 'SII', 'PET', 'NAB', 'MAU',
          'CAR', 'THA', 'NUM', 'LEP', 'CYR', 'ALE', 'MEM', 'BAY', 'THE', 'COR', 'SAD', 'SIC', 'CRE', 'CYP']
seas = ['IBE', 'BER', 'LIG', 'TYN', 'PUN', 'ADR', 'ION', 'AUS', 'GOT', 'GOS', 'LIB', 'MES', 'AEG', 'BLA', 'MIN', 'EGY',
        'CIL', 'SYR', 'GOP', 'REE', 'BAL']
supply_center_territories = ['VIN', 'DAM', 'CIR', 'SAG', 'MAS', 'ROM', 'NEA', 'RAV', 'DAL', 'ATH', 'SPA', 'MAC', 'BYZ',
                             'CHE', 'SIP', 'MIL', 'ANT', 'SID', 'TYE', 'JER', 'PET', 'CAR', 'THA', 'NUM', 'LEP', 'CYR',
                             'ALE', 'MEM', 'THE', 'SAD', 'SIC', 'CRE', 'CYP', 'BAL']
starting_supply_centers = {'red': {'NEA', 'ROM', 'RAV'},
                           'blue': {'THA', 'CIR', 'CAR'},
                           'green': {'SPA', 'ATH', 'MAC'},
                           'black': {'SID', 'ANT', 'DAM'},
                           'yellow': {'ALE', 'MEM', 'THE'}}
land_routes = {'GAU': ['RHA', 'MAS', 'TAR', 'LUS'],
               'RHA': ['SAM', 'VIN', 'VEN', 'ETU', 'MAS', 'GAU'],
               'SAM': ['CHE', 'DAC', 'ILL', 'VIN', 'RHA'],
               'VIN': ['SAM', 'ILL', 'DAL', 'VEN', 'RHA'],
               'ILL': ['SAM', 'DAC', 'MAC', 'EPI', 'DAL', 'VIN'],
               'LUS': ['GAU', 'TAR', 'SAG'],
               'ARM': ['CHE', 'DAM', 'CAP', 'SIP'],
               'GAL': ['BIT', 'SIP', 'CAP', 'ISA', 'MIL', 'BYZ'],
               'DAM': ['ARM', 'ARA', 'SID', 'ANT', 'CAP'],
               'ARA': ['DAM', 'NAB', 'JER', 'TYE', 'SID'],
               'CIR': ['CAR', 'THA', 'NUM', 'PHA', 'SAH', 'MAU'],
               'SAH': ['CIR', 'PHA', 'BAY', 'MAU'],
               'PHA': ['NUM', 'LEP', 'MAR', 'BAY', 'SAH', 'CIR'],
               'MAR': ['CYR', 'MEM', 'BAY', 'PHA', 'LEP'],
               'SAG': ['LUS'],
               'TAR': ['GAU', 'LUS'],
               'MAS': ['GAU', 'RHA'],
               'ETU': ['RHA', 'VEN', 'RAV'],
               'ROM': ['RAV', 'APU'],
               'NEA': [],
               'APU': ['ROM'],
               'RAV': ['ROM', 'ETU'],
               'VEN': ['RHA', 'VIN', 'ETU'],
               'DAL': ['VIN', 'ILL'],
               'EPI': ['ILL', 'MAC'],
               'ATH': [],
               'SPA': [],
               'MAC': ['ILL', 'DAC', 'EPI'],
               'BYZ': ['GAL'],
               'DAC': ['SAM', 'ILL', 'MAC'],
               'CHE': ['SAM', 'ARM'],
               'SIP': ['ARM', 'CAP', 'GAL'],
               'BIT': ['GAL'],
               'MIL': ['GAL'],
               'ISA': ['GAL'],
               'CAP': ['SIP', 'ARM', 'DAM', 'GAL'],
               'ANT': ['DAM'],
               'SID': ['DAM', 'ARA'],
               'TYE': ['ARA'],
               'JER': ['ARA', 'NAB', 'PET'],
               'SII': [],
               'PET': ['JER'],
               'NAB': ['ARA', 'JER'],
               'MAU': ['CIR', 'SAH'],
               'CAR': ['CIR'],
               'THA': ['CIR'],
               'NUM': ['PHA', 'CIR'],
               'LEP': ['MAR', 'PHA'],
               'CYR': ['MEM', 'MAR'],
               'ALE': [],
               'MEM': ['MAR', 'CYR'],
               'BAY': ['MAR', 'SAH', 'PHA'],
               'THE': [],
               'COR': [],
               'SAD': [],
               'SIC': [],
               'CRE': [],
               'CYP': [],
               'BAL': []}
coast_routes = {'SAG': ['TAR', 'MAU'],
                'TAR': ['MAS', 'SAG'],
                'MAS': ['ETU', 'TAR'],
                'ETU': ['ROM', 'MAS'],
                'ROM': ['NEA', 'ETU'],
                'NEA': ['APU', 'SIC', 'ROM'],
                'APU': ['RAV', 'NEA'],
                'RAV': ['VEN', 'APU'],
                'VEN': ['DAL', 'RAV'],
                'DAL': ['EPI', 'VEN'],
                'EPI': ['ATH', 'DAL'],
                'ATH': ['MAC', 'SPA', 'EPI'],
                'SPA': ['ATH'],
                'MAC': ['BYZ', 'ATH'],
                'BYZ': ['DAC', 'BIT', 'MIL', 'MAC'],
                'DAC': ['CHE', 'BYZ'],
                'CHE': ['SIP', 'DAC'],
                'SIP': ['BIT', 'CHE'],
                'BIT': ['BYZ', 'SIP'],
                'MIL': ['ISA', 'BYZ'],
                'ISA': ['CAP', 'MIL'],
                'CAP': ['ANT', 'ISA'],
                'ANT': ['SID', 'CAP'],
                'SID': ['TYE', 'ANT'],
                'TYE': ['JER', 'SID'],
                'JER': ['SII', 'TYE'],
                'SII': ['THE', 'ALE', 'JER', 'PET'],
                'PET': ['SII', 'NAB'],
                'NAB': ['PET'],
                'MAU': ['CAR', 'SAG'],
                'CAR': ['THA', 'MAU'],
                'THA': ['NUM', 'CAR'],
                'NUM': ['LEP', 'THA'],
                'LEP': ['CYR', 'NUM'],
                'CYR': ['ALE', 'LEP'],
                'ALE': ['SII', 'THE', 'MEM', 'CYR'],
                'MEM': ['BAY', 'THE', 'ALE'],
                'BAY': ['THE', 'MEM'],
                'THE': ['SII', 'BAY', 'MEM', "ALE"],
                'COR': ['SAD'],
                'SAD': ['COR'],
                'SIC': ['NEA'],
                'CRE': [],
                'CYP': [],
                'BAL': []}
sea_routes = {'IBE': ['SAG', 'BER', 'MAU'],
              'BER': ['LIG', 'SAD', 'PUN', 'CAR', 'MAU', 'IBE', 'SAG', 'BAL'],
              'LIG': ['MAS', 'ETU', 'ROM', 'COR', 'TYN', 'SAD', 'BER', 'BAL', 'TAR'],
              'TYN': ['ROM', 'NEA', 'AUS', 'SIC', 'PUN', 'SAD', 'LIG', 'COR'],
              'PUN': ['SAD', 'TYN', 'SIC', 'AUS', 'GOT', 'THA', 'CAR', 'BER'],
              'ADR': ['VEN', 'DAL', 'EPI', 'ION', 'APU', 'RAV'],
              'ION': ['ADR', 'EPI', 'ATH', 'SPA', 'MES', 'AUS', 'NEA', 'APU'],
              'AUS': ['NEA', 'ION', 'MES', 'LIB', 'GOT', 'PUN', 'SIC', 'TYN'],
              'GOT': ['AUS', 'MES', 'LIB', 'GOS', 'LEP', 'NUM', 'THA', 'PUN'],
              'GOS': ['LIB', 'CYR', 'LEP', 'GOT'],
              'LIB': ['MES', 'CRE', 'EGY', 'ALE', 'CYR', 'GOS', 'GOT', 'AUS'],
              'MES': ['ION', 'SPA', 'AEG', 'CRE', 'LIB', 'GOT', 'AUS'],
              'AEG': ['MAC', 'BYZ', 'MIL', 'MIN', 'CRE', 'MES', 'SPA', 'ATH'],
              'BLA': ['CHE', 'SIP', 'BIT', 'BYZ', 'DAC'],
              'MIN': ['MIL', 'CIL', 'EGY', 'CRE', 'AEG'],
              'EGY': ['MIN', 'CIL', 'CYP', 'SYR', 'GOP', 'ALE', 'LIB', 'CRE'],
              'CIL': ['ISA', 'CAP', 'ANT', 'SID', 'SYR', 'CYP', 'EGY', 'MIN', 'MIL'],
              'SYR': ['CIL', 'SID', 'TYE', 'JER', 'GOP', 'EGY', 'CYP'],
              'GOP': ['SYR', 'JER', 'SII', 'THE', 'ALE', 'EGY'],
              'REE': ['SII', 'PET', 'NAB', 'THE'],
              'BAL': ['TAR', 'LIG', 'BER', 'SAG'],
              'SAG': ['BAL', 'BER', 'IBE'],
              'TAR': ['LIG', 'BAL'],
              'MAS': ['LIG'],
              'ETU': ['LIG'],
              'ROM': ['TYN', 'LIG'],
              'NEA': ['ION', 'AUS', 'TYN'],
              'APU': ['ADR', 'ION'],
              'RAV': ['ADR'],
              'VEN': ['ADR'],
              'DAL': ['ADR'],
              'EPI': ['ION', 'ADR'],
              'ATH': ['AEG', 'ION'],
              'SPA': ['AEG', 'MES', 'ION'],
              'MAC': ['AEG'],
              'BYZ': ['BLA', 'AEG'],
              'DAC': ['BLA'],
              'CHE': ['BLA'],
              'SIP': ['BLA'],
              'BIT': ['BLA'],
              'MIL': ['CIL', 'MIN', 'AEG'],
              'ISA': ['CIL'],
              'CAP': ['CIL'],
              'ANT': ['CIL'],
              'SID': ['SYR', 'CIL'],
              'TYE': ['SYR'],
              'JER': ['GOP', 'SYR'],
              'SII': ['GOP', 'REE'],
              'PET': ['REE'],
              'NAB': ['REE'],
              'MAU': ['IBE', 'BER'],
              'CAR': ['PUN', 'BER'],
              'THA': ['GOT', 'PUN'],
              'NUM': ['GOT'],
              'LEP': ['GOT', 'GOS'],
              'CYR': ['LIB', 'GOS'],
              'ALE': ['EGY', 'GOP', 'LIB'],
              'MEM': [],
              'BAY': [],
              'THE': ['GOP', 'REE'],
              'COR': ['LIG', 'TYN'],
              'SAD': ['LIG', 'TYN', 'PUN', 'BER'],
              'SIC': ['TYN', 'AUS', 'PUN'],
              'CRE': ['AEG', 'MIN', 'EGY', 'LIB', 'MES'],
              'CYP': ['CIL', 'SYR', 'EGY']}


def check_route_dictionaries():
    # check route dictionaries
    territories_set = set(territories)
    print('land')
    for key in land_routes.keys():
        territories.discard(key)
        for val in land_routes[key]:
            if key not in land_routes[val]:
                print('{} {}'.format(key, val))
            if val == key:
                print(key)
    print('coast')
    for key in coast_routes.keys():
        territories.discard(key)
        for val in coast_routes[key]:
            if key not in coast_routes[val]:
                print('{} {}'.format(key, val))
            if val == key:
                print(key)
    print('sea')
    for key in sea_routes.keys():
        territories.discard(key)
        for val in sea_routes[key]:
            if key not in sea_routes[val]:
                print('{} {}'.format(key, val))
            if val == key:
                print(key)
    print(territories_set)  # should be empty


move_regex = re.compile('^([AF]) (\w{3})-(\w{3})$')
convoyed_move_regex = re.compile('^A (\w{3})-(\w{3}) via convoy$')
hold_regex = re.compile('^([AF]) (\w{3}) H$')
convoy_regex = re.compile('^F (\w{3}) C (\w{3})-(\w{3})$')
support_hold_regex = re.compile('^([AF]) (\w{3}) S (\w{3})$')
support_move_regex = re.compile('^([AF]) (\w{3}) S (\w{3})-(\w{3})$')
support_convoyed_move_regex = re.compile('^([AF]) (\w{3}) S (\w{3})-(\w{3}) via convoy$')
build_regex = re.compile('^([AF]) (\w{3}) B$')
disband_regex = re.compile('^([AF]) (\w{3}) D$')
player_regex = re.compile('^\w[\w ]*#\d{4}$')


def read_order(order):
    if isinstance(order, tuple):
        order_str = ''
        for s in order:
            order_str += s + ' '
        return order_str
    return order


class InvalidPlayerException(Exception):
    pass


class InvalidOrderException(Exception):
    pass


class AncientMediterranean:
    admin = None
    players_locked = False
    players = {'red': None, 'blue': None, 'green': None, 'black': None, 'yellow': None}
    units_by_color = {'red': [('F', 'NEA'), ('A', 'ROM'), ('A', 'RAV')],
                      'blue': [('F', 'THA'), ('A', 'CIR'), ('A', 'CAR')],
                      'green': [('F', 'SPA'), ('A', 'ATH'), ('A', 'MAC')],
                      'black': [('F', 'SID'), ('A', 'ANT'), ('A', 'DAM')],
                      'yellow': [('F', 'ALE'), ('A', 'MEM'), ('A', 'THE')]}
    units_by_terr = {}
    units_to_retreat = {'red': set(), 'blue': set(), 'green': set(), 'black': set(), 'yellow': set()}
    orders = {'red': {}, 'blue': {}, 'green': {}, 'black': {}, 'yellow': {}}
    num_to_build = {'red': 0, 'blue': 0, 'green': 0, 'black': 0, 'yellow': 0}
    supply_centers_by_color = deepcopy(starting_supply_centers)
    supply_centers_by_terr = {terr: 'uncontrolled' for terr in supply_center_territories}
    year = 1
    season = 'spring'

    # TODO: set up git repo

    def __init__(self):
        self._generate_units_by_terr()
        for color in self.supply_centers_by_color.keys():
            for sc in self.supply_centers_by_color[color]:
                self.supply_centers_by_terr[sc] = color

    def _season_step(self, retreat):
        if self.season == 'build':
            self.season = 'spring'
            self.year += 1
        elif self.season == 'spring':
            if retreat:
                self.season = 'spring_retreat'
            self.season = 'fall'
        elif self.season == 'fall':
            if retreat:
                self.season = 'fall_retreat'
            self.season = 'build'
        elif self.season == 'spring_retreat':
            self.season = 'fall'
        elif self.season == 'fall_retreat':
            self.season = 'build'
        else:
            # TODO: maybe make a more descriptively named exception like IllegalSeasonException
            raise Exception('illegal season state {}'.format(self.season))
        return self.season + ' ' + str(self.year)

    def _game_step(self):
        # TODO: finish game cycle
        # TODO: control update function with discord bot and return messages like declaring winner or current game state
        retreat = False
        if self.season == 'build':
            # add new units and remove extra
            self._build_disband()
        elif self.season == 'spring':
            # move units to new territories and resolve conflicts
            # determine if a retreat phase is necessary
            pass
        elif self.season == 'fall':
            # move units to new territories and resolve conflicts
            # determine if a retreat phase is necessary
            # determine change in supply centers
            self._update_supply_centers()
            # check if any player controls 18
            self._check_for_winner()
            # calculate number of builds or disband orders needed
            pass
        elif self.season == 'spring_retreat':
            pass
        elif self.season == 'fall_retreat':
            pass
        # reset orders
        self.orders = {'red': {}, 'blue': {}, 'green': {}, 'black': {}, 'yellow': {}}
        self.units_to_retreat = {'red': set(), 'blue': set(), 'green': set(), 'black': set(), 'yellow': set()}
        self._generate_units_by_terr()
        self._season_step(retreat)

    def _retreat(self):
        # TODO: resolve retreat orders
        pass

    def _build_disband(self):
        for color in self.orders.keys():
            for order in self.orders[color]:
                _, territory, order_type, unit_type = order
                if order_type == 'build':
                    self.units_by_color[color] += (unit_type, territory)
                    self.units_by_terr[territory] = (unit_type, color)
                elif order_type == 'disband':
                    self.units_by_color[color].remove((unit_type, territory))
                    self.units_by_terr.pop(territory)
                else:
                    raise Exception('illegal order {} during build phase'.format(order))

    def _update_supply_centers(self):
        for color in self.units_by_color.keys():
            for unit in self.units_by_color[color]:
                terr = unit[1]
                if self.supply_centers_by_terr[terr] != 'uncontrolled':
                    self.supply_centers_by_color[color].remove(terr)
                self.supply_centers_by_terr[terr] = color
                self.supply_centers_by_color[color].add(terr)

    def _generate_units_by_terr(self):
        self.units_by_terr.clear()
        for color in self.units_by_color.keys():
            for unit in self.units_by_color[color]:
                self.units_by_terr[unit[1]] = (unit[0], color)

    def _check_for_winner(self):
        for c in self.supply_centers_by_color.keys():
            if len(self.supply_centers_by_color[c]) >= 18:
                winner = c
                win_str = '{} wins!!!'.format(self.players[winner])
                for color in self.units_by_color.keys():
                    if color != winner:
                        win_str += '\n{} is a pathetic loser'.format(self.players[color])
                return win_str
        return None

    def _unit_occupying(self, territory):
        if territory not in self.units_by_terr.keys():
            return None
        return self.units_by_terr[territory][0]

    def _convoy_possible(self, source, destination):
        if source not in territories:
            raise InvalidOrderException('territory {} unknown'.format(source))
        if destination not in territories:
            raise InvalidOrderException('territory {} unknown'.format(destination))
        if source not in coast_routes.keys():
            raise InvalidOrderException('only armies on coasts can be convoyed\n'
                                        '{} is not a coastal territory'.format(source))
        if destination not in coast_routes.keys():
            raise InvalidOrderException('armies can only be convoyed to coasts\n'
                                        '{} is not a coastal territory'.format(destination))
        stack = [(source, None)]
        checked = {source}
        while stack:
            cur = stack.pop()
            for adj in sea_routes[cur]:
                if adj == destination:
                    return True
                if adj in seas and adj not in checked:
                    checked.add(adj)
                    if self._unit_occupying(adj) == 'F':
                        stack += adj
        return False

    def _retreat_possible(self, source, destination):
        # TODO: figure out if the unit is allowed to retreat to the ordered territory
        self._check_adjacency(source, destination)
        pass

    def _check_adjacency(self, source, destination):
        if source not in territories:
            raise InvalidOrderException('territory {} unknown'.format(source))
        if destination not in territories:
            raise InvalidOrderException('territory {} unknown'.format(destination))

        if coast_routes.get(source) and destination in coast_routes.get(source):
            return
        unit_type = self._unit_occupying(source)
        if unit_type == 'A':
            if destination in seas:
                raise InvalidOrderException('armies cannot move to sea territories')
            if source not in land_routes.keys():
                raise InvalidOrderException('army not on land. yell at soren')
            if destination not in land_routes[source]:
                raise InvalidOrderException('{} and {} are not adjacent'.format(source, destination))
        elif unit_type == 'F':
            if destination in inlands:
                raise InvalidOrderException('fleets cannot move to inland territories')
            if source not in sea_routes.keys():
                raise InvalidOrderException('fleet not on coast or in seas. yell at soren')
            if destination not in sea_routes[source]:
                raise InvalidOrderException('{} and {} are not adjacent'.format(source, destination))
        else:
            raise InvalidOrderException('cannot order unoccupied territory {}'.format(source))

    def _check_ownership(self, territory, unit_type, color):
        if territory not in territories:
            raise InvalidOrderException('territory {} unknown'.format(territory))
        # check if unit exists on the source territory and which color it is
        if territory not in self.units_by_terr.keys():
            raise InvalidOrderException('territory {} unoccupied'.format(territory))
        unit = self.units_by_terr[territory]
        if unit_type != unit[0]:
            raise InvalidOrderException(
                'the unit in territory {} was ordered as {} but is {}'.format(territory, unit_type, unit[0]))
        if color != unit[1]:
            raise InvalidOrderException('you do not control the unit in the territory'.format(territory))

    def _interpret_order(self, order, color):
        print(order)
        match_move = move_regex.match(order)
        match_convoyed_move = convoyed_move_regex.match(order)
        match_hold = hold_regex.match(order)
        match_convoy = convoy_regex.match(order)
        match_support_hold = support_hold_regex.match(order)
        match_support_move = support_move_regex.match(order)
        match_support_convoyed_move = support_convoyed_move_regex.match(order)
        match_build = build_regex.match(order)
        match_disband = disband_regex.match(order)

        if self.season == 'build':
            # build
            if match_build:
                unit_type, territory = match_build.groups()
                if territory not in self.supply_centers_by_color[color]:
                    raise InvalidOrderException('you cannot build at {}, you do not control it'.format(territory))
                if territory not in starting_supply_centers[color]:
                    raise InvalidOrderException(
                        'you cannot build at {}, it is not one of your starting supply centers'.format(territory))
                if unit_type == 'F' and territory not in coast_routes.keys():
                    raise InvalidOrderException(
                        'you cannot build a fleet at the inland supply center {}'.format(territory))
                if territory in self.orders[color].keys() or len(self.orders[color]) < self.num_to_build[color]:
                    return color, territory, 'build', unit_type
                raise InvalidOrderException(
                    'you already reached your number of builds for this turn\n'
                    'reset your orders with !reset_orders to change your builds')

            # disband
            if match_disband:
                unit_type, territory = match_disband.groups()
                self._check_ownership(territory, unit_type, color)
                if -len(self.orders[color]) > self.num_to_build[color]:
                    return color, territory, 'disband', unit_type
                raise InvalidOrderException(
                    'you have already reached your number of disbands for this turn\n'
                    'reset your orders with !reset_orders to change your disbands')

            if match_move or match_convoyed_move or match_hold or match_convoy or match_support_hold or match_support_move or match_support_convoyed_move:
                raise InvalidOrderException('only build and disband orders are allowed during build phase')
            raise InvalidOrderException('order type not recognized')

        if self.season == 'spring_retreat' or self.season == 'fall_retreat':
            # disband
            if match_disband:
                unit_type, territory = match_move.groups()
                self._check_ownership(territory, unit_type, color)
                if territory not in self.units_to_retreat[color]:
                    raise InvalidOrderException(
                        'the unit in {} has not been dislodged, so you cant disband it'.format(territory))
                return color, territory, 'disband'

            # move
            if match_move:
                unit_type, source, destination = match_move.groups()
                self._check_ownership(source, unit_type, color)
                if source not in self.units_to_retreat[color]:
                    raise InvalidOrderException(
                        'the unit in {} has not been dislodged, so it cant retreat'.format(source))
                if not self._retreat_possible(source, destination):
                    raise InvalidOrderException(''.format(source, destination))
                return color, source, 'move', destination

            if match_convoyed_move or match_hold or match_convoy or match_support_hold or match_support_move or match_support_convoyed_move or match_build:
                raise InvalidOrderException('only move and disband orders are allowed during retreat phases')
            raise InvalidOrderException('order type not recognized')

        # move
        if match_move:
            unit_type, source, destination = match_move.groups()
            self._check_ownership(source, unit_type, color)
            self._check_adjacency(source, destination)
            return color, source, 'move', destination

        # convoyed_move
        if match_convoyed_move:
            unit_type, source, destination = match_convoyed_move.groups()
            self._check_ownership(source, unit_type, color)
            if not self._convoy_possible(source, destination):
                raise InvalidOrderException(
                    'there is no possible route via fleets at sea to convoy {} to {}'.format(source, destination))
            return color, source, 'convoyed_move', destination

        # hold
        if match_hold:
            unit_type, source = match_hold.groups()
            self._check_ownership(source, unit_type, color)
            return color, source, 'hold'

        # convoy
        if match_convoy:
            convoy_loc, source, destination = match_convoy.groups()
            self._check_ownership(convoy_loc, 'F', color)
            if convoy_loc not in seas:
                raise InvalidOrderException('fleet must be at sea to convoy')
            if not self._convoy_possible(source, destination):
                raise InvalidOrderException(
                    'there is no possible route via fleets at sea to convoy {} to {}'.format(source, destination))
            return color, convoy_loc, 'convoy', source, destination

        # support hold
        if match_support_hold:
            unit_type, source, destination = match_support_hold.groups()
            self._check_ownership(source, unit_type, color)
            self._check_adjacency(source, destination)
            if self._unit_occupying(destination) is None:
                raise InvalidOrderException('no unit in {} to support'.format(destination))
            return color, source, 'support_hold', destination

        # support move
        if match_support_move:
            unit_type, support_source, attack_source, destination = match_support_move.groups()
            self._check_ownership(support_source, unit_type, color)
            self._check_adjacency(support_source, destination)
            self._check_adjacency(attack_source, destination)
            return color, support_source, 'support_move', attack_source, destination

        # support convoyed move
        if match_support_convoyed_move:
            unit_type, support_source, attack_source, destination = match_support_convoyed_move.groups()
            self._check_ownership(support_source, unit_type, color)
            self._check_adjacency(support_source, destination)
            if attack_source not in territories:
                raise InvalidOrderException('territory {} unknown'.format(attack_source))
            attacking_type = self._unit_occupying(attack_source)
            if attacking_type is None:
                raise InvalidOrderException(
                    'attempting to support a convoyed move from {}, but that territory is unoccupied'.format(
                        attack_source))
            elif attacking_type is 'F':
                raise InvalidOrderException(
                    'attempting to support a convoyed move from {}, but that territory is occupied by a fleet'.format(
                        attack_source))
            if not self._convoy_possible(attack_source, destination):
                raise InvalidOrderException(
                    'there is no possible route via fleets at sea to convoy {} to {}'.format(attack_source,
                                                                                             destination))
            return color, support_source, 'support_convoyed_move', attack_source, destination

        if match_build or match_disband:
            raise InvalidOrderException('cannot build or disband during spring or fall seasons')
        raise InvalidOrderException('order type not recognized')

    def get_color(self, player):
        for c in self.players.keys():
            if self.players[c] == player:
                return c
        raise InvalidPlayerException('invalid player {}. assign color before issuing orders'.format(player))

    def add_order(self, player, order):
        try:
            color = self.get_color(player)
            order = self._interpret_order(order, color)
        except (InvalidPlayerException, InvalidOrderException) as e:
            return str(e)
        if not isinstance(order, tuple):
            return 'order "{}" not returned as a tuple. yell at soren to fix.'.format(order)
        territory = order[1]
        self.orders[color][territory] = order
        print(self.orders)
        return read_order(order)

    def reset_orders(self, player):
        try:
            color = self.get_color(player)
        except InvalidPlayerException as e:
            return str(e)
        self.orders[color] = {}

    def get_order(self, player, territory):
        try:
            color = self.get_color(player)
        except InvalidPlayerException as e:
            return str(e)
        if territory not in self.orders[color]:
            for unit in self.units_by_color[color]:
                if unit[1] == territory:
                    return '{} no order issued'.format(territory)
            return 'you dont control a unit in this territory, dork'
        return read_order(self.orders[color][territory])

    def get_my_orders(self, player):
        try:
            color = self.get_color(player)
        except InvalidPlayerException as e:
            return str(e)
        orders_str = ''
        for unit in self.units_by_color[color]:
            unit_terr = unit[1]
            if unit_terr in self.orders[color]:
                orders_str += read_order(self.orders[color][unit_terr]) + '\n'
            else:
                orders_str += unit[1] + ' no order issued' + '\n'
        if orders_str == '':
            orders_str = 'you dont have any units to order, fool.'
        return orders_str

    def get_my_units(self, player):
        try:
            color = self.get_color(player)
        except InvalidPlayerException as e:
            return str(e)
        units_str = ''
        for unit in self.units_by_color[color]:
            units_str += unit[0] + ' ' + unit[1] + '\n'
        if units_str == '':
            units_str = 'you dont have any units, loser.'
        return units_str

    def get_all_units(self):
        units_str = ''
        for color in self.units_by_color.keys():
            for unit in self.units_by_color[color]:
                units_str += color + ' ' + unit[0] + ' ' + unit[1] + '\n'
        if units_str == '':
            units_str = 'no units found (soren fucked up)'
        return units_str

    def get_my_supply_centers(self, player):
        try:
            color = self.get_color(player)
        except InvalidPlayerException as e:
            return str(e)
        s = ''
        for sc in self.supply_centers_by_color[color]:
            s += sc + '\n'
        if s == '':
            s = 'you dont have any supply centers, stupid.'
        return s

    def get_all_supply_centers(self):
        s = ''
        for color in self.supply_centers_by_color.keys():
            for sc in self.supply_centers_by_color[color]:
                s += color + ' ' + sc + '\n'
        if s == '':
            s = 'no supply centers found (soren fucked up)'
        return s

    def assign_player(self, player, color):
        if self.players_locked:
            return 'players are locked by the admin'
        if not player_regex.match(player):
            return 'invalid player {} must be of form AAAAA#0000\n' \
                   '(yell at soren if you see this)'.format(player)
        try:
            c = self.get_color(player)
            if c == color:
                return 'you were already assigned that color, you nincompoop'
            return 'you are already assigned the color {}\n' \
                   'remove your current color with !resign to claim a new one'.format(c)
        except InvalidPlayerException:
            if color not in self.players.keys():
                return 'invalid color: {}'.format(color)
            self.players[color] = player
            return 'player {} assigned color {}'.format(player, color)

    def remove_player(self, player):
        if self.players_locked:
            return 'players are locked by the admin'
        if not player_regex.match(player):
            return 'invalid player {} must be of form AAAAA#0000\n' \
                   '(yell at soren if you see this)'.format(player)
        try:
            color = self.get_color(player)
            self.players[color] = None
            return 'you have been removed from control of {}'.format(color)
        except InvalidPlayerException:
            return 'why are you trying to resign when you didnt control a color in the first place, you nitwit'

    def assign_admin(self, player):
        if not player_regex.match(player):
            return 'invalid player {} must be of form AAAAA#0000\n' \
                   '(yell at soren if you see this)'.format(player)
        if self.admin is None:
            self.admin = player
            return 'player {} assigned admin powers'.format(player)
        return 'cannot assign admin powers until {} relinquishes admin powers with !relinquish_admin'.format(self.admin)

    def relinquish_admin(self, player):
        if not player_regex.match(player):
            return 'invalid player {} must be of form AAAAA#0000\n' \
                   '(yell at soren if you see this)'.format(player)
        if player != self.admin:
            return 'dont try and relinquish admin powers you dont have, dummy. current admin is {}'.format(self.admin)
        if self.players_locked:
            self.players_locked = False
            self.admin = None
            return 'your admin powers have been relinquished. players unlocked.'
        self.admin = None
        return 'your admin powers have been relinquished'

    def lock_players(self, player):
        if player != self.admin:
            return 'locking players requires admin powers'
        self.players_locked = True
        return 'players locked'

    def unlock_players(self, player):
        if player != self.admin:
            return 'unlocking players requires admin powers'
        self.players_locked = False
        return 'players unlocked'

    def kick_player(self, admin_name, player):
        if admin_name != self.admin:
            return 'you arent admin, imbecile'
        if not player_regex.match(player):
            return 'invalid player {} must be of form AAAAA#0000\n'.format(player)
        try:
            color = self.get_color(player)
        except InvalidPlayerException:
            return 'you cant kick a player not assigned a color, moron'
        return 'player {} kicked from {}'.format(player, color)
