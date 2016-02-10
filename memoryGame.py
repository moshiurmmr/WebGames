# implementation of card game - Memory

# author: M. Moshiur Rahman

import simplegui
import random

lst = range(0, 8)
card_dec = lst + lst
random.shuffle(card_dec)
card_size = 50
turn = 0 # tracks the card turns

# helper function to initialize globals
def new_game():
    global state, exposed, turn, card1_idx, card2_idx
    state = 0
    turn = 0
    card1_idx = -2
    card2_idx = -2
    random.shuffle(card_dec)
    exposed = [False, False, False, False, False, False, False, False, 
           False, False, False, False, False, False, False, False]
    label.set_text(str(turn))
    
     
# define event handlers
def mouseclick(pos):
    global state, card1_idx, card2_idx, turn
    idx = pos[0] / 50
    print turn
    if state == 0:
        if exposed[idx] == False:
            exposed[idx] = True
            turn += 1
            label.set_text(str(turn))
            card1_idx = idx
            state = 1
    elif state == 1:
        if exposed[idx] == False:
            exposed[idx] = True
            #turn += 1  
            #label.set_text(str(turn))
            card2_idx = idx
            state = 2
        else:
            turn = turn
            exposed[idx] = True
            state = 1
        
    else:
        if exposed[idx] == False:
            exposed[idx] = True
            turn += 1
            label.set_text(str(turn))
            state = 1
            if card_dec[card1_idx] == card_dec[card2_idx]:
                exposed[card1_idx] = True
                exposed[card2_idx] = True
                card1_idx = idx
            else:
                exposed[card1_idx] = False
                exposed[card2_idx] = False
                card1_idx = idx
        else:
            turn = turn
            exposed[idx] = True
            state = 2        
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    x_num = 0 
    for i in range(len(card_dec)):
        if exposed[i] == True:
            canvas.draw_text(str(card_dec[i]), [x_num + 10, 60], 50, "White" )
            x_num += card_size
         
        elif exposed[i] == False:
            canvas.draw_polygon([(x_num, 0), (x_num + card_size, 0), (x_num + card_size, 100), (x_num, 100), (x_num, 0)], 1, 'Black', 'Green')
            x_num += card_size
   
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label_t = frame.add_label("Turn")
label = frame.add_label("Turns = 0")
label.set_text(str(turn))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
