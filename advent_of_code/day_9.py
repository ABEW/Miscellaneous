#!/usr/bin/env python3

def main():
#    input_path = "./temp_data_9_2.txt"
    input_path = (__file__).replace(".py","_input.txt")
    
    lookup = {"U": (0,1), "D": (0,-1), "L": (-1,0), "R": (1,0)}

    with open(input_path,"r") as f:
        all_steps = list(map(lambda x: (x[0],int(x[1])), [x.split() for x in f]))
    print("PART ONE")
    run_part_1(all_steps)

    print("PART TWO")
    run_part_2(all_steps)

def run_part_1(all_steps):
    lookup = {"U": (0,1), "D": (0,-1), "L": (-1,0), "R": (1,0)}
    
    head_pos = (0,0)
    tail_pos = [(0,0)]

    for step in all_steps:
        for _ in range(step[1]):
            movement = lookup[step[0]]            
            head_pos = (head_pos[0]+movement[0], head_pos[1]+movement[1])
            pos_diff = (head_pos[0]-tail_pos[-1][0], head_pos[1]-tail_pos[-1][1])

            if max(list(map(lambda x: abs(x), pos_diff)))<2:
                continue
            # head moved too far
            else:
                pos_updates = [(v<0)*-1 + (v>0) for v in pos_diff]

                tail_pos.append((tail_pos[-1][0]+pos_updates[0], tail_pos[-1][1]+pos_updates[1]))
    
    unique_tails = set([str(x)+","+str(y) for x,y in tail_pos])
    print(f"The tail visits {len(unique_tails)} unique positions")

def run_part_2(all_steps):
    lookup = {"U": (0,1), "D": (0,-1), "L": (-1,0), "R": (1,0)}
    
    rope = [(0,0) for i in range(10)]
    tail_visit = [(0,0)]

    for step in all_steps:
#        print(rope)
        for _ in range(step[1]):
            movement = lookup[step[0]]
            head_pos = rope[0]
            rope[0] = (head_pos[0]+movement[0], head_pos[1]+movement[1])
#            print(rope)
            for i in range(1,10):
                head_pos = rope[i-1]
                tail_pos = rope[i]

                pos_diff = (head_pos[0]-tail_pos[0], head_pos[1]-tail_pos[1])

                if max(list(map(lambda x: abs(x), pos_diff)))<2:
                    continue
                # head moved too far
                else:
                    pos_updates = [(v<0)*-1 + (v>0) for v in pos_diff]

                    rope[i] = (tail_pos[0]+pos_updates[0], tail_pos[1]+pos_updates[1])
                if i==9:
                    tail_visit.append(rope[i])
    print(f"The tail visits {len(set(tail_visit))} unique positions")

if __name__ == "__main__":
    main()
