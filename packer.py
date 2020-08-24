#!/bin/python3
from extruder import *
import zipfile
import json
import shutil

mpath = "assets/minecraft/models/block/"
tpath = "assets/minecraft/textures/block/"
tmp = {"parent": "minecraft:block/$parent", "textures":{"$textname":"minecraft:block/$textfile"}}
VERSION = "1.0.1"
basic_json = json.dumps(tmp)

def main():
    functions = [flowers, grass, crops, seaflora, netherflora, otherflora, fungi, rails, redstone, otherblocks]
    for x in range(1024):
        with zipfile.ZipFile(f'web/cdn/Faithful3D-{VERSION}-custom-{x}.zip', 'w') as zf:
            all(zf)
            for i in range(len(functions)):
                if (x >> i) & 1 == 1:
                    functions[i](zf)
    shutil.copyfile(f'web/cdn/Faithful3D-{VERSION}-custom-1023.zip', f'web/cdn/Faithful3D-{VERSION}.zip')

def all(zf):
    zf.write('pack-constants/pack.mcmeta', 'pack.mcmeta')
    zf.write('pack-constants/pack.png', 'pack.png')

def flowers(zf):
    zf.write('cross.json', mpath+'thick_cross.json')
    zf.write('cross_right.json', mpath+'thick_cross_right.json')

    zf.write('pack-constants/pregen/oxeye_daisy.json', mpath+'oxeye_daisy.json')
    zf.write('sunflower_top.json', mpath+'sunflower_top.json')

    for s in ['birch_sapling', 'blue_orchid', 'cornflower', 'dark_oak_sapling', \
            'dead_bush', 'lily_of_the_valley', 'oak_sapling', 'poppy', 'wither_rose']:
        with open(f'working/{s}.json', 'w') as f:
            content = basic_json.replace('$parent', 'thick_cross_right')
            content = content.replace('$textname', 'cross')
            content = content.replace('$textfile', s)
            f.write(content)
        zf.write(f'working/{s}.json', mpath+f'{s}.json')
    for s in ["dandelion", 'allium', 'azure_bluet', 'red_tulip','white_tulip', \
            'orange_tulip', 'pink_tulip', 'spruce_sapling', 'jungle_sapling', \
            'acacia_sapling', 'peony_bottom', 'peony_top', 'rose_bush_bottom', \
            'rose_bush_top', 'lilac_bottom', 'lilac_top', 'sunflower_bottom', \
            'sweet_berry_bush_stage0', 'sweet_berry_bush_stage1', \
            'sweet_berry_bush_stage2','sweet_berry_bush_stage3', ]:
        with open(f'working/{s}.json', 'w') as f:
            content = basic_json.replace('$parent', 'thick_cross')
            content = content.replace('$textname', 'cross')
            content = content.replace('$textfile', s)
            f.write(content)
        zf.write(f'working/{s}.json', mpath+f'{s}.json')

def grass(zf):
    # apparently everything is just tinted rn TODO: fix that
    zf.write('tinted_cross.json', mpath+'thick_tinted_cross.json')
    for s in ['grass', 'fern', 'tall_grass_bottom', 'tall_grass_top', 'large_fern_bottom',\
            'large_fern_top']:
        with open(f'working/{s}.json', 'w') as f:
            content = basic_json.replace('$parent', 'thick_tinted_cross')
            content = content.replace('$textname', 'cross')
            content = content.replace('$textfile', s)
            f.write(content)
        zf.write(f'working/{s}.json', mpath+f'{s}.json')

def crops(zf):
    zf.write('crop.json', mpath + 'crop.json')
    for s in ['stem_fruit', 'stem_growth1', 'stem_growth2', 'stem_growth3', \
            'stem_growth4', 'stem_growth5', 'stem_growth6', 'stem_growth7']:
        zf.write(f'pack-constants/pregen/{s}.json', mpath + f'{s}.json')

def seaflora(zf):
    zf.write('template_seagrass.json', mpath + 'template_seagrass.json')
    zf.write('tinted_cross.json', mpath+'thick_tinted_cross.json')
    zf.write('coral_fan.json', mpath+'coral_fan.json')
    zf.write('coral_wall_fan.json', mpath+'coral_wall_fan.json')
    zf.write('cross.json', mpath+'thick_cross.json')

    for s in ['kelp_plant', 'kelp']:
        with open(f'working/{s}.json', 'w') as f:
            content = basic_json.replace('$parent', 'thick_tinted_cross')
            content = content.replace('$textname', 'cross')
            content = content.replace('$textfile', s)
            f.write(content)
        zf.write(f'working/{s}.json', mpath+f'{s}.json')
    for s in ['tube_coral', 'fire_coral', 'brain_coral', 'bubble_coral', 'horn_coral', \
            'dead_tube_coral', 'dead_fire_coral', 'dead_brain_coral', 'dead_bubble_coral', \
            'dead_horn_coral']:
        with open(f'working/{s}.json', 'w') as f:
            content = basic_json.replace('$parent', 'thick_cross')
            content = content.replace('$textname', 'cross')
            content = content.replace('$textfile', s)
            f.write(content)
        zf.write(f'working/{s}.json', mpath+f'{s}.json')

def netherflora(zf):
    zf.write('cross.json', mpath+'thick_cross.json')
    for s in ['crimson_roots', 'nether_sprouts', 'warped_roots', 'twisting_vines', \
            'twisting_vines_plant', 'weeping_vines', 'weeping_vines_plant']:
        with open(f'working/{s}.json', 'w') as f:
            content = basic_json.replace('$parent', 'thick_cross')
            content = content.replace('$textname', 'cross')
            content = content.replace('$textfile', s)
            f.write(content)
        zf.write(f'working/{s}.json', mpath+f'{s}.json')

def otherflora(zf):
    for s in ['lily_pad', 'sugar_cane']:
        zf.write(f'pack-constants/pregen/{s}.json', mpath + f'{s}.json')
    for s in ['vine_1', 'vine_1u', 'vine_2', 'vine_2u', 'vine_2_opposite', \
            'vine_2u_opposite', 'vine_3', 'vine_3u', 'vine_4', 'vine_4u', \
            'vine_u']:
        zf.write(f'{s}.json', mpath + f'{s}.json')

def fungi(zf):
    for s in ['red_mushroom', 'brown_mushroom', 'crimson_fungus', 'warped_fungus']:
        zf.write(f'{s}.json', mpath + f'{s}.json')
    for s in ['red_mushroom_top', 'red_mushroom_bottom', 'brown_mushroom_top', \
            'brown_mushroom_bottom', 'warped_fungus_top', 'warped_fungus_bottom', \
            'crimson_fungus_bottom', 'crimson_fungus_top']:
        zf.write(f'textures/{s}.png', tpath + f'{s}.png')

def rails(zf):
    for s in ['activator_rail', 'activator_rail_on', 'activator_rail_on_raised_ne',\
            'activator_rail_on_raised_sw', 'activator_rail_raised_ne',\
            'activator_rail_raised_sw', 'detector_rail', 'detector_rail_f',\
            'detector_rail_on', 'detector_rail_on_raised_ne', 'detector_rail_on_raised_sw',\
            'detector_rail_raised_ne', 'detector_rail_raised_sw', 'golden_rail_f',\
            'master_activator_rail_raised_ne', 'master_activator_rail_raised_sw',\
            'master_detector_rail_raised_ne', 'master_detector_rail_raised_sw',\
            'master_golden_rail_raised_ne', 'master_golden_rail_raised_sw',\
            'powered_rail', 'powered_rail_on', 'powered_rail_on_raised_ne', \
            'powered_rail_on_raised_sw', 'powered_rail_raised_ne',\
            'powered_rail_raised_sw', 'rail_activator_f', 'rail_curved',\
            'rail_flat', 'template_rail_raised_ne', 'template_rail_raised_sw']:
        zf.write(f'pack-constants/pregen/{s}.json', mpath + f'{s}.json')

def redstone(zf):
    for s in ['redstone_dust_dot', 'redstone_dust_side', 'redstone_dust_side_alt',\
            'redstone_dust_up']:
        zf.write(f'pack-constants/pregen/{s}.json', mpath + f'{s}.json')

def otherblocks(zf):
    zf.write(f'pack-constants/pregen/ladder.json', mpath + f'ladder.json')
    for s in ['chain', 'template_hanging_lantern', 'template_lantern',\
            'stonecutter', 'iron_bars_post', 'iron_bars_post_ends', 'iron_bars_side',\
            'iron_bars_side_alt']:
        zf.write(f'{s}.json', mpath + f'{s}.json')
    
    zf.write('cross.json', mpath+'thick_cross.json')
    for s in ['cobweb']:
        with open(f'working/{s}.json', 'w') as f:
            content = basic_json.replace('$parent', 'thick_cross')
            content = content.replace('$textname', 'cross')
            content = content.replace('$textfile', s)
            f.write(content)
        zf.write(f'working/{s}.json', mpath+f'{s}.json')

if __name__ == "__main__":
    main()
