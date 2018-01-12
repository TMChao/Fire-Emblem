import map

size = width,height = 8,6
map = []

for i in range(height):
    temp = []
    for j in range(width):
        temp.append((i+j)%2+1)
    map.append(temp)

def seac(x, y, distance, map):

    #向上
    if x > 0 and distance[x - 1][y] > distance[x][y] + map[x - 1][y]:
        distance[x - 1][y] = distance[x][y] + map[x-1][y]
        seac(x-1, y, distance, map)
        
    #向下
    if x < height - 1 and distance[x + 1][y] > distance[x][y] + map[x + 1][y]:
        distance[x + 1][y] = distance[x][y] + map[x + 1][y]
        seac(x + 1, y, distance, map)
        
    #向左
    if y > 0 and distance[x][y - 1] > distance[x][y] + map[x][y - 1]:
        distance[x][y - 1] = distance[x][y] + map[x][y - 1]
        seac(x, y - 1, distance, map)
    #向右
    if y < width - 1 and distance[x][y +  1] > distance[x][y] + map[x][y + 1]:
        distance[x][y + 1] = distance[x][y] + map[x][y + 1]
        seac(x, y + 1, distance, map)


def get_dis(x, y, map):
    distance = []
    for i in range(len(map)):
        temp = []
        for j in range(len(map[0])):
            temp.append(1000)
        distance.append(temp)
    distance[x][y] = 0
    seac(x, y, distance, map)
    return distance
    
dis = get_dis(0,0,map)

