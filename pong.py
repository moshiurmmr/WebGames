# implementation of classic arcade game Pong

# author: M. Moshiur Rahman

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_vel = [3, 4]
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    #ball_vel = [0, 0]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -random.randrange(2, 4)
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(2, 4)
        ball_vel[1] = -random.randrange(2, 4)
    ball_pos = [WIDTH / 2 + ball_vel[0], HEIGHT/2 + ball_vel[1]]
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [0, 0]
    paddle2_pos = [WIDTH, 0]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global RIGHT, LEFT # my global
    #paddle1_pos[0] = paddle1_pos[0] + paddle1_vel [0]
    paddle1_pos[1] = paddle1_pos[1] + paddle1_vel [1]
    #paddle2_pos[0] = paddle2_pos[0] + paddle2_vel [0]
    paddle2_pos[1] = paddle2_pos[1] + paddle2_vel [1]
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    '''
    Test when the ball hits the top or bottom walls
    '''
    if ball_pos[1] <= BALL_RADIUS :
    # if the ball hits the top wall
        #ball_pos[0] = ball_pos[0] + 10
        ball_pos[1] = ball_pos[1] + HEIGHT / 2
        #ball_vel[1] =  10
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        # if the ball hits the bottom wall
        ball_pos[1] = HEIGHT - BALL_RADIUS - HEIGHT / 2
        #ball_pos[0] = ball_pos[0] + 10
    else:
        ball_pos[1] = ball_pos[1]
        
    ''''
    Test the ball collision with left and right walls
    '''
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
    # check when the ball hits the left wall
        if (ball_pos[1] + BALL_RADIUS) < paddle1_pos[1]:
            # ball hits the left gutter above the paddle1
            RIGHT = True
            LEFT = False
            spawn_ball(RIGHT)
            score2 += 1
            
            '''
            print "Ball hit the left gutter"
            print "score1 = ", score1
            print "score2 = ", score2
            print "Right is: ", RIGHT
            print "Left is: ", LEFT
            '''
        elif (ball_pos[1] - BALL_RADIUS) > (paddle1_pos[1] + PAD_HEIGHT):
            # ball hits the left gutter below the paddle1
            RIGHT = True
            LEFT = False
            spawn_ball(RIGHT)
            score2 += 1
        else:
            # ball hists paddle1
            #print "ball hits paddle1."
            RIGHT = True
            LEFT = False
            spawn_ball(RIGHT) 
            
            
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):
        # check when the ball hits the right-paddle
        if (ball_pos[1] + BALL_RADIUS) < paddle2_pos[1]:
            # ball hits the right gutter above the paddle1
            RIGHT = False
            LEFT = True
            spawn_ball(LEFT)
            score1 += 1
        elif (ball_pos[1] - BALL_RADIUS) > (paddle2_pos[1] + PAD_HEIGHT):
            # ball hits the rigth gutter below the paddle1
            RIGHT = False
            LEFT = True
            spawn_ball(LEFT)
            score1 += 1
        else:
            # ball hists paddle2
            #print "ball hits paddle2."
            RIGHT = False
            LEFT = True
            spawn_ball(LEFT)
   
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 3, "Red", "White" )
    # update paddle's vertical position, keep paddle on the screen
    
    # draw paddles
    if paddle1_pos[1] < 0:
        paddle1_pos[1] = 0
    elif paddle1_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    else:
        paddle1_pos[1] = paddle1_pos[1]
    if paddle2_pos[1] < 0:
        paddle2_pos[1] = 0
    elif paddle2_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
    else:
        paddle2_pos[1] = paddle2_pos[1]
    canvas.draw_line(paddle1_pos, [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH*2, "Blue")
    canvas.draw_line(paddle2_pos, [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH*2, "Blue")
     
    # draw scores
    canvas.draw_text( str(score1), [150, 50], 50, 'Green')
    canvas.draw_text( str(score2), [450, 50], 50, 'Green')
   
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] += 6
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] += 6
    else:
        paddle1_vel[1] = 0
        paddle2_vel[1] = 0
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] -= 6
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = -6
    else:
        paddle1_vel[1] = 0
        paddle2_vel[1] = 0

def restart_game():
    global score1, score2
    new_game()
    score1 = 0
    score2 = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
# Register even handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart_game, 70)
# start frame
new_game()
frame.start()


