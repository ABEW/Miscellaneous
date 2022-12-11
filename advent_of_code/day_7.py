#!/usr/bin/env python3
import pdb

import os
import re
from collections import deque,defaultdict
import bisect
import pprint

def main():
    input_path = (__file__).replace(".py","_input.txt")
    
    input_stream=[]
    
    with open(input_path,"r") as f:
        for line in f:
            input_stream.append(line.strip("\n"))
    
    curr_dir = "."
    file_dict = {".":[]} #defaultdict(list)
    all_file_size = 0   
    i = 0  
    while i < len(input_stream):
        val = input_stream[i]
#        pdb.set_trace()
        if val.startswith("$"):
            cmd_line = val.split()
            if (cmd_line[1]=="cd") and (cmd_line[2]==".."):
                curr_dir = "/".join(curr_dir.split("/")[:-1])
            elif (cmd_line[1]=="cd") and (cmd_line[2]=="/"):
                curr_dir = "."
            elif cmd_line[1]=="cd":
                curr_dir += "/"+cmd_line[2]
            i += 1
        else:
#            print(curr_dir)
            if curr_dir not in file_dict:
                file_dict[curr_dir]=[]

            while (i<len(input_stream) and not input_stream[i].startswith("$")):
                x, y = input_stream[i].split()
                y = curr_dir + "/" + y
                if x=="dir":
                    if y not in file_dict:
                        file_dict[y]=[]
                    if y not in file_dict[curr_dir]:
                        file_dict[curr_dir].append(y)
                else:
                    y = y+'_f'
                    if y not in file_dict[curr_dir]:
                        file_dict[curr_dir].append(y)
                        file_dict[y] = int(x)
                        all_file_size += int(x)
                i += 1
    
    size_to_clear = 30_000_000 - (70_000_000 - all_file_size)
    
    print(len(file_dict))
    print(f"Total size of everything: {all_file_size}")
    print(f"Size to remove is : {size_to_clear}")    
    result = dict()

    def get_size(curr):
        if curr in result:
            return result[curr]
        if isinstance(file_dict[curr],int):
            result[curr] = file_dict[curr]
            return file_dict[curr]
#        print(curr)
        curr_size = 0.0
        for child in file_dict[curr]:
            if isinstance(child,int):
                curr_size += child
                continue
            curr_size += get_size(child)
        
        result[curr]=curr_size
        return curr_size

    get_size(".")
    
    dirs_with_less_100k = [(k,v) for k,v in result.items() if (v<=100000 and not k.endswith("_f"))]
    sorted_dirs = sorted(list(result.items()), key=lambda x: x[1])
    dir_to_remove =  sorted_dirs[bisect.bisect_left([x[1] for x in sorted_dirs],size_to_clear)]  
    
#    pprint.pprint(sorted_dirs)
    print(f"The sum of their total sizes is {sum(x[1] for x in dirs_with_less_100k)}")
    print(f"Directory to be removed is {dir_to_remove}") 

#    while len(my_queue) > 0:
#        curr_dir = my_queue[-1]
#        if curr_dir in visited:
#            my_queue.pop()
#            continue
#        curr_size = 0
#        if curr_dir not in file_dict:
#            result[curr_dir]=file_size[curr_dir]
#            visited.add(curr_dir)
#            continue
#        if len(file_dict[curr_dir]==0):
#            result[curr_dir]=curr_size
#            visited.add(curr_dir)
#            continue
#
#        for child in file_dict[curr_dir]:
#            if child in visited:
#                result[curr_dir] += result[child]
#            else:
#                my_queue.append(child)
                
if __name__ == "__main__":
    main()
