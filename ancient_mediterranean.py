import re
import json
from copy import deepcopy
from collections import namedtuple
from order_resolver import OrderSolver

territories = {'GAU', 'RHA', 'SAM', 'VIN', 'ILL', 'LUS', 'ARM', 'GAL', 'DAM', 'ARA', 'CIR', 'SAH', 'PHA', 'MAR', 'SAG',
               'TAR', 'MAS', 'ETR', 'ROM', 'NEA', 'APU', 'RAV', 'VEN', 'DAL', 'EPI', 'ATH', 'SPA', 'MAC', 'BYZ', 'DAC',
               'CHE', 'SIP', 'BIT', 'MIL', 'ISA', 'CAP', 'ANT', 'SID', 'TYE', 'JER', 'SII', 'PET', 'NAB', 'MAU', 'CAR',
               'THA', 'NUM', 'LEP', 'CYR', 'ALE', 'MEM', 'BAY', 'THE', 'COR', 'SAD', 'SIC', 'CRE', 'CYP', 'IBE', 'BER',
               'LIG', 'TYN', 'PUN', 'ADR', 'ION', 'AUS', 'GOT', 'GOS', 'LIB', 'MES', 'AEG', 'BLA', 'MIN', 'EGY',
               'CIL', 'SYR', 'GOP', 'REE', 'BAL'}

land_locked = {'GAU', 'RHA', 'SAM', 'VIN', 'ILL', 'LUS', 'ARM', 'GAL', 'DAM', 'ARA', 'CIR', 'SAH', 'PHA', 'MAR'}
coasts = {'SAG', 'TAR', 'MAS', 'ETR', 'ROM', 'NEA', 'APU', 'RAV', 'VEN', 'DAL', 'EPI', 'ATH', 'SPA', 'MAC', 'BYZ',
          'DAC', 'CHE', 'SIP', 'BIT', 'MIL', 'ISA', 'CAP', 'ANT', 'SID', 'TYE', 'JER', 'SII', 'PET', 'NAB', 'MAU',
          'CAR', 'THA', 'NUM', 'LEP', 'CYR', 'ALE', 'MEM', 'BAY', 'THE', 'COR', 'SAD', 'SIC', 'CRE', 'CYP'}
seas = {'IBE', 'BER', 'LIG', 'TYN', 'PUN', 'ADR', 'ION', 'AUS', 'GOT', 'GOS', 'LIB', 'MES', 'AEG', 'BLA', 'MIN', 'EGY',
        'CIL', 'SYR', 'GOP', 'REE', 'BAL'}
supply_center_territories = {'VIN', 'DAM', 'CIR', 'SAG', 'MAS', 'ROM', 'NEA', 'RAV', 'DAL', 'ATH', 'SPA', 'MAC', 'BYZ',
                             'CHE', 'SIP', 'MIL', 'ANT', 'SID', 'TYE', 'JER', 'PET', 'CAR', 'THA', 'NUM', 'LEP', 'CYR',
                             'ALE', 'MEM', 'THE', 'SAD', 'SIC', 'CRE', 'CYP', 'BAL'}
starting_supply_centers = {'red': {'NEA', 'ROM', 'RAV'},
                           'blue': {'THA', 'CIR', 'CAR'},
                           'green': {'SPA', 'ATH', 'MAC'},
                           'black': {'SID', 'ANT', 'DAM'},
                           'yellow': {'ALE', 'MEM', 'THE'}}
land_routes = {'GAU': ['RHA', 'MAS', 'TAR', 'LUS'],
               'RHA': ['SAM', 'VIN', 'VEN', 'ETR', 'MAS', 'GAU'],
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
               'ETR': ['RHA', 'VEN', 'RAV'],
               'ROM': ['RAV', 'APU'],
               'NEA': [],
               'APU': ['ROM'],
               'RAV': ['ROM', 'ETR'],
               'VEN': ['RHA', 'VIN', 'ETR'],
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
                'MAS': ['ETR', 'TAR'],
                'ETR': ['ROM', 'MAS'],
                'ROM': ['NEA', 'ETR'],
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
              'LIG': ['MAS', 'ETR', 'ROM', 'COR', 'TYN', 'SAD', 'BER', 'BAL', 'TAR'],
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
              'ETR': ['LIG'],
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
    territories_set = deepcopy(territories)
    print('land')
    for key in land_routes.keys():
        territories_set.discard(key)
        for val in land_routes[key]:
            if key not in land_routes[val]:
                print('{} {}'.format(key, val))
            if val == key:
                print(key)
    print('coast')
    for key in coast_routes.keys():
        territories_set.discard(key)
        for val in coast_routes[key]:
            if key not in coast_routes[val]:
                print('{} {}'.format(key, val))
            if val == key:
                print(key)
    print('sea')
    for key in sea_routes.keys():
        territories_set.discard(key)
        for val in sea_routes[key]:
            if key not in sea_routes[val]:
                print('{} {}'.format(key, val))
            if val == key:
                print(key)
    print(territories_set)  # should be empty


move_regex = re.compile('^([AF]) +(\w{3})-(\w{3})$')
convoyed_move_regex = re.compile('^A +(\w{3})-(\w{3}) +VIA +CONVOY$')
hold_regex = re.compile('^([AF]) +(\w{3}) +H$')
convoy_regex = re.compile('^F (\w{3}) +C +(\w{3})-(\w{3})$')
support_hold_regex = re.compile('^([AF]) +(\w{3}) +S +(\w{3})$')
support_move_regex = re.compile('^([AF]) +(\w{3}) +S +(\w{3})-(\w{3})$')
support_convoyed_move_regex = re.compile('^([AF]) +(\w{3}) +S +(\w{3})-(\w{3}) +VIA +CONVOY$')
build_regex = re.compile('^([AF]) +(\w{3}) +B$')
disband_regex = re.compile('^([AF]) +(\w{3}) +D$')
add_supply_center_regex = re.compile('^ADD +SUPPLY +CENTER +(\w{3})$')
remove_supply_center_regex = re.compile('^REMOVE +SUPPLY +CENTER +(\w{3})$')
set_season_regex = re.compile('^SET +SEASON +(\w+)$')
set_year_regex = re.compile('^SET +YEAR +(\d+)$')

add_retreat_regex = re.compile('^([AF]) +(\w{3}) RETREAT +(\w{3})$')
remove_retreat_regex = re.compile('^REMOVE +RETREAT +(\w{3})$')
add_standoff_regex = re.compile('^ADD +STANDOFF +(\w{3})$')
remove_standoff_regex = re.compile('^REMOVE +STANDOFF +(\w{3})$')

player_regex = re.compile('^\w[\w ]*#\d{4}$')
Order = namedtuple('Order', 'source order_type extra_info')
valid_seasons = ['spring', 'spring_retreat', 'fall', 'fall_retreat', 'build']


def read_order(order):
    order_str = [order.source, order.order_type]
    if order.order_type in {'move', 'convoyed_move', 'support_hold', 'build'}:
        order_str.append(order.extra_info)
    elif order.order_type in {'convoy', 'support_move', 'support_convoyed_move'}:
        order_str.append(order.extra_info[0])
        order_str.append(order.extra_info[1])
    return ' '.join(order_str)


def _convoy_possible2(source, destination, convoying_fleets):
    stack = [source]
    checked = set()
    while stack:
        cur = stack.pop()
        for adj in sea_routes.get(cur, set()):
            if adj == destination:
                return True
            if adj in convoying_fleets and adj not in checked:
                checked.add(adj)
                stack += adj
    return False


class AdministrativeException(Exception):
    pass


class InvalidOrderException(Exception):
    pass


class InvalidPlayerException(Exception):
    pass


class AncientMediterranean:
    def __init__(self, load_path=None):
        self.admin = None
        self.colors = {'red', 'blue', 'green', 'black', 'yellow'}
        self.players_locked = False
        self.players = {'red': None, 'blue': None, 'green': None, 'black': None, 'yellow': None}
        self.units_by_color = {'red': {('F', 'NEA'), ('A', 'ROM'), ('A', 'RAV')},  # (unit type, territory)
                               'blue': {('F', 'THA'), ('A', 'CIR'), ('A', 'CAR')},
                               'green': {('F', 'SPA'), ('A', 'ATH'), ('A', 'MAC')},
                               'black': {('F', 'SID'), ('A', 'ANT'), ('A', 'DAM')},
                               'yellow': {('F', 'ALE'), ('A', 'MEM'), ('A', 'THE')}}
        self.units_by_terr = {}  # (unit type, color)
        self.retreating_units = {'red': {}, 'blue': {}, 'green': {}, 'black': {},
                                 'yellow': {}}  # (dislodging_unit, unit_type)
        self.orders = {'red': {}, 'blue': {}, 'green': {}, 'black': {}, 'yellow': {}}  # (source, order type, ...)
        self.num_to_build = {'red': 0, 'blue': 0, 'green': 0, 'black': 0, 'yellow': 0}
        self.supply_centers_by_color = deepcopy(starting_supply_centers)
        self.supply_centers_by_terr = {terr: 'uncontrolled' for terr in supply_center_territories}
        self.season = 'spring'
        self.year = 1
        self.standoffs = set()
        if load_path:
            self.load(load_path)
        else:
            # add starting units to units_by_terr
            for color in self.colors:
                for unit in self.units_by_color[color]:
                    self.units_by_terr[unit[1]] = (unit[0], color)
            # add starting supply centers to supply_centers_by_terr
            for color in self.colors:
                for sc in self.supply_centers_by_color[color]:
                    self.supply_centers_by_terr[sc] = color
        self.order_resolver = OrderSolver(self.units_by_color, self.units_by_terr)

    def _season_step(self, retreat):
        if self.season == 'build':
            self.season = 'spring'
            self.year += 1
        elif self.season == 'spring':
            self.season = 'fall'
            if retreat:
                self.season = 'spring_retreat'
        elif self.season == 'fall':
            self.season = 'build'
            if retreat:
                self.season = 'fall_retreat'
        elif self.season == 'spring_retreat':
            self.season = 'fall'
        elif self.season == 'fall_retreat':
            self.season = 'build'
        else:
            raise Exception('illegal season state {}\n'
                            'valid seasons are {}'.format(self.season, valid_seasons))
        return self.season + ' ' + str(self.year).zfill(2)

    def status(self):
        ret_str = ['{} {}'.format(self.season, str(self.year).zfill(2))]
        if self.season in {'spring', 'fall'}:
            for color in self.colors:
                ret_str.append('{}: {} units, {} orders submitted'.format(color, len(self.units_by_color[color]),
                                                                          len(self.orders[color])))
        elif self.season in {'spring_retreat', 'fall_retreat'}:
            for color in self.colors:
                ret_str.append('{}: {} units retreating, {} orders submitted'
                               .format(color, str(len(self.retreating_units[color])), len(self.orders[color])))
        elif self.season == 'build':
            for color, num in self.num_to_build.items():
                if num < 0:
                    ret_str.append('{}: {} units to disband, {} orders submitted'.format(color, abs(num),
                                                                                         len(self.orders[color])))
                else:
                    ret_str.append('{}: {} units to build, {} orders submitted'.format(color, num,
                                                                                       len(self.orders[color])))
        if not ret_str:
            return 'no status detected. yell at soren.'
        return '\n'.join(ret_str)

    def _flatten_normal_orders(self):
        flat = set()
        for color in self.colors:
            for order in self.orders[color].values():
                flat.add(order)
        return flat

    def _flatten_retreat_orders(self):
        flat = set()
        for color in self.colors:
            for order in self.orders[color].values():
                source, order_type, extra_info = order
                _, unit_type = self.retreating_units[color][source]
                new_order = (source, order_type, extra_info, color, unit_type)
                flat.add(new_order)
        return flat

    def game_step(self, admin, fp):
        if admin != self.admin:
            raise AdministrativeException("you aren't admin, imbecile")
        overview = ['overview of {} {}'.format(self.season, str(self.year).zfill(2))]
        # list out orders
        for color in self.colors:  # TODO: make each player's orders appear in one line like color: order order order...
            overview.append(
                '{}: {}'.format(color, ', '.join([read_order(order) for order in self.orders[color].values()])))
        retreat = False
        if self.season in {'spring', 'fall'}:
            # move units to new territories and resolve conflicts
            dislodged_units, standoffs, summary = self.order_resolver.resolve_normal_orders(
                self._flatten_normal_orders())
            overview += summary
            self.standoffs.clear()
            for territory in standoffs:
                self.standoffs.add(territory)
                overview.append('standoff occurred in {}'.format(territory))
            # add dislodged units to retreating units
            for color in self.colors:
                self.retreating_units[color].clear()
            for dislodged_unit in dislodged_units.keys():
                dislodging_unit, unit_type, color = dislodged_units[dislodged_unit]
                if self._anywhere_to_retreat(dislodged_unit, dislodging_unit, unit_type):
                    retreat = True
                    self.retreating_units[color][dislodged_unit] = (dislodging_unit, unit_type)
                    overview.append('{} must order {} to retreat or disband'.format(color, dislodged_unit))
                else:
                    self.order_resolver.remove_unit(dislodged_unit)
                    overview.append('{} {} in {} was dislodged, but has no possible paths of retreat, '
                                    'so it was disbanded.'.format(color, unit_type, dislodged_unit))
        elif self.season in {'spring_retreat', 'fall_retreat'}:
            overview += self.order_resolver.resolve_retreat_orders(self._flatten_retreat_orders())
            # reset retreating_units
            for units in self.retreating_units.values():
                units.clear()
        elif self.season == 'build':
            # add new and remove extra units
            overview += self.order_resolver.build_disband(self.orders)

        if (self.season == 'fall' and not retreat) or self.season == 'fall_retreat':
            # determine change in supply centers
            overview += self._update_supply_centers()
            # check if any player controls 18
            overview += self._check_for_winner()
            # calculate number of units to build or disband
            for color in self.colors:
                num_supply_centers = len(self.supply_centers_by_color[color])
                num_units = len(self.units_by_color[color])
                num_builds = num_supply_centers - num_units
                self.num_to_build[color] = num_builds
                if num_builds < 0:
                    overview.append('{}: {} units to disband ({} supply centers {} units)'
                                    .format(color, abs(num_builds), num_supply_centers, num_units))
                else:
                    overview.append('{}: {} units to build ({} supply centers {} units)'
                                    .format(color, num_builds, num_supply_centers, num_units))

        # reset orders
        for order_dict in self.orders.values():
            order_dict.clear()
        self._season_step(retreat)
        self.save(fp)
        overview.append('game state saved')
        overview.append('next phase is {} {}'.format(self.season, str(self.year).zfill(2)))
        return '\n'.join(overview)

    def _update_supply_centers(self):
        # loop through each color's units and check if they took control of uncontrolled supply centers
        # or another player's supply centers
        summary = []
        for color in self.colors:
            for unit in self.units_by_color[color]:
                territory = unit[1]
                if territory not in supply_center_territories:
                    continue
                old_color = self.supply_centers_by_terr[territory]
                if old_color == color:
                    continue
                elif old_color == 'uncontrolled':
                    summary.append('{} gained control of the uncontrolled supply center at {}'.format(color, territory))
                elif old_color != color:
                    summary.append('{} stole the supply center at {} from {}'.format(color, territory, old_color))
                    self.supply_centers_by_color[old_color].remove(territory)
                self.supply_centers_by_terr[territory] = color
                self.supply_centers_by_color[color].add(territory)
        return summary

    def _check_for_winner(self):
        win_str = []
        for c in self.supply_centers_by_color.keys():
            if len(self.supply_centers_by_color[c]) >= 18:
                winner = c
                win_str.append('{} wins!!!'.format(self.players[winner]))
                for color in self.colors:
                    if color != winner:
                        win_str.append('{} is a pathetic loser'.format(self.players[color]))
        return win_str

    def _unit_occupying(self, territory):  # return self.units_by_terr.get(territory, [None])[0]
        if self.units_by_terr.get(territory):
            return self.units_by_terr[territory][0]
        return None

    def _convoy_possible(self, source, destination):
        if source not in territories:
            raise InvalidOrderException('territory {} unknown'.format(source))
        if destination not in territories:
            raise InvalidOrderException('territory {} unknown'.format(destination))
        if coast_routes.get(source) is None:
            raise InvalidOrderException('only armies on coasts can be convoyed\n'
                                        '{} is not a coastal territory'.format(source))
        if coast_routes.get(destination) is None:
            raise InvalidOrderException('armies can only be convoyed to coasts\n'
                                        '{} is not a coastal territory'.format(destination))
        stack = [source]
        checked = {source}
        while stack:
            cur = stack.pop()
            for adj in sea_routes.get(cur, set()):
                if adj == destination:
                    return True
                if adj in seas and adj not in checked:
                    checked.add(adj)
                    if self._unit_occupying(adj) == 'F':
                        stack.append(adj)
        return False

    def _anywhere_to_retreat(self, dislodged_unit, dislodging_unit, unit_type):
        # check all adjacent territories to see if the dislodged unit has any territory it can retreat to.
        # it cannot retreat to the territory that the unit that dislodged it attacked from, a territory where a
        # standoff took place, or an occupied territory.
        for adj in coast_routes.get(dislodged_unit, set()):
            if adj != dislodging_unit and adj not in self.standoffs and self.units_by_terr.get(adj) is None:
                return True
        if unit_type == 'A':
            for adj in land_routes[dislodged_unit]:
                if adj != dislodging_unit and adj not in self.standoffs and self.units_by_terr.get(adj) is None:
                    return True
        elif unit_type == 'F':
            for adj in sea_routes[dislodged_unit]:
                if adj != dislodging_unit and adj not in self.standoffs and self.units_by_terr.get(adj) is None:
                    return True
        return False

    def _retreat_possible(self, source, destination, color):
        dislodging_unit, unit_type = self.retreating_units[color][source]
        self._check_adjacency(source, destination, unit_type_override=unit_type)
        if self.units_by_terr.get(destination):
            raise InvalidOrderException('cannot retreat into an occupied territory')
        if destination == dislodging_unit:
            raise InvalidOrderException('cannot retreat into the territory that the dislodging unit attacked from')
        if destination in self.standoffs:
            raise InvalidOrderException('cannot retreat into a territory where a standoff took place')

    def _check_adjacency(self, source, destination, unit_type_override=None):
        if source not in territories:
            raise InvalidOrderException('territory {} unknown'.format(source))
        if destination not in territories:
            raise InvalidOrderException('territory {} unknown'.format(destination))

        if destination in coast_routes.get(source, set()):
            return
        if unit_type_override is None:
            unit_type = self._unit_occupying(source)
        else:
            unit_type = unit_type_override
        if unit_type == 'A':
            if destination in seas:
                raise InvalidOrderException("armies can't move to sea territories")
            if land_routes.get(source) is None:
                raise InvalidOrderException('army not on land. yell at soren')
            if destination not in land_routes[source]:
                raise InvalidOrderException('{} and {} are not adjacent'.format(source, destination))
        elif unit_type == 'F':
            if destination in land_locked:
                raise InvalidOrderException("fleets can't move to inland territories")
            if sea_routes.get(source) is None:
                raise InvalidOrderException('fleet not on coast or in seas. yell at soren')
            if destination not in sea_routes[source]:
                raise InvalidOrderException('{} and {} are not adjacent'.format(source, destination))
        else:
            raise InvalidOrderException('cannot order unoccupied territory {}'.format(source))

    def _check_ownership(self, territory, unit_type, color):
        if territory not in territories:
            raise InvalidOrderException('territory {} unknown'.format(territory))
        # check if unit exists on the source territory and which color it is
        if self.units_by_terr.get(territory) is None:
            raise InvalidOrderException('territory {} unoccupied'.format(territory))
        actual_unit_type, actual_color = self.units_by_terr[territory]
        if unit_type != actual_unit_type:
            raise InvalidOrderException(
                'the unit in territory {} was ordered as {} but is {}'.format(territory, unit_type, actual_unit_type))
        if color != actual_color:
            raise InvalidOrderException("you don't control the unit in the territory".format(territory))

    def _check_retreat(self, territory, unit_type, color):
        if territory not in territories:
            raise InvalidOrderException('territory {} unknown'.format(territory))
        if territory not in self.retreating_units[color].keys():
            raise InvalidOrderException(
                'the unit in {} has not been dislodged, so you cant disband it'.format(territory))
        _, actual_unit_type = self.retreating_units[color][territory]
        if unit_type != actual_unit_type:
            raise InvalidOrderException(
                'the unit in territory {} was ordered as {} but is {}'.format(territory, unit_type,
                                                                              actual_unit_type))

    def _interpret_order(self, order, color):
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
                    raise InvalidOrderException("you can't build at {}, you don't control it".format(territory))
                if territory not in starting_supply_centers[color]:
                    raise InvalidOrderException(
                        "you can't build at {}, it is not one of your starting supply centers".format(territory))
                if unit_type == 'F' and coast_routes.get(territory) is None:
                    raise InvalidOrderException(
                        "you can't build a fleet at the inland supply center {}".format(territory))
                if self.orders[color].get(territory) is not None or len(self.orders[color]) < self.num_to_build[color]:
                    return Order(territory, 'build', unit_type)
                raise InvalidOrderException(
                    'you already reached your number of builds, {}, for this turn\n'
                    'reset your orders with !reset_orders to change your builds'.format(self.num_to_build[color]))

            # disband
            if match_disband:
                unit_type, territory = match_disband.groups()
                self._check_ownership(territory, unit_type, color)
                if -len(self.orders[color]) > self.num_to_build[color]:
                    return Order(territory, 'disband', unit_type)
                raise InvalidOrderException(
                    'you have already reached your number of disbands, {}, for this turn\n'
                    'reset your orders with !reset_orders to change your disbands'.format(self.num_to_build[color]))

            if match_move or match_convoyed_move or match_hold or match_convoy or match_support_hold \
                    or match_support_move or match_support_convoyed_move:
                raise InvalidOrderException('only build and disband orders are allowed during build phase')
            raise InvalidOrderException('order type not recognized')

        if self.season == 'spring_retreat' or self.season == 'fall_retreat':
            # disband
            if match_disband:
                unit_type, territory = match_disband.groups()
                self._check_retreat(territory, unit_type, color)
                return Order(territory, 'disband', None)

            # move
            if match_move:
                unit_type, source, destination = match_move.groups()
                self._check_retreat(source, unit_type, color)
                self._retreat_possible(source, destination, color)
                return Order(source, 'move', destination)

            if match_convoyed_move or match_hold or match_convoy or match_support_hold or match_support_move \
                    or match_support_convoyed_move or match_build:
                raise InvalidOrderException('only move and disband orders are allowed during retreat phases')
            raise InvalidOrderException('order type not recognized')

        # move
        if match_move:
            unit_type, source, destination = match_move.groups()
            self._check_ownership(source, unit_type, color)
            self._check_adjacency(source, destination)
            return Order(source, 'move', destination)

        # convoyed_move
        if match_convoyed_move:
            source, destination = match_convoyed_move.groups()
            self._check_ownership(source, 'A', color)
            if not self._convoy_possible(source, destination):
                raise InvalidOrderException(
                    'there is no possible route via fleets at sea to convoy {} to {}'.format(source, destination))
            return Order(source, 'convoyed_move', destination)

        # hold
        if match_hold:
            unit_type, source = match_hold.groups()
            self._check_ownership(source, unit_type, color)
            return Order(source, 'hold', None)

        # convoy
        if match_convoy:
            convoy_loc, source, destination = match_convoy.groups()
            self._check_ownership(convoy_loc, 'F', color)
            if convoy_loc not in seas:
                raise InvalidOrderException('fleet must be at sea to convoy')
            if not self._convoy_possible(source, destination):
                raise InvalidOrderException(
                    'there is no possible route via fleets at sea to convoy {} to {}'.format(source, destination))
            return Order(convoy_loc, 'convoy', (source, destination))

        # support hold
        if match_support_hold:
            unit_type, source, destination = match_support_hold.groups()
            self._check_ownership(source, unit_type, color)
            self._check_adjacency(source, destination)
            if self._unit_occupying(destination) is None:
                raise InvalidOrderException('no unit in {} to support'.format(destination))
            return Order(source, 'support_hold', destination)

        # support move
        if match_support_move:
            unit_type, support_source, attack_source, destination = match_support_move.groups()
            self._check_ownership(support_source, unit_type, color)
            self._check_adjacency(support_source, destination)
            self._check_adjacency(attack_source, destination)
            return Order(support_source, 'support_move', (attack_source, destination))

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
            return Order(support_source, 'support_convoyed_move', (attack_source, destination))

        if match_build or match_disband:
            raise InvalidOrderException('cannot build or disband during spring or fall seasons')
        raise InvalidOrderException('order type not recognized')

    def get_color(self, player):
        for c in self.players.keys():
            if self.players[c] == player:
                return c
        raise InvalidPlayerException('invalid player {}. assign color before issuing orders'.format(player))

    def add_order(self, player, order_str):
        color = self.get_color(player)
        order = self._interpret_order(order_str.strip().upper(), color)
        if not isinstance(order, Order):
            raise InvalidOrderException('order "{}" not of type Order. yell at soren to fix.'.format(order))
        self.orders[color][order.source] = order
        return read_order(order)

    def reset_orders(self, player):
        color = self.get_color(player)
        self.orders[color].clear()
        return 'orders reset'

    def get_order(self, player, territory):
        if territory not in territories:
            raise AdministrativeException('invalid territory {}'.format(territory))
        if self.units_by_terr.get(territory) is None:
            return 'no unit in {}'.format(territory)
        _, color = self.units_by_terr[territory]
        if color != self.get_color(player):
            raise AdministrativeException("you don't control a unit in this territory, dork")
        if territory not in self.orders[color].keys():
            return '{} no order issued'.format(territory)
        return read_order(self.orders[color][territory])

    def get_my_orders(self, player):
        color = self.get_color(player)
        order_descriptions = []
        if self.season in {'spring', 'fall'}:
            for unit_type, territory in self.units_by_color[color]:
                order = self.orders[color].get(territory)
                if order:
                    order_descriptions.append(read_order(order))
                else:
                    order_descriptions.append('{} in {} no order issued'.format(unit_type, territory))
            if not order_descriptions:
                return "you don't have any units to order, fool."
        elif self.season in {'spring_retreat', 'fall_retreat'}:
            for units in self.retreating_units[color]:
                for unit in units.keys():
                    order = self.orders[color].get(unit)
                    if order:
                        order_descriptions.append(read_order(order))
                    else:
                        _, unit_type = units[unit]
                        order_descriptions.append('{} in {} no order issued'.format(unit_type, unit))
            if not order_descriptions:
                return "you don't have any retreating units to order."
        elif self.season == 'build':
            num = self.num_to_build[color]
            if num < 0:
                order_descriptions.append('you have {} units to disband'.format(abs(num)))
            else:
                order_descriptions.append('you have {} units to build'.format(num))
            submitted_orders = self.orders[color]
            for _, order in submitted_orders.items():
                order_descriptions.append(read_order(order))
        return '\n'.join(order_descriptions)

    def get_my_units(self, player):
        color = self.get_color(player)
        units_str = []
        for unit in self.units_by_color[color]:
            units_str.append('{} {}'.format(*unit))
        if not units_str:
            return "you don't have any units, loser."
        return '\n'.join(units_str)

    def get_all_units(self):
        unit_descriptions = []
        for color, units in self.units_by_color.items():
            unit_descriptions += ['{} {} {}'.format(color, *unit) for unit in units]
        if not unit_descriptions:
            return 'no units found (soren fucked up)'
        return '\n'.join(unit_descriptions)

    def get_my_supply_centers(self, player):
        color = self.get_color(player)
        s = ' '.join(self.supply_centers_by_color[color])
        if s == '':
            return "you don't have any supply centers, stupid."
        return s

    def get_all_supply_centers(self):
        s = []
        for color, supply_centers in self.supply_centers_by_color.items():
            s.append('{}: {} - {}'.format(color, len(self.supply_centers_by_color[color]),
                                          ' '.join(self.supply_centers_by_color[color])))
        if not s:
            return 'no supply centers found (soren fucked up)'
        return '\n'.join(s)

    def assign_player(self, player, color):
        if self.players_locked:
            raise AdministrativeException('players are locked by the admin')
        if not player_regex.match(player):
            raise AdministrativeException('invalid player {} must be of form AAAAA#0000\n'
                                          '(yell at soren if you see this)'.format(player))
        try:
            c = self.get_color(player)
            if c == color:
                raise AdministrativeException('you were already assigned that color, you nincompoop')
            raise AdministrativeException('you are already assigned the color {}\n'
                                          'remove your current color with !resign to claim a new one'.format(c))
        except InvalidPlayerException:
            if color not in self.players.keys():
                raise AdministrativeException('invalid color: {}'.format(color))
            self.players[color] = player
            return 'player {} assigned color {}'.format(player, color)

    def remove_player(self, player):
        if self.players_locked:
            raise AdministrativeException('players are locked by the admin')
        if not player_regex.match(player):
            raise AdministrativeException('invalid player {} must be of form AAAAA#0000\n'
                                          '(yell at soren if you see this)'.format(player))
        try:
            color = self.get_color(player)
            self.players[color] = None
            return 'you have been removed from control of {}'.format(color)
        except InvalidPlayerException:
            raise AdministrativeException(
                'why are you trying to resign when you didnt control a color in the first place, you nitwit?')

    def assign_admin(self, player):
        if not player_regex.match(player):
            raise AdministrativeException('invalid player {} must be of form AAAAA#0000\n'
                                          '(yell at soren if you see this)'.format(player))
        if self.admin is None:
            self.admin = player
            return 'player {} assigned admin powers'.format(player)
        raise AdministrativeException(
            'cannot assign admin powers until {} relinquishes admin powers with !relinquish_admin'.format(self.admin))

    def relinquish_admin(self, player):
        if not player_regex.match(player):
            raise AdministrativeException('invalid player {} must be of form AAAAA#0000\n'
                                          '(yell at soren if you see this)'.format(player))
        if player != self.admin:
            raise AdministrativeException(
                "don't try and relinquish admin powers you don't have, dummy. current admin is {}".format(self.admin))
        self.admin = None
        msg = 'your admin powers have been relinquished.'
        if self.players_locked:
            self.players_locked = False
            msg += ' players unlocked.'
        return msg

    def lock_players(self, player):
        if player != self.admin:
            raise AdministrativeException('locking players requires admin powers')
        self.players_locked = True
        return 'players locked'

    def unlock_players(self, player):
        if player != self.admin:
            raise AdministrativeException('unlocking players requires admin powers')
        self.players_locked = False
        return 'players unlocked'

    def kick_player(self, admin, player):
        if admin != self.admin:
            raise AdministrativeException("you aren't admin, imbecile")
        if not player_regex.match(player):
            raise AdministrativeException('invalid player {} must be of form AAAAA#0000\n'.format(player))
        try:
            color = self.get_color(player)
            self.players[color] = None
            return '{} has been removed from control of {}'.format(player, color)
        except InvalidPlayerException:
            raise AdministrativeException('you cant kick a player not assigned a color, moron')

    def save(self, fp):
        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        data = [self.admin, self.players_locked, self.players, self.units_by_color, self.units_by_terr,
                self.retreating_units, self.orders, self.num_to_build, self.supply_centers_by_color,
                self.supply_centers_by_terr, self.season, self.year, self.standoffs]
        with open(fp, 'w') as file:
            json.dump(data, file, default=set_default)

    def load(self, fp):
        with open(fp, 'r') as file:
            self.admin, self.players_locked, self.players, units_by_color, units_by_terr, retreating_units, orders, \
            self.num_to_build, supply_centers_by_color, self.supply_centers_by_terr, self.season, self.year, \
            standoffs = json.load(file)
            # json only stores lists and dictionaries. other data structures need to be adjusted manually.
            self.units_by_terr.clear()
            for color in self.colors:
                # convert units from lists to tuples
                self.units_by_color[color].clear()
                for unit in units_by_color[color]:
                    self.units_by_color[color].add(tuple(unit))
                    self.units_by_terr[unit[1]] = (unit[0], color)
                # convert retreating units from lists to tuples
                self.retreating_units[color].clear()
                for territory, info in retreating_units[color].items():
                    self.retreating_units[color][territory] = tuple(info)
                # supply centers requires sets
                self.supply_centers_by_color[color] = set(supply_centers_by_color[color])
                # convert orders from lists to Order namedtuple
                self.orders[color].clear()
                for territory, order in orders[color].items():
                    if isinstance(order[2], list):
                        order[2] = tuple(order[2])
                    self.orders[color][territory] = Order(*order)
            self.standoffs = set(standoffs)

    def override(self, admin, orders):
        if admin != self.admin:
            raise AdministrativeException("need admin powers to use override command")
        lines = orders.splitlines()
        if len(lines) == 1:
            raise AdministrativeException('all overriding orders must be submitted on separate lines in one message')
        color = lines[0].strip().lower()
        if color not in self.players.keys():
            raise AdministrativeException('invalid color {}'.format(color))
        override_msg = ['overriding {}'.format(color)]
        override_moves = set()
        builds = []
        for line in lines[1:]:
            line = line.strip().upper()
            try:
                match_move = move_regex.match(line)
                match_build = build_regex.match(line)
                match_disband = disband_regex.match(line)
                match_add_sc = add_supply_center_regex.match(line)
                match_remove_sc = remove_supply_center_regex.match(line)
                match_set_season = set_season_regex.match(line)
                match_set_year = set_year_regex.match(line)
                match_add_retreat = add_retreat_regex.match(line)
                match_remove_retreat = remove_retreat_regex.match(line)
                match_add_standoff = add_standoff_regex.match(line)
                match_remove_standoff = remove_standoff_regex.match(line)

                # move
                if match_move:
                    unit_type, source, destination = match_move.groups()
                    self._check_ownership(source, unit_type, color)
                    override_moves.add((source, destination))
                    override_msg.append('{} at {} moved to {}'.format(unit_type, source, destination))
                # build
                elif match_build:
                    unit_type, territory = match_build.groups()
                    if territory not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(territory))
                    if self.units_by_terr.get(territory):
                        raise InvalidOrderException('there is already a units in {}'.format(territory))
                    # add to list to build later, because building now could conflict with moving units
                    builds.append((unit_type, territory))
                    override_msg.append('{} added to {}'.format(unit_type, territory))
                # disband
                elif match_disband:
                    unit_type, territory = match_disband.groups()
                    self._check_ownership(territory, unit_type, color)
                    self.order_resolver.remove_unit(territory)
                    override_msg.append('{} in {} disbanded'.format(unit_type, territory))
                # add supply center
                elif match_add_sc:
                    territory = match_add_sc.groups()[0]
                    if territory not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(territory))
                    if territory not in supply_center_territories:
                        raise InvalidOrderException('territory {} doesnt have a supply center in it'.format(territory))
                    old_color = self.supply_centers_by_terr[territory]
                    if old_color == color:
                        override_msg.append('you already controlled the supply center at {}, fool'.format(territory))
                        continue
                    elif old_color == 'uncontrolled':
                        override_msg.append('gained control of the uncontrolled supply center at {}'.format(territory))
                    elif old_color != color:
                        override_msg.append('stole the supply center at {} from {}'.format(territory, old_color))
                        self.supply_centers_by_color[old_color].remove(territory)
                    self.supply_centers_by_terr[territory] = color
                    self.supply_centers_by_color[color].add(territory)
                # remove supply center
                elif match_remove_sc:
                    territory = match_remove_sc.groups()[0]
                    if territory not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(territory))
                    if territory not in supply_center_territories:
                        raise InvalidOrderException('territory {} doesnt have a supply center in it'.format(territory))
                    old_color = self.supply_centers_by_terr[territory]
                    if old_color == color:
                        override_msg.append('removed control of supply center in {}'.format(territory))
                        self.supply_centers_by_color[color].remove(territory)
                        self.supply_centers_by_terr[territory] = 'uncontrolled'
                    else:
                        raise InvalidOrderException(
                            "you didn't have control of the supply center of {}, blockhead".format(territory))
                elif match_set_season:
                    season = match_set_season.groups()[0]
                    if season not in valid_seasons:
                        raise AdministrativeException('invalid season {}\n'
                                                      'valid seasons are {}'.format(season, valid_seasons))
                    self.season = season
                    override_msg.append('season set to {}'.format(season))
                elif match_set_year:
                    year = match_set_season.groups()[0]
                    if len(year) != 2 or not year.isdigit:
                        raise AdministrativeException(
                            'year must be a two digit number. your input: {}'.format(year))
                    self.year = int(year)
                    override_msg.append('year set to {}'.format(year))
                # TODO: are adding retreats and standoffs really necessary?
                # add retreat
                elif match_add_retreat:
                    unit_type, dislodged_unit, dislodging_unit = match_add_retreat
                    if dislodged_unit not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(dislodged_unit))
                    if dislodging_unit not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(dislodged_unit))
                    if color not in self.players.keys():
                        raise InvalidOrderException('invalid color {}'.format(color))
                    self.retreating_units[color][dislodged_unit] = (dislodging_unit, unit_type)
                    override_msg.append('added {} {} retreating from {} that was dislodged by a unit attacking from {}'
                                        .format(color, unit_type, dislodged_unit, dislodging_unit))
                # remove retreat
                elif match_remove_retreat:
                    territory = match_remove_retreat
                    if territory not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(territory))
                    if self.retreating_units[color].get(territory) is None:
                        raise InvalidOrderException('no unit retreating from {} to remove'.format(territory))
                    self.retreating_units[color].pop(territory)
                    override_msg.append('removed unit retreating from {} '.format(territory))
                # add standoff
                elif match_add_standoff:
                    territory = match_add_standoff.groups()
                    if territory not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(territory))
                    self.standoffs.add(territory)
                    override_msg.append('standoff added at {}'.format(territory))
                # remove standoff
                elif match_remove_standoff:
                    territory = match_remove_standoff.groups()
                    if territory not in territories:
                        raise InvalidOrderException('territory {} unknown'.format(territory))
                    self.standoffs.discard(territory)
                    override_msg.append('standoff removed from {}'.format(territory))
                else:
                    raise InvalidOrderException('order type not recognized')
            except InvalidOrderException as e:
                override_msg.append(str(e))
        self.order_resolver.mass_move(override_moves)
        # build units last so newly built units don't over write units that were ordered to move elsewhere
        for unit_type, territory in builds:
            self.order_resolver.add_unit(color, unit_type, territory)
        return '\n'.join(override_msg)

    def set_season(self, admin, season):
        if admin != self.admin:
            raise AdministrativeException('need admin powers to set the season')
        if season not in valid_seasons:
            raise AdministrativeException('invalid season {}\n'
                                          'valid seasons are {}'.format(season, valid_seasons))
        self.season = season
        return 'season set to {}'.format(season)

    def set_year(self, admin, year):
        if admin != self.admin:
            raise AdministrativeException('need admin powers to set the year')
        if len(year) != 2 or not year.isdigit:
            raise AdministrativeException('year must be a two digit number. your input: {}'.format(year))
        self.year = int(year)
        return 'year set to {}'.format(year)

    def clear_orders(self, admin):
        if admin != self.admin:
            raise AdministrativeException('need admin powers to clear all orders')
        for color in self.colors:
            self.orders[color].clear()
        return 'all orders cleared'
