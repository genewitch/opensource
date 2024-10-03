# see https://mathworld.wolfram.com/ElementaryCellularAutomaton.html
# usage python elementalautomata.py number
# where number is an 8 bit integer of the rule you want to use.
# 45, 110, 167 are decent examples.
import pygame
from secrets import randbelow
import sys

# Check if there are enough arguments
if len(sys.argv) != 2:
    print("Usage: python pyprogram.py <number>")
    sys.exit(1)

# Get the input number from the command line argument
input_num = int(sys.argv[1])
print(f"Input number is: {input_num}")

pygame.init()
oneD = []
lineOut = []
w, h = 640, 640
ScrSize = (w, h)
Gray = (200, 200, 200)
screen = pygame.display.set_mode(ScrSize)
world = pygame.Surface((ScrSize[0], ScrSize[1]))
world.fill(Gray)

# initial state
for n in range(0, w+2):
    oneD.append(randbelow(2))

for n in range(0, w+2):
    lineOut.append(0)

print("initial state done")

def int_to_binary_list(n, length=8):
    # Convert integer to binary string, remove the "0b" prefix, and pad with leading zeros
    bin_str = bin(n)[2:].zfill(length)
    # Convert binary string to a list of integers
    bin_list = [int(digit) for digit in bin_str]
    return bin_list

# Example usage
#input_num = 110
rules = int_to_binary_list(input_num, 8)
print("rule #" + str(input_num))


#rules = [0,0,0,1,1,1,1,0] #30
#rules = [0,	1,	0, 	1, 	1, 	0, 	1, 	0] #90
#rules = [ 0,1,1,0,1,1,1,0 ] # 110
#rules = [ 0,1,1,0,1,1,1,1 ] # 111

def scroll_world():
    global world
    world.scroll(dy=-1)
    pygame.draw.line(world, Gray, (0, h - 1), (w, h - 1))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    for row in range(0, h):
        for t in range(1, w+1):
            if oneD[t-1:t+2] == [1, 1, 1]:
                lineOut[t] = rules[0]
            elif oneD[t-1:t+2] == [1, 1, 0]:
                lineOut[t] = rules[1]
            elif oneD[t-1:t+2] == [1, 0, 1]:
                lineOut[t] = rules[2]
            elif oneD[t-1:t+2] == [1, 0, 0]:
                lineOut[t] = rules[3]
            elif oneD[t-1:t+2] == [0, 1, 1]:
                lineOut[t] = rules[4]
            elif oneD[t-1:t+2] == [0, 1, 0]:
                lineOut[t] = rules[5]
            elif oneD[t-1:t+2] == [0, 0, 1]:
                lineOut[t] = rules[6]
            elif oneD[t-1:t+2] == [0, 0, 0]:
                lineOut[t] = rules[7]
            else:
                print("BONKERS")
                
        #if row % 50 == 0:
        #    print(".", end='')

        for pixel in range(1, w):
            if lineOut[pixel] == 1:
                world.set_at((pixel, h-1), (0, 0, 0))
            else:
                world.set_at((pixel, h-1), (255, 255, 255))
        
        lineOut[0] = oneD[w]
        lineOut[w] = oneD[0]
        oneD = list(lineOut)

        scroll_world()
        screen.blit(world, (0, 0))
        pygame.display.update()
        
pygame.quit()
