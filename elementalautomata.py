# i had to fix a lot 
# i am debating trying to make it faster without being
# clever
import pygame
from pygame.locals import *
from secrets import randbelow
import sys
import numbers
import base64
import math

pygame.init()
oneD = []
lineOut = []
w, h = 641, 360
state = []
history = 1
linecount = 0
marker = 0
rules = []
ScrSize = (w, h)
Gray = (200, 200, 200)
screen = pygame.display.set_mode((ScrSize), pygame.HWSURFACE|pygame.DOUBLEBUF)
#screen = pygame.display.set_mode((ScrSize), pygame.SCALED, vsync=True)
clock = pygame.time.Clock()  
pygame.display.set_caption("Elementary Cellular Automaton")
world = pygame.Surface((ScrSize[0], ScrSize[1]))
world.fill(Gray)
font = pygame.font.Font(None, 36)

def get_input_num():
    user_input = ""
    input_active = True

    while input_active:
        
        #screen.fill((0, 0, 0))        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    
                    try:                        
                        if int(user_input) >= 0:
                            input_active = False
                            return int(user_input)
                        else:
                            user_input = ""
                            break
                    except ValueError:
                        user_input = ""
                        break
                    except TypeError:
                        user_input = ""
                        break
    
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
    
        # Render input text
        pt = "Enter a rule number:\n"
        pt += "While running:\n"
        pt += "'R'estart   'N'umber\n"
        lines = pt.split('\n')
        y = 20
        for line in lines:
            prompt = font.render(line, True, (255, 255, 255))
            screen.blit(prompt, (20, y))
            y+=40
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
    global oneD, lineOut, world, linecount, marker
    linecount = 0
    marker = 0
    oneD = [randbelow(2) for _ in range(w + 2)]
    seed = get_base64(oneD)
    print("seed: " + seed)
    lineOut = [0 for _ in range(w + 2)]
    world.fill(Gray)

def get_base64(blist):
    binary_string = ''.join(map(str, blist))
    binary_bytes = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
    # Encode the bytes to base64
    base64_encoded = base64.b64encode(binary_bytes)
    # Decode to get the string
    base64_string = base64_encoded.decode('utf-8')
    return base64_string
    
import math

def custom_chisquare(observed, expected):
    return sum((o - e) ** 2 / e for o, e in zip(observed, expected))

def check_randomness(integers):
    if not integers:
        print("Empty list")
        return

    # Calculate observed frequencies
    observed = [integers.count(i) for i in set(integers)]
    total = sum(observed)
    
    # Calculate expected frequencies (assuming uniform distribution)
    expected = [total / len(observed)] * len(observed)
    
    # Perform custom chi-square test
    chi2 = custom_chisquare(observed, expected)

    # Simple heuristic for p-value approximation (for small values of chi2, assume higher p-value)
    p_value = math.exp(-0.5 * chi2)
    
    # If p-value is very low, it's not really random
    if p_value < 0.05:
        print("!r")
    else:
        print("R")

def is_unique_list(new_list, seen_lists, h):
    if new_list in seen_lists:
        return False
    if len(seen_lists) >= h:
        seen_lists.pop(0)  # Remove the oldest list to maintain the size limit
    seen_lists.append(new_list)
    return True


running = True
while running:
    pause = False
    if not rules:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_n}))
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
            elif event.key == pygame.K_r:
                reset_world()
                break
            elif event.key == pygame.K_h:
                history += 1
                print("history screenfulls: " + str(history))
                
    for row in range(0, h):
        for t in range(1, w+1):
            testee = oneD[t-1:t+2]
            if testee == [1, 1, 1]:
                lineOut[t] = rules[0]
            elif testee == [1, 1, 0]:
                lineOut[t] = rules[1]
            elif testee == [1, 0, 1]:
                lineOut[t] = rules[2]
            elif testee == [1, 0, 0]:
                lineOut[t] = rules[3]
            elif testee == [0, 1, 1]:
                lineOut[t] = rules[4]
            elif testee == [0, 1, 0]:
                lineOut[t] = rules[5]
            elif testee == [0, 0, 1]:
                lineOut[t] = rules[6]
            elif testee == [0, 0, 0]:
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
        linecount += 1
        
         #debug statement
        #check_randomness(oneD)
        if is_unique_list(oneD, state, h*history) == False:
            #print("non-uniq line found drrr")
            if marker == 0:
                marker = linecount                
            scrollinfo = font.render("non-uniqueness found at line: " + str(marker), True, (255, 255, 255))
            screen.blit(scrollinfo, (20, h-40))
            pygame.display.flip()
            
        scroll_world()    
        screen.blit(world, (0, 0))
        #pygame.display.update()
            
        pygame.display.flip()
    #clock.tick(60)
    
pygame.quit()
