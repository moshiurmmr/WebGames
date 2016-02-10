# Mini-project #6 - Blackjack

# author: M. Moshiur Rahman

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
wins = 0
looses = 0

is_player_busted = False
is_dealer_busted = False
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# global variables for canvas
hand_pos = [50, 400]
dealer_pos = [50, 200]


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        #print pos
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):
        hand_str = ''
        for c in range(len(self.hand)):
            hand_str += ' ' +(str(self.hand[c]))
        return str('Hand is:') + str(hand_str)

    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        value = 0
        num_ace = 0
        rnks = ''
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        for card in self.hand:
            rnk = card.rank
            value += VALUES[rnk]
            rnks += rnk
        if 'A' not in rnks:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
   
    def draw(self, canvas, pos):
        i = 0   
        for card in self.hand:
            if i <= 5:
                pos[0] = 50 + i * CARD_SIZE[0]
                card.draw(canvas, pos)
                i += 1        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))          

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        # deal a card object from the deck
        return random.choice(self.deck)
    
    def __str__(self):
        # return a string representing the deck
        deck_str = ''
        for c in range(len(self.deck)):
            deck_str += ' ' +(str(self.deck[c]))
        return str('Deck contains') + str(deck_str)



#define event handlers for buttons
def deal():
    global in_play
    global deck, player_hand, dealer_hand, wins, looses
    # create a deck object and shuffle it
    deck = Deck()
    deck.shuffle()
    # create a player and dealer hands
    player_hand = Hand()
    dealer_hand = Hand()
    # deal 2 cards to player
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    # deal 2 cards to dealer
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    # if pressed the deal button in the middle of the game
    if in_play == True:
        looses += 1
        print "You loose for pressing Deal button in the middle of the game!"

    # player_hand is in play
    in_play = True
    
def hit():
    global in_play, wins, looses
    global player_hand, dealer_hand
    # if the hand is in play, hit the player
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        print "Delaer' score: ", dealer_hand.get_value()
        print "Player's score: ", player_hand.get_value()
        print "Player's hand:", player_hand
    else:
        print "Player got busted!"
        print "Delaer' score: ", dealer_hand.get_value()
        print "Player's score: ", player_hand.get_value()
        looses += 1
        
def stand():
    global in_play, score, wins, looses
    # replace with your code below
    in_play = False
    if player_hand.get_value() > 21:
        print "The player is busted!"
        print "Delaer' score: ", dealer_hand.get_value()
        print "Player's score: ", player_hand.get_value()
        looses += 1
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            print "The dealer is busted!"
            print "Delaer' score: ", dealer_hand.get_value()
            print "Player's score: ", player_hand.get_value()
            wins += 1
        elif player_hand.get_value() <= dealer_hand.get_value():
            print "The dealer wins !"
            print "Delaer' score: ", dealer_hand.get_value()
            print "Player's score: ", player_hand.get_value()
            looses += 1
        else:
            print "The player wins!"
            print "Delaer' score: ", dealer_hand.get_value()
            print "Player's score: ", player_hand.get_value()
            wins += 1
            
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack',[70, 80], 35, 'Red' )
    canvas.draw_text('Wins = ' + str(wins) + '   ' + 'Looses = ' + str(looses), [300, 80], 25, 'Black')
    canvas.draw_text('Dealer',[50, 150], 30, 'Black' )
    dealer_hand.draw(canvas, dealer_pos)
    canvas.draw_text('Player',[50, 350], 30, 'Black' )
    canvas.draw_text('Hit or Stand?', [230, 350], 30, 'Black')
    player_hand.draw(canvas, hand_pos)
    
    # Hide the first card of the dealer_hand when not in_play
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_CENTER[0], CARD_BACK_CENTER[1] + 200 ], CARD_BACK_SIZE)
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
#deal()
player_hand = Hand()
dealer_hand = Hand()
frame.start()


# remember to review the gradic rubric
