import os
from cmath import polar, rect, pi
from PIL import Image, ImageDraw

# the bounding boxes of the supply center territories. used for coloring the territories in.
supply_center_bounding_boxes = {'DAL': (240, 48, 328, 136), 'VIN': (231, 0, 271, 64), 'SIC': (224, 192, 272, 221),
                                'CAR': (136, 200, 215, 240), 'JER': (527, 248, 551, 287), 'ALE': (384, 281, 494, 328),
                                'THE': (488, 283, 580, 392), 'NEA': (233, 129, 296, 198), 'MEM': (394, 299, 512, 367),
                                'BYZ': (392, 120, 456, 168), 'SAG': (0, 153, 88, 207), 'NUM': (160, 256, 240, 296),
                                'CYR': (320, 272, 408, 336), 'MAC': (331, 119, 406, 176), 'SID': (528, 199, 568, 232),
                                'THA': (160, 225, 215, 270), 'PET': (530, 281, 574, 325), 'BAL': (97, 145, 132, 174),
                                'CRE': (380, 225, 424, 247), 'ROM': (201, 88, 246, 142), 'ATH': (328, 160, 384, 200),
                                'SPA': (338, 185, 374, 224), 'MAS': (96, 56, 184, 112), 'RAV': (209, 72, 255, 118),
                                'SAD': (176, 138, 200, 184), 'ANT': (528, 163, 568, 208), 'TYE': (532, 224, 560, 253),
                                'CYP': (456, 216, 512, 242), 'MIL': (400, 160, 464, 208), 'CHE': (375, 0, 612, 104),
                                'LEP': (216, 284, 328, 343), 'CIR': (120, 227, 181, 296), 'DAM': (543, 144, 611, 224),
                                'SIP': (480, 88, 584, 143)}

# the RGB values of the different colors
palette = {
    'red': (196, 143, 133),
    'blue': (121, 175, 198),
    'green': (164, 196, 153),
    'black': (168, 126, 159),
    'yellow': (234, 234, 175)}
# tells where the upper left position of a unit in that territory should be
unit_xys = {'GAU': (108, 31),
            'RHA': (195, 37),
            'SAM': (303, 40),
            'VIN': (247, 35),
            'ILL': (316, 90),
            'LUS': (10, 126),
            'ARM': (583, 129),
            'GAL': (470, 137),
            'DAM': (580, 182),
            'ARA': (576, 228),
            'CIR': (144, 242),
            'SAH': (152, 306),
            'PHA': (230, 325),
            'MAR': (356, 325),
            'SAG': (36, 163),
            'TAR': (76, 119),
            'MAS': (145, 76),
            'ETR': (191, 72),
            'ROM': (207, 99),
            'NEA': (267, 150),
            'APU': (257, 123),
            'RAV': (228, 92),
            'VEN': (224, 51),
            'DAL': (272, 81),
            'EPI': (325, 148),
            'ATH': (350, 169),
            'SPA': (347, 188),
            'MAC': (366, 128),
            'BYZ': (412, 147),
            'DAC': (367, 85),
            'CHE': (523, 32),
            'SIP': (539, 104),
            'BIT': (461, 110),
            'MIL': (422, 182),
            'ISA': (480, 178),
            'CAP': (512, 156),
            'ANT': (542, 181),
            'SID': (549, 204),
            'TYE': (543, 229),
            'JER': (537, 263),
            'SII': (516, 296),
            'PET': (542, 300),
            'NAB': (577, 295),
            'MAU': (59, 236),
            'CAR': (167, 213),
            'THA': (188, 243),
            'NUM': (205, 270),
            'LEP': (282, 313),
            'CYR': (361, 280),
            'ALE': (432, 294),
            'MEM': (467, 315),
            'BAY': (399, 355),
            'THE': (515, 338),
            'COR': (181, 111),
            'SAD': (183, 141),
            'SIC': (251, 191),
            'CRE': (382, 221),
            'CYP': (486, 219),
            'IBE': (38, 203),
            'BER': (139, 163),
            'LIG': (151, 107),
            'TYN': (230, 155),
            'PUN': (198, 172),
            'ADR': (253, 97),
            'ION': (298, 161),
            'AUS': (279, 202),
            'GOT': (234, 236),
            'GOS': (303, 290),
            'LIB': (319, 250),
            'MES': (326, 206),
            'AEG': (384, 180),
            'BLA': (439, 76),
            'MIN': (427, 215),
            'EGY': (428, 243),
            'CIL': (473, 200),
            'SYR': (510, 221),
            'GOP': (503, 256),
            'REE': (546, 330),
            'BAL': (98, 146)}


# TODO: once current code is stable, change add_moves to add_orders which handles every type of order.
#  the inputs are a list of orders and two sets for successful and failed orders. each order should have a different
#  look. hold support can be a line like a move but with a perpendicular line on the end like the line used to draw a
#  lineman's movements in football moves. convoyed moves can have a blue tinted line, but be the same as move.
#  convoy orders should have a line meeting the line of the moving unit at a 90deg angle with a circle at the
#  intersection. i'm not sure about move support or convoyed move support orders.


def generate_bounding_boxes_and_masks(territories_fp='ancient_mediterranean_maps/supply_center_territories/',
                                      masks_fp='ancient_mediterranean_maps/masks/'):
    for filename in os.listdir(territories_fp):
        if filename.endswith('.jpeg'):
            territory = filename[:3]
            if filename.find('.') != 3:
                continue
            territory = filename[:3]
            im = Image.open(territories_fp + filename)
            bbox = im.getbbox()
            im = im.crop(bbox).convert(mode="1")
            im.save(masks_fp + territory + '.bmp')
            supply_center_bounding_boxes[territory.upper()] = bbox
    print(supply_center_bounding_boxes)
    # then you manually copy the printed dictionary to


def color_supply_centers(im, supply_centers_by_color):
    # color supply center territories by owner
    for color in supply_centers_by_color.keys():
        for supply_center in supply_centers_by_color[color]:
            bbox = supply_center_bounding_boxes[supply_center]
            rgb = palette[color]
            mask = Image.open('ancient_mediterranean_maps/masks/' + supply_center.lower() + '.bmp')
            im.paste(rgb, bbox, mask)
    return im


def add_units(im, units_by_color):
    # add units corresponding to their color and unit type
    for color in units_by_color.keys():
        for unit_type, territory in units_by_color[color]:
            if unit_type == 'F':
                unit = color + '_fleet.jpeg'
            elif unit_type == 'A':
                unit = color + '_army.jpeg'
            else:
                raise Exception('{} idk'.format(unit_type))
            sprite = Image.open('ancient_mediterranean_maps/units/' + unit)
            im.paste(sprite, unit_xys[territory])
    return im


def add_circularhead(draw, end_point, angle, fill):
    offset = rect(4, angle)
    end_point = (end_point[0] + offset.real, end_point[1] + offset.imag)
    side_length = 4
    bbox = (
        end_point[0] - side_length, end_point[1] - side_length, end_point[0] + side_length, end_point[1] + side_length)
    draw.chord(bbox, 0, 360, fill=fill)


def add_archead(draw, end_point, angle, fill):
    offset = rect(6, angle)
    end_point = (end_point[0] + offset.real, end_point[1] + offset.imag)
    side_length = 6
    angle = angle * 180 / pi
    bbox = (
        end_point[0] - side_length, end_point[1] - side_length, end_point[0] + side_length, end_point[1] + side_length)
    draw.chord(bbox, angle + 90, angle - 90, fill=fill)


def add_flathead(draw, end_point, angle, fill):
    side_length = 8
    offset_angles = [pi / 2, -pi / 2]
    offsets = [rect(side_length, angle + offset_angle) for offset_angle in offset_angles]
    points = [(end_point[0] + offset.real, end_point[1] + offset.imag) for offset in offsets]
    draw.line(points, fill=fill, width=5)


def add_arrowhead(draw, end_point, angle, fill):
    side_length = 6
    offset_angles = [0, pi * 2 / 3, -pi * 2 / 3]
    offsets = [rect(side_length, angle + offset_angle) for offset_angle in offset_angles]
    points = [(end_point[0] + offset.real, end_point[1] + offset.imag) for offset in offsets]
    draw.polygon(points, fill=fill)


def add_arrow(draw, move, failed=False):
    source_xy = [a + 9 for a in unit_xys[move[0]]]
    destination_xy = [a + 9 for a in unit_xys[move[1]]]
    mid = complex(destination_xy[0] - source_xy[0], destination_xy[1] - source_xy[1])
    # the square units are wider near the edges. i calculate a multiplier which translates the length to the nearest
    # edge, 9, to the distance to the edge at the line's angle. ex: a 45 degree line has a multiplier of root 2
    ratio = min(abs(mid.real), abs(mid.imag)) / max(abs(mid.real), abs(mid.imag))
    multiplier, _ = polar(complex(1.0, ratio))
    distance, angle = polar(mid)
    # shift line slightly (by 3) towards source to make up for the arrowhead's extra length
    offset = min(9.0 * multiplier + 3, (distance - 12) / 2)
    start_offset = rect(offset - 3, angle)
    end_offset = rect(distance - offset - 3, angle)
    start_point = (source_xy[0] + start_offset.real, source_xy[1] + start_offset.imag)
    end_point = (source_xy[0] + end_offset.real, source_xy[1] + end_offset.imag)
    fill = (0, 0, 0)
    if failed:
        fill = (100, 100, 100)
    draw.line([start_point, end_point], fill=fill, width=5)
    add_arrowhead(draw, end_point, angle, fill)


def add_moves(im, successful_moves, failed_moves):
    draw = ImageDraw.Draw(im)
    for move in successful_moves:
        add_arrow(draw, move)
    for move in failed_moves:
        add_arrow(draw, move, failed=True)
    return im


def generate_map(supply_centers_by_color, units_by_color, show=False):
    blank = Image.open('ancient_mediterranean_maps/blank.jpeg')
    blank = color_supply_centers(blank, supply_centers_by_color)
    blank = add_units(blank, units_by_color)
    if show:
        blank.show()
    return blank


def generate_changes(supply_centers_by_color, units_by_color, successful_moves, failed_moves, show=False):
    blank = generate_map(supply_centers_by_color, units_by_color)
    blank = add_moves(blank, successful_moves, failed_moves)
    if show:
        blank.show()
    return blank


if __name__ == '__main__':
    example_supply_centers_by_color = {'red': {'NEA', 'ROM', 'RAV', 'VIN', 'MAS'},
                                       'blue': {'THA', 'CIR', 'CAR', 'SAG', 'LEP'},
                                       'green': {'SPA', 'ATH', 'MAC', 'CRE'},
                                       'black': {'SID', 'ANT', 'DAM', 'TYE', 'CYP', 'SIP'},
                                       'yellow': {'ALE', 'MEM', 'THE', 'CYR'}}
    example_units_by_color = {'red': {('F', 'ADR'), ('A', 'DAL'), ('A', 'MAS'), ('F', 'MES'), ('F', 'SIC')},
                              'blue': {('A', 'LEP'), ('F', 'PUN'), ('F', 'AEG'), ('F', 'BER'), ('A', 'MAU')},
                              'green': {('A', 'MAC'), ('A', 'ATH'), ('F', 'CRE'), ('F', 'SPA')},
                              'black': {('A', 'DAM'), ('A', 'TYE'), ('F', 'CYP'), ('F', 'CIL'), ('A', 'SIP'),
                                        ('A', 'ARA')},
                              'yellow': {('A', 'SII'), ('F', 'CYR'), ('A', 'MEM'), ('A', 'PHA')}}
    example_successful_moves = {('CIL', 'MIN'), ('AEG', 'MIL'), ('ADR', 'EPI'), ('MAC', 'BYZ'), ('ATH', 'MAC'),
                                ('SPA', 'ATH'), ('CYP', 'EGY'), ('SIP', 'BIT'), ('LEP', 'MAR'), ('CYR', 'LEP'),
                                ('RAV', 'ADR'), ('APU', 'ADR'), ('ADR', 'DAL')}
    example_failed_moves = {('MAU', 'CIR'), ('PHA', 'CIR'), ('SIC', 'PUN'), ('TYE', 'JER'), ('SII', 'JER')}
    generate_changes(example_supply_centers_by_color, example_units_by_color, example_successful_moves,
                     example_failed_moves, show=True)
