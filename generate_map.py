import os
from PIL import Image

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

# # generate supply center bounding boxes and masks
# for filename in os.listdir('ancient_mediterranean_maps/supply_center_territories'):
#     if filename.endswith('.jpeg'):
#         territory = filename[:3]
#         if filename.find('.') != 3:
#             continue
#         territory = filename[:3]
#         im = Image.open('ancient_mediterranean_maps/supply_center_territories/' + filename)
#         bbox = im.getbbox()
#         im = im.crop(bbox).convert(mode="1")
#         im.save('ancient_mediterranean_maps/masks/' + territory + '.bmp')
#         supply_center_bounding_boxes[territory.upper()] = bbox
#  print(supply_center_bounding_boxes)

palette = {
    'red': (196, 143, 133),
    'blue': (121, 175, 198),
    'green': (164, 196, 153),
    'black': (168, 126, 159),
    'yellow': (234, 234, 175)}
supply_center_colors = {'DAL': 'uncontrolled', 'VIN': 'red', 'SIC': 'uncontrolled', 'CAR': 'blue',
                        'JER': 'uncontrolled', 'ALE': 'yellow', 'THE': 'yellow', 'NEA': 'red',
                        'MEM': 'yellow', 'BYZ': 'uncontrolled', 'SAG': 'blue', 'NUM': 'uncontrolled',
                        'CYR': 'yellow', 'MAC': 'green', 'SID': 'black', 'THA': 'blue',
                        'PET': 'uncontrolled', 'BAL': 'uncontrolled', 'CRE': 'green', 'ROM': 'red',
                        'ATH': 'green', 'SPA': 'green', 'MAS': 'red', 'RAV': 'red',
                        'SAD': 'uncontrolled', 'ANT': 'black', 'TYE': 'black', 'CYP': 'black',
                        'MIL': 'uncontrolled', 'CHE': 'uncontrolled', 'LEP': 'blue', 'CIR': 'blue',
                        'DAM': 'black', 'SIP': 'black'}
units_by_color = {'red': {('F', 'ADR'),
                          ('A', 'DAL'),
                          ('A', 'MAS'),
                          ('F', 'MES'),
                          ('F', 'SIC')},
                  'blue': {('A', 'LEP'),
                           ('F', 'PUN'),
                           ('F', 'AEG'),
                           ('F', 'BER'),
                           ('A', 'MAU')},
                  'green': {('A', 'MAC'),
                            ('A', 'ATH'),
                            ('F', 'CRE'),
                            ('F', 'SPA')},
                  'black': {('A', 'DAM'),
                            ('A', 'TYE'),
                            ('F', 'CYP'),
                            ('F', 'CIL'),
                            ('A', 'SIP'),
                            ('A', 'ARA')},
                  'yellow': {('A', 'SII'),
                             ('F', 'CYR'),
                             ('A', 'MEM'),
                             ('A', 'PHA')}}

blank = Image.open('ancient_mediterranean_maps/blank.jpeg').copy()
# color supply center territories by owner
for territory, bbox in supply_center_bounding_boxes.items():
    owner = supply_center_colors[territory]
    if owner == 'uncontrolled':
        continue
    color = palette[owner]
    mask = Image.open('ancient_mediterranean_maps/masks/' + territory.lower() + '.bmp')
    blank.paste(color, bbox, mask)

# add units
for color in units_by_color.keys():
    for unit_type, territory in units_by_color[color]:
        if unit_type == 'F':
            unit = color + '_fleet.jpeg'
        elif unit_type == 'A':
            unit = color + '_army.jpeg'
        else:
            raise Exception('{} idk'.format(unit_type))
        sprite = Image.open('ancient_mediterranean_maps/units/' + unit)
        blank.paste(sprite, unit_xys[territory])

blank.show()
