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


def _convoy_possible(convoy, convoying_fleets):
    source, destination = convoy
    stack = [source]
    checked = {source}
    while stack:
        cur = stack.pop()
        for adj in sea_routes[cur]:
            if adj == destination:
                return True
            if adj in convoying_fleets and adj not in checked:
                checked.add(adj)
                stack.append(adj)
    return False


def _find_cycles_and_border_clashes(dependencies, convoyed_moves):
    cycles = set()
    # a border clash is a cycle of length 2
    border_clashes = set()
    checked = set()
    for source in dependencies.keys():
        if source in checked:
            continue
        cur_source = source
        cur_cycle = []
        while True:
            checked.add(cur_source)
            cur_cycle.append(cur_source)
            cur_source = dependencies[cur_source]
            if cur_source in cur_cycle:
                # cycle found. remove territories that depend on the cycle but are not part of it.
                # ex: a->b->c->d->b. the cycle is [b, c, d]. a simply led to the cycle.
                index = cur_cycle.index(cur_source)
                cycle = cur_cycle[index:]
                if len(cycle) == 2:
                    # convoyed moves dont cause border clashes
                    for convoy in convoyed_moves:
                        if convoy[0] in cycle and convoy[1] in cycle:
                            cycles.add(cycle)
                            break
                    else:
                        border_clashes.add(tuple(cycle))
                else:
                    cycles.add(tuple(cycle))
                break
            if cur_source is None or cur_source in checked:
                break
    return cycles, border_clashes


class OrderSolver:

    def __init__(self, units_by_color, units_by_terr):
        self.dislodged_units = {}
        self.standoffs = set()
        self.successful_moves = set()
        self.dependent_moves = set()
        self.failed_moves = set()
        self.orders_by_territory = {}
        self.move_destinations = {}
        self.convoys = {}
        self.hold_support = {}
        self.move_support = {}
        self.convoyed_move_support = {}
        self.units_by_color = units_by_color  # (unit type, territory)
        self.units_by_terr = units_by_terr  # (unit type, color)

    def update_unit_dicts(self, units_by_color, units_by_terr):
        self.units_by_color = units_by_color
        self.units_by_terr = units_by_terr

    def move_unit(self, source, destination):
        unit_type, color = self.units_by_terr.pop(source)
        self.units_by_terr[destination] = (unit_type, color)
        self.units_by_color[color].remove((unit_type, source))
        self.units_by_color[color].add((unit_type, destination))

    def add_unit(self, color, unit_type, territory):
        self.units_by_color[color].add((unit_type, territory))
        self.units_by_terr[territory] = (unit_type, color)

    def remove_unit(self, territory):
        unit_type, color = self.units_by_terr.pop(territory)
        self.units_by_color[color].remove((unit_type, territory))

    def mass_move(self, moves):
        # move all units in moves by storing their color and unit type in a temporary dictionary,
        # removing the old units, then adding new units in their respective destinations
        temp_territories = {}
        for source, destination in moves:
            temp_territories[source] = self.units_by_terr[source]
            self.remove_unit(source)
        for source, destination in moves:
            unit_type, color = temp_territories[source]
            self.add_unit(color, unit_type, destination)

    def _sort_orders(self, orders):
        summary = []
        # sort orders for ease of access
        self.orders_by_territory.clear()
        self.move_destinations.clear()
        self.convoys.clear()
        self.hold_support.clear()
        self.move_support.clear()
        for source, order_type, extra_info in orders:
            self.orders_by_territory[source] = (order_type, extra_info)
            self.hold_support[source] = set()
            if order_type == 'move':
                destination = extra_info
                if self.move_destinations.get(destination) is None:
                    self.move_destinations[destination] = set()
                self.move_destinations[destination].add(source)
                self.move_support[(source, destination)] = set()
            elif order_type == 'convoyed_move':
                destination = extra_info
                self.convoys[(source, destination)] = set()
                # armies that are supposed to move via convoy can still move over land if their destination is adjacent,
                # so add it to move_destinations and related dictionaries as if it were a normal move order.
                if destination in coast_routes[source]:
                    # add the unit to move_destination and move_support as if it were a normal attack
                    if self.move_destinations.get(destination) is None:
                        self.move_destinations[destination] = set()
                    self.move_support[(source, destination)] = set()

        for source, order_type, extra_info in orders:
            if order_type == 'convoy':
                if extra_info in self.convoys.keys():  # check if there's a unit to convoy
                    self.convoys[extra_info].add(source)
            elif order_type == 'support_hold':  # match supports to holds
                if self._support_cut(source):
                    summary.append("{}'s support cut".format(source))
                    continue
                # check if there's a unit to support. it's also illegal to support a moving unit
                if extra_info in self.hold_support.keys() and self.orders_by_territory.get(extra_info, [None])[0]\
                        not in {'move', 'convoyed_move'}:
                    self.hold_support[extra_info].add(source)
            elif order_type == 'support_move':  # match supports to moves
                if self._support_cut(source):
                    summary.append("{}'s support cut".format(source))
                    continue
                # check if there's a move to support
                if extra_info in self.move_support.keys():
                    self.move_support[extra_info].add(source)

        # check which armies have a possible path of convoying fleets with which to convoy
        self.convoyed_move_support.clear()
        convoys_to_remove = set()
        for convoy, convoying_fleets in self.convoys.items():
            if _convoy_possible(convoy, convoying_fleets):
                self.convoyed_move_support[convoy] = set()
            else:
                convoys_to_remove.add(convoy)
        # remove impossible convoys
        for convoy in convoys_to_remove:
            summary.append("{}'s convoy to {} failed".format(*convoy))
            self.convoys.pop(convoy)

        # match supports to convoyed moves
        for source, order_type, extra_info in orders:
            if order_type == 'support_convoyed_move':
                if self._support_cut(source):
                    summary.append("{}'s support cut".format(source))
                    continue
                if extra_info in self.convoyed_move_support.keys():
                    self.convoyed_move_support[extra_info].add(source)
                # convoyed move can act as normal move if its destination is adjacent, so support the normal move too
                if extra_info in self.move_support.keys():
                    self.move_support.get(extra_info).add(source)
        return summary

    def _support_cut(self, supporter):
        order_type, extra_info = self.orders_by_territory[supporter]
        color = self.units_by_terr[supporter][1]
        if order_type == 'support_hold':
            for attacker in self.move_destinations.get(supporter, set()):
                # hold support is cut if the attacking unit is not of the same color.
                if self.units_by_terr[attacker][1] != color:
                    return True
        elif order_type in {'support_move', 'support_convoyed_move'}:
            for attacker in self.move_destinations.get(supporter, set()):
                # support is cut by an enemy unit that this unit is not supporting an attack on and its color differs.
                # extra_info[1] is the territory supporter is supporting an attack on.
                if attacker != extra_info[1] and self.units_by_terr[attacker][1] != color:
                    return True
        return False

    def _attack_dislodges(self, attacker, attack_support, defender, defense_support):
        attack_color = self.units_by_terr[attacker][1]
        defense_color = self.units_by_terr[defender][1]
        if attack_color != defense_color:
            attack_force = 1
            for support in attack_support:
                if self.units_by_terr[support][1] != defense_color:
                    attack_force += 1
            if attack_force > len(defense_support) + 1:
                return True
        return False

    def _resolve_attacks(self, territory):
        # make list of attackers and their force to sort
        attacking_forces = []
        for attacker in self.move_destinations.get(territory, set()):
            attacking_forces.append((len(self.move_support[(attacker, territory)]) + 1, attacker))
        # determine whether each attack succeeds, fails, or may succeed
        if len(attacking_forces) == 1:
            attacker = attacking_forces[0][1]
            if self.units_by_terr.get(territory) is None:
                # lone attacker always moves into an unoccupied territory
                self.successful_moves.add(attacker)
                return attacker
            elif self._attack_dislodges(attacker, self.move_support[(attacker, territory)], territory,
                                        self.hold_support.get(territory, set())):
                self.dislodged_units[territory] = (attacker, *self.units_by_terr[territory])
                self.successful_moves.add(attacker)
                return attacker
            elif self.orders_by_territory.get(territory, [None])[0] == 'move':
                # attacker able to move in if the unit in territory successfully moves out
                self.dependent_moves.add(attacker)
            else:
                self.failed_moves.add(attacker)
        elif len(attacking_forces) > 1:
            sorted_attackers = sorted(attacking_forces, reverse=True)
            strongest = sorted_attackers[0][1]
            second_strongest = sorted_attackers[1][1]
            for attacker in sorted_attackers[1:]:
                self.failed_moves.add(attacker[1])
            if self._attack_dislodges(strongest, self.move_support[(strongest, territory)], second_strongest,
                                      self.move_support[(second_strongest, territory)]):
                if self.units_by_terr.get(territory) is None:
                    self.successful_moves.add(strongest)
                    return strongest
                elif self._attack_dislodges(strongest, self.move_support[(strongest, territory)], territory,
                                            self.hold_support.get(territory, set())):
                    self.dislodged_units[territory] = (strongest, *self.units_by_terr[territory])
                    self.successful_moves.add(strongest)
                elif self.orders_by_territory.get(territory, [None])[0] == 'move':
                    # strongest able to move in if the unit in territory successfully moves out
                    self.dependent_moves.add(strongest)
                return strongest
            else:
                self.failed_moves.add(strongest)
                self.standoffs.add(territory)
        return None

    def _resolve_border_attack(self, unit0, unit1):
        # this method used in the case of two territories attacking each other
        # same as resolve attacks, but compare self.move_support to self.move_support, not self.hold_support
        unit0_support = self.move_support[(unit0, unit1)]
        unit1_support = self.move_support[(unit1, unit0)]
        # check if unit0 can dislodge unit1
        if self._attack_dislodges(unit0, unit0_support, unit1, unit1_support):
            return 0
        # check if unit1 can dislodge unit0
        if self._attack_dislodges(unit1, unit1_support, unit0, unit0_support):
            return 1
        return None

    def _generate_dependencies_graph(self):
        dependencies = {}
        for destination in self.move_destinations.keys():
            for source in self.move_destinations[destination]:
                if self.orders_by_territory.get(destination, [None])[0] == 'move':
                    dependencies[source] = destination
                else:
                    dependencies[source] = None
        return dependencies

    def _check_for_successful_convoys(self):
        successful_convoys = set()
        # check all convoying fleets to see if they're dislodged
        for convoy, convoying_fleets in self.convoys.items():
            ok_fleets = set()
            for fleet in convoying_fleets:
                if self._resolve_attacks(fleet) is None:
                    # fleet not dislodged, so can be used to convoy
                    ok_fleets.add(fleet)
            # check if convoy is still possible with fleets that weren't dislodged
            if _convoy_possible(convoy, ok_fleets):
                successful_convoys.add(convoy)
        return successful_convoys

    def resolve_normal_orders(self, orders):
        resolve_summary = []
        resolve_summary += self._sort_orders(orders)

        # check which convoys succeed by checking if each of their convoying fleets is dislodged or not
        # when a convoy succeed, check if it cuts the support at its destination.
        # this may allow another convoy to succeed, so checks continue until no more supports are cut succeed in a loop.
        # keep track of convoyed moves because they dont cause border clashes like normal moves do/
        convoyed_moves = set()
        new_support_cut = True
        while new_support_cut:
            new_support_cut = False
            for convoy in self._check_for_successful_convoys():
                source, destination = convoy
                self.convoys.pop(convoy)
                convoyed_moves.add(convoy)
                # add the successful convoy to move_destination and move_support as if it were a normal attack
                if self.move_destinations.get(destination) is None:
                    self.move_destinations[destination] = set()
                self.move_destinations[destination].add(source)
                self.move_support[(source, destination)] = self.convoyed_move_support[convoy]
                # check if the newly successful convoy cuts any support given by a unit at its destination
                if self.units_by_terr.get(destination) is not None and self._support_cut(destination):
                    resolve_summary.append("{}'s support cut".format(destination))
                    new_support_cut = True

        # clear results of attacks evaluated when checking for successful convoys
        self.dislodged_units.clear()
        self.standoffs.clear()
        self.successful_moves.clear()
        self.dependent_moves.clear()
        self.failed_moves.clear()

        dependency_graph = self._generate_dependencies_graph()
        cycles, border_clashes = _find_cycles_and_border_clashes(dependency_graph, convoyed_moves)
        # check which units succeed, fail, or may succeed in their moves
        # also determines units forced to retreat
        for territory in self.move_destinations.keys():
            self._resolve_attacks(territory)

        # sort dependent moves into successful and failed moves based on dependency graph
        success = set()
        fail = set()
        for clash in border_clashes:
            clash_victor = self._resolve_border_attack(*clash)
            # loser of clash fails its move
            # victor of clash only succeeds if it beat out other attackers (which was determined earlier)
            if clash_victor != 0:
                self.successful_moves.discard(clash[0])
                self.dependent_moves.discard(clash[0])
                self.failed_moves.add(clash[0])
            if clash_victor != 1:
                self.successful_moves.discard(clash[1])
                self.dependent_moves.discard(clash[1])
                self.failed_moves.add(clash[1])
        for territory in self.dependent_moves:
            if territory in success or territory in fail:
                continue
            cur_terr = territory
            cur_cycle = []
            while True:
                cur_cycle.append(cur_terr)
                cur_terr = dependency_graph[cur_terr]
                if cur_terr in self.successful_moves:
                    success.update(cur_cycle)
                    break
                elif cur_terr in self.failed_moves:
                    fail.update(cur_cycle)
                    break
                elif cur_terr in self.dependent_moves:
                    if cur_terr in cur_cycle:
                        # cycle of dependent moves found. they can all move without conflict.
                        success.update(cur_cycle)
                        break
                else:
                    raise Exception('{} not in successful, failed, or dependent moves'.format(cur_terr))
        for s in success:
            self.successful_moves.add(s)
        for f in fail:
            self.failed_moves.add(f)
        for s in self.successful_moves:
            # units that successfully moved cannot be dislodged
            # an attacking unit being added to dislodged_units means it would be dislodged if it failed its attack
            self.dislodged_units.pop(s, None)
            resolve_summary.append('{} successfully moved to {}'.format(s, self.orders_by_territory[s][1]))
        for f in self.failed_moves:
            resolve_summary.append('{} failed to moved to {}'.format(f, self.orders_by_territory[f][1]))
        for convoy in self.convoys.keys():
            resolve_summary.append("{}'s convoy to {} was broken".format(*convoy))

        # make list of all successful moves for a mass move
        moves = []
        for territory in self.successful_moves:
            destination = self.orders_by_territory[territory][1]
            moves.append((territory, destination))
        self.mass_move(moves)
        return self.dislodged_units, self.standoffs, resolve_summary

    def resolve_retreat_orders(self, orders):
        order_summary = []
        self.move_destinations.clear()
        for source, order_type, extra_info, color, unit_type in orders:
            if order_type == 'move':
                # make dictionary of territories that units retreat to to check for conflicts
                destination = extra_info
                if self.move_destinations.get(destination) is None:
                    self.move_destinations[destination] = set()
                self.move_destinations[destination].add((source, color, unit_type))
            elif order_type == 'disband':
                # nothing needs to be done to disband a retreating unit since retreating units aren't part of the game
                # state
                order_summary.append('{} {} in {} disbanded'.format(color, unit_type, source))
        for destination in self.move_destinations.keys():
            # if only one unit retreats to a territory, move it
            if len(self.move_destinations[destination]) == 1:
                source, color, unit_type = self.move_destinations[destination][0]
                order_summary.append('{} {} retreated from {} to {}'.format(color, unit_type, source, destination))
                # add unit because retreating units aren't part of the normal game state, so they can't be moved
                self.add_unit(color, unit_type, destination)
            else:
                # if multiple units retreat to the same territory, they get disbanded. nothing needs to be done to
                # disband a retreating unit since retreating units aren't part of the game state.
                for source, color, unit_type in self.move_destinations[destination]:
                    order_summary.append('{} {} retreated from {} to {}, but was disbanded due to multiple units'
                                         'retreating to that territory'.format(color, unit_type, source, destination))
        return order_summary

    def build_disband(self, orders):
        # add or remove units corresponding to each color's build and disband orders
        summary = []
        for color in orders.keys():
            for territory, order_type, unit_type in orders[color].values():
                if order_type == 'build':
                    summary.append('{} built {} at {}'.format(color, unit_type, territory))
                    self.add_unit(color, unit_type, territory)
                elif order_type == 'disband':
                    summary.append('{} disbanded {} at {}'.format(color, unit_type, territory))
                    self.remove_unit(territory)
                else:
                    print('illegal order {} {} {} during build phase'.format(territory, order_type, unit_type))
        return summary
