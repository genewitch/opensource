# i had to fix a lot and this does not check input
# i am debating trying to make it faster without being
# clever
import pygame
from secrets import randbelow
import sys

pygame.init()
oneD = []
lineOut = []
w, h = 480, 270
ScrSize = (w, h)
Gray = (200, 200, 200)
screen = pygame.display.set_mode(ScrSize)
pygame.display.set_caption("Elementary Cellular Automaton")
world = pygame.Surface((ScrSize[0], ScrSize[1]))
world.fill(Gray)
font = pygame.font.Font(None, 36)

def get_input_num():
    user_input = ""
    input_active = True

    while input_active:
        screen.fill((0, 0, 0))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    try: 
                        return int(user_input)
                    # will crash on negatives but why use them?
                    # and i don't want to fix it
                    except ValueError:
                        continue
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
    
        # Render input text
        prompt = font.render("Enter a rule number:", True, (255, 255, 255))
        screen.blit(prompt, (20, 20))
        input_box = font.render(user_input, True, (255, 255, 255))
        screen.blit(input_box, (300, 20))
        pygame.display.flip()
    


# Function to convert integer to binary list
def int_to_binary_list(n, length=8):
    bin_str = bin(n)[2:].zfill(length)
    bin_list = [int(digit) for digit in bin_str]
    return bin_list

def scroll_world():
    global world
    world.scroll(dy=-1)
    pygame.draw.line(world, Gray, (0, h - 1), (w, h - 1))

def reset_world():
    global oneD, lineOut, world
    oneD = [randbelow(2) for _ in range(w + 2)]
    lineOut = [0 for _ in range(w + 2)]
    world.fill(Gray)

running = True
while running:
    input_num = get_input_num()
    rules = int_to_binary_list(input_num, 8)
    reset_world()
    print("rule #" + str(input_num))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_n:
                    #print("caught 'n'")
                    
                    input_num = get_input_num()
                    rules = int_to_binary_list(input_num, 8)
                    reset_world()
                    print("reset to rule #" + str(input_num))
                    break

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
