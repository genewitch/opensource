import pygame
from secrets import randbelow

pygame.init()
oneD= []
lineOut = []
w,h = 400,400
ScrSize = (w,h)
Origin  = (0,0)
Gray    = (200,200,200)
screen = pygame.display.set_mode(ScrSize)
world = pygame.Surface((ScrSize[0], ScrSize[1]*2))
world.fill(Gray)

# initial state

for n in range (0,w+2):
    oneD.append(randbelow(2))

#for n in range (0, w+2):
#    oneD.append(0)
##oneD.append(1)

##for #30:
#oneD[int(w/2)] = 1

for n in range (0, w+2):
    lineOut.append(0)


print("initial state done")

#rules = [0,0,0,1,1,1,1,0] #30
rules = [0,	1,	0, 	1, 	1, 	0, 	1, 	0] #90
#rules = [ 0,1,1,0,1,1,1,0 ] # 110
#rules = [ 0,1,1,0,1,1,1,1 ] # 111
while(True):
    for row in range (0,h):
        for t in range (1,w+1):
            if oneD[t-1:t+2] == [1,1,1]:
                lineOut[t] = rules[0]

            elif oneD[t-1:t+2] == [1,1,0]:
                lineOut[t] = rules[1]

            elif oneD[t-1:t+2] == [1,0,1]:
                lineOut[t] = rules[2]

            elif oneD[t-1:t+2] == [1,0,0]:
                lineOut[t] = rules[3]

            elif oneD[t-1:t+2] == [0,1,1]:
                lineOut[t] = rules[4]

            elif oneD[t-1:t+2] == [0,1,0]:
                lineOut[t] = rules[5]

            elif oneD[t-1:t+2] == [0,0,1]:
                lineOut[t] = rules[6]

            elif oneD[t-1:t+2] == [0,0,0]:
                lineOut[t] = rules[7]

            else:
                print("BONKERS")
                
        if row % 50 == 0:
            print(".",end = '')
        for pixel in range (1,w):
            if lineOut[pixel] == 1:
                world.set_at((pixel,row), (0,0,0))
                #d.point((pixel,row),fill="black")
            else:
                world.set_at((pixel,row), (255,255,255))                

        #this was the bug, rofl
        lineOut[0] = oneD[w]
        lineOut[w] = oneD[0]
        oneD = list(lineOut)
        screen.blit(world,(0,0))
        
    pygame.display.update()
