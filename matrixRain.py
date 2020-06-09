import random
import curses
import time
import sys
import string

#Returns the dimension of the console screen
def max_dimensions(window):
    height, width = window.getmaxyx()
    return height - 2, width - 1

#Initialize the library. 
#Return a WindowObject which represents the whole screen.
stdscr = curses.initscr()

screenLength, screenWidth = max_dimensions(stdscr)

dropLength = []
for i in range (screenWidth):
    dropLength.append(random.randrange(int(screenLength/3)-4,int(screenLength/2)-4))

#Sets inertial/basic posion of beginning of rain
#Setting the basic dimensions for printing
rain = []
for i in range (screenWidth):
    rain.append(i%(screenLength+1))
#Shuffle inertial/basic posion of beginning of rain randomly random number of time
for i in range (random.randrange(1,5)):
    random.shuffle(rain)

#Processing function
def main(window, speed):
    curses.start_color()
    #Setting basic colours
    #green
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    #white
    curses.init_pair(2, curses.COLOR_WHITE,  curses.COLOR_BLACK)
    #transperent or black
    curses.init_pair(3,  curses.COLOR_BLACK,  curses.COLOR_BLACK)
    
    #To limit the length of the rain or time of rain
    rainLength = screenLength*3
    
    for i in range (rainLength):
        '''
        #for infinite rain
        if not i%screenLength:
            i = 0
        '''
        for j in range(screenWidth):
            '''
            #setting rendom (Unicode) Kanji (Japanese) charecter to print
            random_ints = random.sample(range(0x30A0,0x30FF), 1)
            random_unicodes = [chr(x) for x in random_ints]
            character = u"".join(random_unicodes)
            '''
            character = random.choice(string.ascii_lowercase)
            
            if i%screenLength == rain[j] or i == rain[j]:
                #White (1st position of drop)
                stdscr.addstr(0,j, character, curses.color_pair(2) + curses.A_BOLD)
            elif (i%screenLength == (rain[j]+1)%screenLength or i%screenLength == (rain[j]+2)%screenLength)  and i > rain[j]:
                #Light Green (2nd & 3rd position of drop)
                stdscr.addstr(0,j,character,curses.color_pair(1) + curses.A_BOLD)
            elif i%screenLength == (rain[j]+3)%screenLength and random.randrange(2) and i > rain[j]:
                # Light Green (may/may not be 3rd position of drop)
                stdscr.addstr(0,j,character , curses.color_pair(1) + curses.A_BOLD)   
            elif i > rain[j] and ((i%screenLength == (rain[j]+dropLength[j])%screenLength and random.randrange(2)) or i%screenLength == ((rain[j]+dropLength[j])-1)%screenLength or i%screenLength == ((rain[j]+dropLength[j])-2)%screenLength):
                #Dark Green (Tail position of drop)
                stdscr.addstr(0,j,character,curses.color_pair(1) + curses.A_DIM)
            else :
                #Balck (rest of the part)
                stdscr.addstr(0,j," ",curses.color_pair(3) + curses.A_DIM)
                number = [*range(3,dropLength[j])]
                for n in range (dropLength[j] - 4):
                    if i%screenLength == (rain[j]+number[n])%screenLength and i > rain[j]:
                        #Green (Body of drop)
                        stdscr.addstr(0,j,character , curses.color_pair(1)) 
                        
        #Refresh to screen
        stdscr.refresh()
        #Insert a blank line under the cursor. All following lines are moved down by one line.
        stdscr.insertln()
        
        #Wait
        try:
            time.sleep((0.1) / (speed / 100))
        except ZeroDivisionError:
            time.sleep(0.1)
     
    stdscr.getch()
    curses.endwin()
           
#int main(void) - Driver Code
#Made By : Saloni Raj
if __name__ == '__main__':
    speed = 100
    if len(sys.argv) > 1:
        try:
            speed = int(sys.argv[1])
        except ValueError:
            print(
                'Usage:\npython snowterm.py [SPEED]\n'
                'SPEED is integer representing percents.',
            )
            sys.exit(1)
    try:
        curses.wrapper(main, speed)
    except KeyboardInterrupt:
        sys.exit(0)
