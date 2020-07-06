
GAP = {0:0, 1:0.9725, 2:1.9765, 3:2.9805, 4:3.984, 5:4.98825, 6:5.992, 7:6.996, 8:8}
for g in range(0, 9):
    GAP[16-g] = 16-GAP[g]
GAP_OFFSETS = [0, -0.0275, -0.0235, -0.0195, -0.016, -0.01175, -0.008, -0.004, 0, 0.004, 0.008, 0.01175, 0.016, 0.0195, 0.0235, 0.0275, 0]


def make_template(start, end, texture, offset=[0, 0], mirror=False, drop=[]):
    limits = [int(abs(start[x] - end[x])) for x in range(3)]
    if 1 not in limits:
        print(limits)
        print("No dimension is thickness 1")
        3 / 0
    ns = ('north', 'south')
    ew = ('east', 'west')
    ud = ('up', 'down')

    if(mirror):
        ns = ('south', 'north')
        ew = ('west', 'east')
        ud = ('down', 'up')

#    gapstart = [GAP.setdefault(start[i], start[i]) for i in range(3)]
#    gapend = [GAP.setdefault(end[i], end[i]) for i in range(3)]

    flat = [ew, ud, ns][limits.index(1)]
    mask = [((0, 0, 1), (0, 1, 0)), ((1, 0, 0), (0, 0, 1)), ((1, 0, 0), (0, 1, 0))][limits.index(1)]
    
    uvstart = domask(start, mask)
    uvend = domask(end, mask)

    x = offset[0]
    y = offset[1]

    elements = []

    ## FLAT FACE
    voxel = {}
    voxel['from'] = start
    voxel['to'] = end
    faces = {}
    faces[flat[1]] = {'uv':[x + uvstart[0], y + uvstart[1], x + uvend[0], y + uvend[1]], "texture": texture}
    faces[flat[0]] = {'uv':[x + uvend[0], y + uvstart[1], x + uvstart[0], y + uvend[1]], "texture": texture}
    
    if 'down' in faces:
        faces['down']['rotation'] = 180

    voxel['faces'] = faces
    elements.append(voxel)

    ## SIDE 1
    if ew != flat:
        if flat == ud:
            ew = ew[::-1]
        for i in range(limits[0] + 1):
            voxel = {}
            loc = start[0] + i
            if mirror or flat == ud:
                loc = end[0] - i
            voxel['from'] = [loc, start[1], start[2]]
            voxel['to'] = [loc, end[1], end[2]]
            faces = {}
            if i > 0:
                faces[ew[0]] = {'uv': [ x + uvstart[0] + i, y + uvstart[1], x + uvstart[0] + i - 1, y + uvend[1]], 'texture': texture}
            if i < limits[0]:
                faces[ew[1]] = {'uv': [ x + uvstart[0] + i, y + uvstart[1], x + uvstart[0] + i + 1, y + uvend[1]], 'texture': texture}

            if flat == ud:
                if 'east' in faces:
                    faces['east']['rotation'] = 90
                if 'west' in faces:
                    faces['west']['rotation'] = 270

            voxel['faces'] = faces

            elements.append(voxel)

    ## SIDE 2
    if ud != flat:
        for i in range(limits[1] + 1):
            voxel = {}
            locx = [start[0], end[0]]
            locz = [start[2], end[2]]
            if mirror and flat == ns:
                locx = [end[0], start[0]]
            if mirror and flat == ew:
                locz = [end[2], start[2]]

            voxel['from'] = [locx[0], end[1] - i, locz[0]]
            voxel['to'] = [locx[1], end[1] - i, locz[1]]
            faces = {}
            if i < limits[1]:
                faces[ud[0]] = {'uv': [x + uvstart[0], y + uvstart[1] + i, x + uvend[0],  y + uvstart[1] + i + 1], 'texture': texture}
            if i > 0:
                faces[ud[1]] = {'uv': [x + uvstart[0], y + uvstart[1] + i, x + uvend[0],  y + uvstart[1] + i - 1], 'texture': texture}

            if flat == ew:
                for f in faces:
                    faces[f]['rotation'] = 90
                    if f == 'down':
                        faces[f]['rotation'] = 270
            voxel['faces'] = faces
            elements.append(voxel)
    
    ## SIDE 3
    if ns != flat:
        for i in range(limits[2] + 1):
            voxel = {}
            loc = start[2] + i
            if mirror:
                loc = end[2] - i
            voxel['from'] = [start[0], start[1], loc]
            voxel['to'] = [end[0], end[1], loc]
            faces = {}
            if i < limits[2]:
                faces[ns[0]] = {'uv': [ x + uvstart[0] + i, y + uvstart[1], x + uvstart[0] + i + 1, y + uvend[1]], 'texture': texture}
            if i > 0:
                faces[ns[1]] = {'uv': [ x + uvstart[0] + i, y + uvstart[1], x + uvstart[0] + i - 1, y + uvend[1]], 'texture': texture}
            voxel['faces'] = faces
            
            if flat == ud:
                if 'north' in faces:
                    faces['north']['rotation'] = 180
                if 'south' in faces:
                    faces['south']['rotation'] = 0
                for face in faces.values():
                    face['uv'] = face['uv'][::-1]
            
            elements.append(voxel)
    if start[0] in range(-64, 64) and start[1] in range(-64, 64) and start[2] in range(-64, 64):
        fixgapsrel(elements, start)
    return elements

def make_template_flat(start, end, texture, offset=[0, 0], rotation=0, reflect=False):
    elements = []

    limits = [end[x] - start[x] for x in range(3)]
    dx = offset[0]
    dy = offset[1]
    dxm = offset[0] + limits[0]
    dym = offset[1] + limits[2]
    antirotation = (360 - rotation) % 360
    ## top and bottom:
    voxel = {}
    voxel['from'] = start
    voxel['to'] = end
    faces = {}
    faces['up'] = {'uv': [dx + start[0], dy + start[2], dx + end[0], dy + end[2]], 'texture': texture}
    faces['down'] = {'uv': [dx + start[0], dy + end[2], dx + end[0], dy + start[2]], 'texture': texture}
    faces['up']['rotation'] = rotation
    faces['down']['rotation'] = antirotation
    voxel['faces'] = faces
    elements.append(voxel)

    ## east and west:
    for i in range(limits[0] + 1):
        voxel = {}
        voxel['from'] = [start[0] + i] + start[1:]
        voxel['to'] = [start[0] + i] + end[1:]
        faces = {}
        if rotation == 0:
            if i > 0:
                faces['east'] = {'uv': [dx + start[0] + i, dy + start[2], dx + start[0] + i - 1, dy + end[2]], 'texture': texture, 'rotation': 90}
            if i < limits[0]:
                faces['west'] = {'uv': [dx + start[0] + i, dy + start[2], dx + start[0] + i + 1, dy + end[2]], 'texture': texture, 'rotation': 270}
        if rotation == 90:
            if i > 0:
                faces['east'] = {'uv': [dx + start[0], dym + start[2] - i, dx + end[0], dym + start[2] - i + 1], 'texture': texture, 'rotation': 180}
            if i < limits[0]:
                faces['west'] = {'uv': [dx + start[0], dym + start[2] - i, dx + end[0], dym + start[2] - i - 1], 'texture': texture, 'rotation': 0}
        if rotation == 180:
            if i > 0:
                faces['east'] = {'uv': [dxm + start[0] - i, dy + start[2], dxm + start[0] - i + 1, dy + end[2]], 'texture': texture, 'rotation': 270}
            if i < limits[0]:
                faces['west'] = {'uv': [dxm + start[0] - i, dy + start[2], dxm + start[0] - i - 1, dy + end[2]], 'texture': texture, 'rotation': 90}
        if rotation == 270:
            if i > 0:
                faces['east'] = {'uv': [dx + start[0], dy + start[2] + i, dx + end[0], dy + start[2] + i - 1], 'texture': texture, 'rotation': 0}
            if i < limits[0]:
                faces['west'] = {'uv': [dx + start[0], dy + start[2] + i, dx + end[0], dy + start[2] + i + 1], 'texture': texture, 'rotation': 180}
        voxel['faces'] = faces
        elements.append(voxel)


    ## north and south:
    for i in range(limits[2] + 1):
        voxel = {}
        voxel['from'] = start[:2] + [start[2] + i]
        voxel['to'] = end[:2] + [start[2] + i]
        faces = {}
        if rotation == 0:
            if i > 0:
                faces['south'] = {'uv': [dx + start[0], dy + start[2] + i, dx + end[0], dy + start[2] + i - 1], 'texture': texture, 'rotation': 0}
            if i < limits[2]:
                faces['north'] = {'uv': [dx + start[0], dy + start[2] + i, dx + end[0], dy + start[2] + i + 1], 'texture': texture, 'rotation': 180}
        if rotation == 90:
            if i > 0:
                faces['south'] = {'uv': [dx + start[0] + i, dy + start[2], dx + start[0] + i - 1, dy + end[2]], 'texture': texture, 'rotation': 90}
            if i < limits[2]:
                faces['north'] = {'uv': [dx + start[0] + i, dy + start[2], dx + start[0] + i + 1, dy + end[2]], 'texture': texture, 'rotation': 270}
        if rotation == 180:
            if i > 0:
                faces['south'] = {'uv': [dx + start[0], dym + start[2] - i, dx + end[0], dym + start[2] - i + 1], 'texture': texture, 'rotation': 180}
            if i < limits[2]:
                faces['north'] = {'uv': [dx + start[0], dym + start[2] - i, dx + end[0], dym + start[2] - i - 1], 'texture': texture, 'rotation': 0}
        if rotation == 270:
            if i > start[2]:
                faces['south'] = {'uv': [dxm + start[0] - i, dy + start[2], dxm + start[0] - i + 1, dy + end[2]], 'texture': texture, 'rotation': 270}
            if i < end[2]:
                faces['north'] = {'uv': [dxm + start[0] - i, dy + start[2], dxm + start[0] - i - 1, dy + end[2]], 'texture': texture, 'rotation': 90}
        voxel['faces'] = faces
        elements.append(voxel)


    if start[0] in range(-64, 64) and start[1] in range(-64, 64) and start[2] in range(-64, 64):
        fixgapsrel(elements, start)
    return elements


def domask(val, mask):
    return [sum([val[i] * mask[d][i] for i in range(len(val))]) for d in range(len(mask))]

def fixgaps(elements):
    for element in elements:
        for vertex in 'to', 'from':
            element[vertex] = [gap(element[vertex][x]) for x in range(len(element[vertex]))]

def fixgapsrel(elements, start):
    for element in elements:
        for vertex in 'to', 'from':
            element[vertex] = [element[vertex][x] + GAP_OFFSETS[element[vertex][x] - start[x]] for x in range(len(element[vertex]))]

def gap(x):
    if x not in GAP:
        return x
    return GAP[x]

def addelementattr(elements, key, attr):
    for element in elements:
        element[key] = attr
    return elements

def addfaceattr(elements, key, val):
    for element in elements:
        for face in element['faces'].values():
            face[key] = val
    return elements

