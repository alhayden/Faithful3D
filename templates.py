def make_ud_template(start, end, texture, offset=[0, 0], mirror=False, drop = []):
    pass

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
    voxel['faces'] = faces
    elements.append(voxel)

    ## SIDE 1
    if ew != flat:
        for i in range(limits[0] + 1):
            voxel = {}
            loc = start[0] + i
            if flat == ud:
                ew = ew[::-1]
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
            elements.append(voxel)

    fixgaps(elements)
    return elements

