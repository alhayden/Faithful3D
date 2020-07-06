#! /bin/python3

import json
from PIL import Image
from lib import *

def gen_mushroom(texture):

    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle':f'minecraft:{texture}', 
            'side':f'minecraft:block/{texture}',
            'top':f'minecraft:block/{texture}_top',
            'bottom':f'minecraft:block/{texture}_bottom'}
    elements = []


    icon = Image.open(f'textures/{texture}.png').convert('RGBA')
    edges = []
    for y in range(icon.height - 1, -1, -1):
        x = 0;
        edge = []
        while x < icon.width and icon.getpixel((x, y))[3] == 0:
            x += 1
        edges.append((icon.width // 2) - x)
    y = 0
    while y < icon.height:
        if edges[y] > 0 :
            i = 0
            while y + i + 1 < icon.height and edges[y + i + 1] == edges[y]:
                i += 1
            R = edges[y]
            voxel = {}
            voxel['from'] = [8 - R, y, 8 - R]
            voxel['to'] = [8 + R, y + i + 1, 8 + R]
            faces = {}
            faces['up'] = {'uv': [8 - R, 8 - R, 8 + R, 8 + R], 'texture': '#top'}
            faces['down'] = {'uv': [8 - R, 8 - R, 8 + R, 8 + R], 'texture': '#bottom'}
            faces['east'] = {'uv': [8 - R, 16 - (y + i + 1), 8 + R, 16 - y], 'texture': '#side'}
            faces['south'] = {'uv': [8 - R, 16 - (y + i + 1), 8 + R, 16 - y], 'texture': '#side'}
            faces['west'] = {'uv': [8 - R, 16 - (y + i + 1), 8 + R, 16 - y], 'texture': '#side'}
            faces['north'] = {'uv': [8 - R, 16 - (y + i + 1), 8 + R, 16 - y], 'texture': '#side'}

            voxel['faces'] = faces
            elements.append(voxel)

            y += i
        y += 1



    model['elements'] = elements
    with open(f'{texture}.json', 'w') as f:
        f.write(json.dumps(model))

def gen_cross():
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle':'#cross'}
    elements = []
    angles = [-45, 45]

    ## FACES
    for angle in angles:
        voxel = {}
        if angle == 45:
            voxel['from'] = [0, 0, 7]#swap for other center
            voxel['to'] = [16, 16, 8]
        else:
            voxel['from'] = [0, 0, 8]#swap for other center
            voxel['to'] = [16, 16, 9]
        voxel['rotation'] = {'origin': [8, 8, 8], 'axis': 'y', 'angle': angle, 'rescale': True}
        faces = {}
        faces['south'] = {'uv': [0, 0, 16, 16], 'texture': '#cross', 'rotation':0, 'tintindex':0}
        faces['north'] = {'uv': [16, 0, 0, 16], 'texture': '#cross', 'rotation':0, 'tintindex':0}
        voxel['faces'] = faces
        elements.append(voxel)

    ##TOP/BOTTOM
    for angle in angles:
        for y in range(0, 17):
            voxel = {}
            if angle == 45:
                voxel['from'] = [0, GAP[y], 7]#swap for other center
                voxel['to'] = [16, GAP[y], 8]
            else:
                voxel['from'] = [0, GAP[y], 8]#swap for other center
                voxel['to'] = [16, GAP[y], 9]
            voxel['rotation'] = {'origin': [8, 8, 8], 'axis': 'y', 'angle': angle, 'rescale': True}
            faces = {}
            if y > 0:
                faces['up'] = {'uv': [0, 16 - y, 16, 16 - (y-1)], 'texture': '#cross', 'rotation':0, 'tintindex':0}
            if y < 16:
                faces['down'] = {'uv': [0, 16 - y, 16, 16 - (y+1)], 'texture': '#cross', 'rotation':0, 'tintindex':0}
            voxel['faces'] = faces
            elements.append(voxel)

    ##SIDES
    for angle in angles:
        for x in range(0, 17):
            voxel = {}
            if angle == 45:
                voxel['from'] = [GAP[x], 0, 7]#swap for other center
                voxel['to'] = [GAP[x], 16, 8]
            else:
                voxel['from'] = [GAP[x], 0, 8]#swap for other center
                voxel['to'] = [GAP[x], 16, 9]
            voxel['rotation'] = {'origin': [8, 8, 8], 'axis': 'y', 'angle': angle, 'rescale': True}
            faces = {}
            if x > 0 and x != 8:#swap for other center
                faces['east'] = {'uv': [x, 0, x-1, 16], 'texture': '#cross', 'rotation':0, 'tintindex':0}
            if x < 16 and x != 7:#swap for other center
                faces['west'] = {'uv': [x, 0, x + 1, 16], 'texture': '#cross', 'rotation':0, 'tintindex':0}
            voxel['faces'] = faces
            elements.append(voxel)

    

    model['elements'] = elements

    with open('cross.json', 'w') as f:
        f.write(json.dumps(model))

def gen_chain():
    rotation = {"origin": [8, 8, 8], "axis": "y", "angle": 45}
    model = {}
    model["ambientocclusion"] = False
    model["textures"] = {"particle": "block/chain", "all": "block/chain"}
    elements = make_template([6.5, 0, 7.5], [9.5, 16, 8.5], '#all', [-6.5, 0])
    for element in elements:
        element['from'][1] += 0.001
        element['to'][1] += 0.001
    elements += make_template([7.5, 0, 6.5], [8.5, 16, 9.5], '#all', [-3.5, 0])
    addelementattr(elements, "rotation", rotation)
    for element in elements:
        element['from'] = [7.75 if x == 7.5 else x for x in element['from']]
        element['to'] = [8.25 if x == 8.5 else x for x in element['to']]
    model['elements'] = elements
    with open('chain.json', 'w') as f:
        f.write(json.dumps(model))

def gen_crop():
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle': '#crop'}
    elements = make_template([3, -1, 0], [4, 15, 16], '#crop', [0, 1])
    elements += make_template([0, -1, 3], [16, 15, 4], '#crop', [0, 1])
    elements += make_template([12, -1, 0], [13, 15, 16], '#crop', [0, 1], mirror=True)
    elements += make_template([0, -1, 12], [16, 15, 13], '#crop', [0, 1], mirror=True)
    model['elements'] = elements

    with open('crop.json', 'w') as f:
        f.write(json.dumps(model))

def gen_seagrass():
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle': '#texture'}
    elements = make_template([3, 0, 0], [4, 16, 16], '#texture')
    elements += make_template([0, 0, 3], [16, 16, 4], '#texture')
    elements += make_template([12, 0, 0], [13, 16, 16], '#texture', mirror=True)
    elements += make_template([0, 0, 12], [16, 16, 13], '#texture', mirror=True)
    addfaceattr(elements, 'tintindex', 0)
    model['elements'] = elements

    with open('template_seagrass.json', 'w') as f:
        f.write(json.dumps(model))

def gen_coral_wall():
    rotation = {"origin": [8, 8, 14], 'axis': 'x', 'angle': 22.5, 'rescale': True}
    rotation2 = {"origin": [8, 8, 14], 'axis': 'x', 'angle': -22.5, 'rescale': True}
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle': '#fan'}
    elements = addelementattr(make_template([0, 8, 0], [16, 9, 16], '#fan'), 'rotation', rotation)
    elements += addelementattr(make_template([0, 7, 0], [16, 8, 16], '#fan'), 'rotation', rotation2)
    model['elements'] = elements

    with open('coral_wall_fan.json', 'w') as f:
        f.write(json.dumps(model))

def gen_coral_fan():
    rotation0 = { "origin": [ 8, 0, 0 ], "axis": "z", "angle": 22.5, "rescale": False }
    rotation1 = { "origin": [ 8, 0, 0 ], "axis": "z", "angle": -22.5, "rescale": False }
    rotation2 = { "origin": [ 0, 0, 8 ], "axis": "x", "angle": -22.5, "rescale": False }
    rotation3 = { "origin": [ 0, 0, 8 ], "axis": "x", "angle": 22.5, "rescale": False }
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle': '#fan'}
    elements = addelementattr(make_template_flat([8, 0, 0], [24, 1, 16], '#fan', [-8, 0], 90), 'rotation', rotation0)
    elements += addelementattr(make_template_flat([-8, 0, 0], [8, 1, 16], '#fan', [8, 0], 270), 'rotation', rotation1)
    elements += addelementattr(make_template_flat([0, 0, 8], [16, 1, 24], '#fan', [0, -8], 180), 'rotation', rotation2)
    elements += addelementattr(make_template_flat([0, 0, -8], [16, 1, 8], '#fan', [0, 8], 0), 'rotation', rotation3)

    model['elements'] = elements

    with open('coral_fan.json', 'w') as f:
        f.write(json.dumps(model))

def gen_lantern():
    gen_hanging_lantern()
    gen_sitting_lantern()

def gen_hanging_lantern():
    rotation = { "origin": [ 8, 8, 8 ], "axis": "y", "angle": 45}
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle': '#lantern'}
    elements = []
    elements += make_template([6.5, 11, 7.5], [9.5, 15, 8.5], '#lantern', [-6.5 + 11, -11 + 1])
    for element in elements:
        element['from'][1] += 0.001
        element['to'][1] += 0.001
    elements += make_template([7.5, 10, 6.5], [8.5, 16, 9.5], '#lantern', [-6.5 + 11, -11 + 7])
    addelementattr(elements, "rotation", rotation)
    for element in elements:
        element['from'] = [7.75 if x == 7.5 else x for x in element['from']]
        element['to'] = [8.25 if x == 8.5 else x for x in element['to']]
    elements.append({   "from": [ 5, 1, 5 ],
            "to": [ 11, 8, 11 ],
            "faces": {
                "down":  { "uv": [  0, 9,  6, 15 ], "texture": "#lantern"},
                "up":    { "uv": [  0, 9,  6, 15 ], "texture": "#lantern" },
                "north": { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" },
                "south": { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" },
                "west":  { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" },
                "east":  { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" }
            }
        })
    elements.append({   "from": [ 6, 8, 6 ],
            "to": [ 10, 10, 10 ],
            "faces": {
                "down":  { "uv": [  1, 10,  5, 14 ], "texture": "#lantern"},
                "up":    { "uv": [  1, 10,  5, 14 ], "texture": "#lantern" },
                "north": { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" },
                "south": { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" },
                "west":  { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" },
                "east":  { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" }
            }
        })

    model['elements'] = elements

    with open('template_hanging_lantern.json', 'w') as f:
        f.write(json.dumps(model))

def gen_sitting_lantern():
    rotation = { "origin": [ 8, 8, 8 ], "axis": "y", "angle": 45}
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle': '#lantern'}
    elements = []
    elements += make_template([6.5, 9, 7.5], [9.5, 11, 8.5], '#lantern', [-6.5 + 11, -9 + 1])
    for element in elements:
        element['from'][1] += 0.001
        element['to'][1] += 0.001
    elements += make_template([7.5, 9, 6.5], [8.5, 11, 9.5], '#lantern', [-6.5 + 11, -9 + 10])
    addelementattr(elements, "rotation", rotation)
    for element in elements:
        element['from'] = [7.75 if x == 7.5 else x for x in element['from']]
        element['to'] = [8.25 if x == 8.5 else x for x in element['to']]
    elements.append({   "from": [ 5, 0, 5 ],
            "to": [ 11, 7, 11 ],
            "faces": {
                "down":  { "uv": [  0, 9,  6, 15 ], "texture": "#lantern", "cullface": "down" },
                "up":    { "uv": [  0, 9,  6, 15 ], "texture": "#lantern" },
                "north": { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" },
                "south": { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" },
                "west":  { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" },
                "east":  { "uv": [ 0, 2, 6,  9 ], "texture": "#lantern" }
            }
        })
    elements.append({   "from": [ 6, 7, 6 ],
            "to": [ 10, 9, 10 ],
            "faces": {
                "up":    { "uv": [  1, 10,  5, 14 ], "texture": "#lantern" },
                "north": { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" },
                "south": { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" },
                "west":  { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" },
                "east":  { "uv": [ 1, 0, 5,  2 ], "texture": "#lantern" }
            }
        })

    model['elements'] = elements

    with open('template_lantern.json', 'w') as f:
        f.write(json.dumps(model))



def gen_sunflower_top():
    rotation = {"origin": [ 8, 8, 8 ], "axis": "y", "angle": 45, "rescale": True}
    flower_rotation = { "origin": [ 8, 8, 8 ], "axis": "z", "angle": 22.5, "rescale": True }
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {"particle": "block/sunflower_front",
        "cross": "block/sunflower_top",
        "back": "block/sunflower_back",
        "front": "block/sunflower_front"}
    elements = make_template([0, 0, 7], [16, 16, 8], '#cross')
    elements += make_template([7, 0, 0], [8, 16, 16], '#cross')
    addelementattr(elements, 'rotation', rotation)

    flower_elements = make_template([8.6, 1, 1], [9.6, 17, 15], '#back', [0, -1])
    addelementattr(flower_elements, 'rotation', flower_rotation)
    for element in flower_elements:
        for face in element['faces']:
            if face == 'east':
                element['faces'][face]['texture'] = '#front'
    elements += flower_elements


    model['elements'] = elements

    with open('sunflower_top.json', 'w') as f:
        f.write(json.dumps(model))

def gen_vines():
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {"particle": "block/vine", "vine": "block/vine"}
    elements_s = addfaceattr(make_template([0, 0, 15], [16, 16, 16], '#vine'), 'tintindex', 0)
    elements_n = addfaceattr(make_template([0, 0, 0], [16, 16, 1], '#vine', mirror=True), 'tintindex', 0)
    elements_e = addfaceattr(make_template([15, 0, 0], [16, 16, 16], '#vine'), 'tintindex', 0)
    elements_w = addfaceattr(make_template([0, 0, 0], [1, 16, 16], '#vine', mirror=True), 'tintindex', 0)
    elements_u = addfaceattr(make_template_flat([0, 15, 0], [16, 16, 16], '#vine'), 'tintindex', 0)
    
    model['elements'] = elements_s
    with open('vine_1.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] += elements_u
    with open('vine_1u.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] = elements_n + elements_e
    with open('vine_2.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] += elements_u
    with open('vine_2u.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] = elements_w + elements_e
    with open('vine_2_opposite.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] += elements_u
    with open('vine_2u_opposite.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] = elements_n + elements_s + elements_e
    with open('vine_3.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] += elements_u
    with open('vine_3u.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] = elements_n + elements_s + elements_e + elements_w
    with open('vine_4.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] += elements_u
    with open('vine_4u.json', 'w') as f:
        f.write(json.dumps(model))
    model['elements'] = elements_u
    with open('vine_u.json', 'w') as f:
        f.write(json.dumps(model))

def gen_stonecutter():
    model = {}
    model["parent"] = "block/block"
    model["textures"] = {
        "particle": "block/stonecutter_bottom",
        "bottom": "block/stonecutter_bottom",
        "top": "block/stonecutter_top",
        "side": "block/stonecutter_side",
        "saw": "block/stonecutter_saw"
    }
    elements = addfaceattr(make_template([1, 9, 7.5], [15, 16, 8.5], '#saw'), 'tintindex', 0)
#    for element in elements:
#        element['from'] = [7.75 if x == 7.5 else x for x in element['from']]
#        element['to'] = [8.25 if x == 8.5 else x for x in element['to']]
    base = {   "from": [ 0, 0, 0 ],
            "to": [ 16, 9, 16 ],
            "faces": {
                "down":  { "uv": [ 0, 0, 16, 16 ], "texture": "#bottom", "cullface": "down" },
                "up":    { "uv": [ 0, 0, 16, 16 ], "texture": "#top" },
                "north": { "uv": [ 0, 7, 16, 16 ], "texture": "#side", "cullface": "north" },
                "south": { "uv": [ 0, 7, 16, 16 ], "texture": "#side", "cullface": "south" },
                "west":  { "uv": [ 0, 7, 16, 16 ], "texture": "#side", "cullface": "west" },
                "east":  { "uv": [ 0, 7, 16, 16 ], "texture": "#side", "cullface": "east" }
            }
        }
    elements.append(base)

    model['elements'] = elements
    with open('stonecutter.json', 'w') as f:
        f.write(json.dumps(model))

def gen_bars():
    ###### DEPRECATED IN FAVOR OF ARTISAN HANDCRAFTED MODEL ########
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {'particle':'block/iron_bars', 'bars': 'block/iron_bars'}

    elements = make_template([7, 0, 0], [8, 16, 8], '#bars')
    elements += make_template([8, 0, 0], [9, 16, 8], '#bars')
    model['elements'] = elements
    with open('iron_bars_side.json', 'w') as f:
        f.write(json.dumps(model))
    
    elements = make_template([7, 0, 8], [8, 16, 16], '#bars')
    elements += make_template([8, 0, 8], [9, 16, 16], '#bars')
    model['elements'] = elements
    with open('iron_bars_side_alt.json', 'w') as f:
        f.write(json.dumps(model))

def gen_fire():
    rotation0 = { "origin": [ 8, 8, 8 ], "axis": "x", "angle": -22.5, "rescale": True }
    rotation1 = { "origin": [ 8, 8, 8 ], "axis": "x", "angle": 22.5, "rescale": True }
    rotation2 = { "origin": [ 8, 8, 8 ], "axis": "z", "angle": -22.5, "rescale": True }
    rotation3 = { "origin": [ 8, 8, 8 ], "axis": "z", "angle": 22.5, "rescale": True }
    model = {}
    model['ambientocclusion'] = False
    model['textures'] = {"particle": "#fire"}
    elements = addelementattr(make_template([0, 0, 8], [16, 16, 9], '#fire'), 'rotation', rotation0)
    elements += addelementattr(make_template([0, 0, 7], [16, 16, 8], '#fire'), 'rotation', rotation1)
    elements += addelementattr(make_template([8, 0, 0], [9, 16, 16], '#fire'), 'rotation', rotation2)
    elements += addelementattr(make_template([7, 0, 0], [8, 16, 16], '#fire'), 'rotation', rotation3)

    addelementattr(elements, 'shade', False)
    model['elements'] = elements

    with open('template_fire_floor.json', 'w') as f:
        f.write(json.dumps(model))

    elements = addelementattr(make_template([0, 0, 0], [16, 16, 1], '#fire'), 'shade', False)
    model['elements'] = elements
    with open('template_fire_side.json', 'w') as f:
        f.write(json.dumps(model))



def main():
    gen_fire()
    gen_stonecutter()
    gen_coral_fan()
    gen_coral_wall()
    gen_chain()
    gen_crop()
    gen_cross()
    gen_seagrass()
    gen_lantern()
    gen_sunflower_top()
    gen_vines()
#    gen_mushroom('red_mushroom')


if __name__ == '__main__':
    main()

