# Based on the help from https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm

import numpy as np
import random
import cv2

width = 200
height = 200
grid = [[{"in":False, "frontier": False, "dir":[]} for j in range(height)] for i in range(width)]
frontier = []
line_thickness = 1
draw_margin = 20
image = np.ones((width*4 + draw_margin, height*4 + draw_margin)) * 255

def add_frontier(x, y):
    if x >= 0 and x < height and y < width and y >= 0 and grid[x][y]["in"] == False and grid[x][y]["frontier"] == False:
        grid[x][y]["frontier"] = True
        frontier.append([x,y]) 

def mark(x, y):
    grid[x][y]["in"] = True
    grid[x][y]["frontier"] = False
    add_frontier(x-1, y)
    add_frontier(x+1, y)
    add_frontier(x, y-1)
    add_frontier(x, y+1)

def neighbors(x, y):
    n = []

    if x > 0 and grid[x-1][y]["in"] == True:
        n.append([x-1, y])
    if x+1 < height and grid[x+1][y]["in"] == True:
        n.append([x+1, y])
    if y > 0 and grid[x][y-1]["in"] == True:
        n.append([x, y-1])
    if y+1 < width and grid[x][y+1]["in"] == True:
        n.append([x, y+1])
    
    return n

def direction(x, y, nx, ny):
    if x < nx:
        return "s"
    if x > nx:
        return "n" 
    if y < ny:
        return "e" 
    if y > ny:
        return "w" 
    print("FAILED in direction")
    exit()

def opposite_direction(dir):
    if dir == "e":
        return "w"
    if dir == "w":
        return "e"
    if dir == "n":
        return "s"
    if dir == "s":
        return "n"

def opposite_list_direction(dir_list):
    lst = []
    if "n" not in dir_list:
        lst.append("n")
    if "s" not in dir_list:
        lst.append("s")
    if "e" not in dir_list:
        lst.append("e")
    if "w" not in dir_list:
        lst.append("w")
    return lst

def draw_line(r, c, element):
    if element == "n":
        cv2.line(image, (int(draw_margin/2) + r*4, int(draw_margin/2) + c*4), (int(draw_margin/2) + r*4, int(draw_margin/2) + c*4+4), (0, 255, 0), thickness=line_thickness)
    if element == "s":
        cv2.line(image, (int(draw_margin/2) + r*4+4, int(draw_margin/2) + c*4), (int(draw_margin/2) + r*4+4, int(draw_margin/2) + c*4+4), (0, 255, 0), thickness=line_thickness)
    if element == "e":
        cv2.line(image, (int(draw_margin/2) + r*4, int(draw_margin/2) + c*4+4), (int(draw_margin/2) + r*4+4, int(draw_margin/2) + c*4+4), (0, 255, 0), thickness=line_thickness)
    if element == "w":
        cv2.line(image, (int(draw_margin/2) + r*4, int(draw_margin/2) + c*4), (int(draw_margin/2) + r*4+4, int(draw_margin/2) + c*4), (0, 255, 0), thickness=line_thickness)

def draw_maze():
    for r, row in enumerate(grid):
        for c, column in enumerate(row):
            for element in opposite_list_direction(column["dir"]):
                draw_line(r, c, element)
    cv2.imshow("Image", image)
    cv2.waitKey()


def main():
    mark(np.random.randint(height, size=1)[0], np.random.randint(width, size=1)[0])
    while len(frontier) > 0:
        coords = random.choice(frontier)
        frontier.remove(coords)
        x = coords[0]
        y = coords[1]

        n = neighbors(x, y)
        n_coords = random.choice(n)
        nx = n_coords[0]
        ny = n_coords[1]

        dir = direction(x, y, nx, ny)
        grid[x][y]["dir"].append(dir)
        grid[nx][ny]["dir"].append(opposite_direction(dir))

        mark(x, y)
    draw_maze()





if __name__=="__main__":
    main()