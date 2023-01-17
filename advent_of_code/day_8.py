#!/usr/bin/env python3

import os
import re
from pprint import pprint

from collections import deque,defaultdict
from functools import reduce

def get_scenic_score(input_data):
    scores = defaultdict(lambda: [0,0,0,0])
    
    # direction [N, E, S, W]
    # x is row count, y is column count
    def _calculate_score(x,y,direction):
        idx = str(x)+","+str(y)
            
        movement = [0+((direction+1)%2)*(direction-1), 0+((direction%2)*(direction-2))]
        new_x, new_y = [x+movement[0], y+movement[1]]
        
        while (0<=new_x<len(input_data)) and (0<=new_y<len(input_data[0])) and (int(input_data[x][y]) > int(input_data[new_x][new_y])):
            scores[idx][direction] += 1
            new_x, new_y = [new_x+movement[0], new_y+movement[1]]
        if (0<=new_x<len(input_data)) and (0<=new_y<len(input_data[0])):
            scores[idx][direction] += 1    
    
    for i in range(len(input_data)):
        for j in range(len(input_data[0])):
            idx = str(i)+","+str(j)
            _ = [_calculate_score(i,j,my_dir) for my_dir in range(4)]
    
    for k, v in scores.items():
        v.append(reduce(lambda x,y: x*y, v))
    
    print(f"The best tree has a scenic score of {max([x[-1] for x in scores.values()])}.")

def main():
#    input_path = "temp_data_8.txt"
    input_path = (__file__).replace(".py","_input.txt")

    with open(input_path,"r") as f:
        input_data = [x.strip("\n") for x in f]
    
    row_size = len(input_data)
    col_size = len(input_data[0])

    left_max = []#[-1]*row_size]
    right_max = []#[-1]*row_size]
    top_max = [[-1]*col_size]
    bot_max = [[-1]*col_size]
    
    for i,row in enumerate(input_data):
        top_temp=[]
        bot_temp=[]
        left_temp=[-1]
        right_temp=[-1]
        for j,col in enumerate(row):
            col = int(col)
            right_data = int(row[col_size-1-j])
            bot_data = int(input_data[row_size-1-i][j])

            top_temp.append(max(col,top_max[-1][j]))
            bot_temp.append(max(bot_data,bot_max[-1][j]))
            
            left_temp.append(max(col,left_temp[-1]))
            right_temp.append(max(right_data,right_temp[-1]))
        
        top_max.append(top_temp)
        bot_max.append(bot_temp)

        left_max.append(left_temp)#[1:])
        right_max.append(right_temp)#[1:])
    
    top_max = top_max#[1:]
    bot_max = bot_max[::-1]
    right_max = [x[::-1] for x in right_max]
    
    visibility = []
    visible_count = 0
    
    for i in range(row_size):
        visibility.append([])
        for j in range(col_size):
            is_visible = any(
                list(
                    map(
                        lambda x: int(input_data[i][j])>x,
                        [
                            top_max[i][j],
                            bot_max[i+1][j],
                            left_max[i][j],
                            right_max[i][j+1]
                        ]
                    )
                )
            )
            visible_count += int(is_visible)
            visibility[-1].append(is_visible)
    
    print(f"There are {visible_count} trees visible")
    
    get_scenic_score(input_data)


if __name__ == "__main__":
    main()
