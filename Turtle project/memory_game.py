
'''
    CS5001 Fall 2025
    Kartik Kulkarni
    Project
'''
from turtle import Turtle
from card import Card, Button, Border
import random
import time

'''
----------------X------------------------------X-----------------------SCREEN DESIGN-------------------X----------------------X----------------------------X------------------------------X
'''

def board_design():
    '''
        This function designs the game backdrop and displays it on screen
    '''
    global game, SPRITES

    # Create and set the wallpapers and borders as objects at its respective positions
    playar = Button(SPRITES[7], -130, 55)
    leaderboardar = Button(SPRITES[8], 263, 55)
    statusar = Button(SPRITES[9], -130, -265)
    buttonar = Button(SPRITES[10], 263, -265)
    playbr = Border(Turtle(), 523, 520)
    leaderboardbr = Border(Turtle(), 240, 520)
    statusbr = Border(Turtle(), 523, 100)
    buttonbr = Border(Turtle(), 240, 100)

    # Bordering the game
    playbr.draw('#e675ff', 10, -390, 315)
    leaderboardbr.draw('#f1b3ff', 10, 143, 315)
    statusbr.draw('#d000ff', 10, -390, -215)
    buttonbr.draw('#e675ff', 10, 143, -215)
        
    game.color('black')
    
def update_leaderboard(filename: str):
    '''
        This function takes the leaderboard file as input
        It displays the best scores of the leaderboard for the game onto the turtle screen
    '''
    global game, SPRITES

    # Tries to read leaderboard file, and display error if occured while opening file
    leader_file = ''
    try:
        leader_file = open(filename)
        leaders = (leader_file.read()).split('\n')
        leader_file.close()
        
    except FileNotFoundError:
        print("Leaderboard file missing!")
        error_alert(4)

    # Each element of list scores is a list that stores one score from ldrbd list
    scores = []
    for score in leaders:
        details = score.split(' ')
        scores.append(details)
        
    ypos = 215
    game.penup()
    game.goto(265, 265)
    game.write("LEADERBOARDS", align = "center", font = ('Arial',19,'bold'))
    game.hideturtle()

    # Empty leaderboard
    if len(scores) == 1:
        return
    
    for i in range(1, len(scores)): # Iterate through scores
        
        if i > 8: # Want only upto 8 scores
            break
        best_score = int(scores[1][1])
        best_scorer = scores[1][0]
        
        for j in range(1, len(scores)): # Picks best score of every iteration
            if scores[j][0] == '': #Empty line
                break
            if int(scores[j][1]) < best_score:
                best_score = int(scores[j][1])
                best_scorer = scores[j][0]
                
        # Code to actually write the best score onto screen
        game.goto(163,ypos)
        game.write(best_scorer + ":" + str(best_score), align = "left", font = ('Arial', 16))

        # Updating ypos for next score
        ypos = ypos - 56

        # Remove score from list once added to screen.
        scores.remove([best_scorer, str(best_score)])
        
    game.hideturtle()
    
def render_buttons():
    '''
        This function initialises and renders the quit and load buttons on the screen
    '''
    global quit_button, load_button, game, SPRITES
    
    # Quit button
    quit_button = Button(SPRITES[1], 223, -265)
    quit_button.turtle.shape(quit_button.value)

    # Load button
    load_button = Button(SPRITES[2], 303, -265)
    load_button.turtle.shape(load_button.value)
    
    
def render_game() -> list:
    '''
        This function creates and positions the card objects
        on the board to the respective format
        Returns the list containing card turtles as output
    '''
    global game, X_8_CARDS, Y_8_CARDS, X_10_CARDS, Y_10_CARDS, X_12_CARDS, Y_12_CARDS, SPRITES, num_cards, deck, card_order
    cards = []
    
    for i in range(8, 14, 2): # For 8, 10 and 12 cards (each layout)
        if num_cards == i: 
            for j in range(i): # Creates required cards, assigns card back gif
                cards.append(Card()) 
                cards[j].value = deck[card_order[j]]
                cards[j].turtle = Turtle()
                cards[j].turtle.penup()
                cards[j].turtle.shape(SPRITES[0])
            
    for i in range(len(cards)): # Moves cards to nessecary positions
        if len(cards) == 8: # 8 card layout
            cards[i].move(X_8_CARDS[i], Y_8_CARDS[i])
        elif len(cards) == 10: # 10 card layout
            cards[i].move(X_10_CARDS[i], Y_10_CARDS[i])
        else: # 12 card layout
            cards[i].move(X_12_CARDS[i], Y_12_CARDS[i])
    return cards
    
def update_status():
    '''
        This function updates the status section of the game
    '''
    global matches, guesses, game_status # Points to game_status text turtle()
    
    # Clears previous text
    game_status.penup()
    game_status.goto(-130, -280)
    game_status.clear()
    game_status.write("Guesses: " + str(guesses) + ", Matches: " + str(matches), align = "center", font = ('Arial', 20))

'''
----------------X------------------------------X------------------------ GAME EVENTS -------------------X----------------------X----------------------------X------------------------------X
'''

def screen_click(x, y, cards):
    '''
        This function deals with the click operation
        It executes the necessary function depending on the cursors position
        Takes the x and y positions of cursor and the card objects as input
    '''
    global quit_button, load_button, SPRITES, busy
    
    if busy: # Click function already in progress
        return # Stops unnecessary clicks from registering
    busy = True

    # Check if cursor in zone of cards
    check_click_card(cards, x, y)
    
    if quit_button.x - 30 <= x and quit_button.x + 30 >= x and quit_button.y - 20 <= y and quit_button.y + 20 >= y:
        # If in quit zone
        click_quit(cards)

    elif load_button.x - 30 <= x and load_button.x + 30 >= x and load_button.y - 20 <= y and load_button.y + 20 >= y:
        # If in load zone
        click_load(cards)      
    busy = False

def click_quit(cards):
    '''
        This function deals with the quitting operation of the game
        Takes cards as input to render the quitting animation
    '''
    global game

    # Quitting animation
    for card in cards:
        card.disappear()

    # Roll credits
    roll_credits()

    # Quit message
    game.clear()
    game.goto(-130,75)
    game.showturtle()
    game.shape(SPRITES[5])
    time.sleep(2)
    game.screen.bye()

def click_load(cards):
    '''
        This function deals with the loading operation of the game
        Takes cards as input to render animations or to update their designs
    '''
    global SPRITES, game_status, card_order

    # Takes user input and reads file
    file_name = game_status.screen.textinput("Load file", "Please enter the name of your config file")

    # For blank input
    if file_name is None or file_name == '':
        game_status.clear()
        game_status.write("No file entered. continuing...", align = 'center', font = ('Arial', 20))
        error_animation(cards)
        return
    
    # Any other cases
    user_deck = read_config(file_name)
    if user_deck == [] or 2 * len(user_deck) < len(card_order): # If file not found or empty or lacks sufficient cards
        game_status.clear()
        if len(user_deck) == 0: # File empty or not found
            game_status.write("File empty or not found. continuing...", align = 'center', font = ('Arial', 18))
            
        else: # File lacks sufficient cards
            game_status.write("File does not have enough cards! continuing....", align = 'center', font = ('Arial', 15))

        # Error animation to display gif image
        error_animation(cards)

    else: # File recieved in proper formatting
        
        for i in range(len(card_order)): # Changes the value of the card to the new deck
            cards[i].change_design(user_deck[card_order[i]])
            
        # Update user with status
        game_status.clear()
        game_status.goto(-130,-280)
        game_status.write("Deck Uploaded Succesfully!", align = 'center', font = ('Arial', 20))
        time.sleep(2)
        update_status()

def error_animation(cards):
    '''
        This function does the error missage display animation
        in the center of the play area when called,
        stops for a while then continues the game
    '''
    global card_order, game_status, SPRITES
    
    # Animation removing the center row cards to display error
    if len(card_order) == 10:
        for i in range(3,7):
            cards[i].disappear()
             
    elif len(card_order) == 12:
        for i in range(4,8):
            cards[i].disappear()

    # Display error gif
    game_status.goto(-130, 75)
    game_status.showturtle()
    game_status.shape(SPRITES[3])
    time.sleep(2.5)

    # Animation to show the center row cards again
    if len(card_order) == 10:
        for i in range(3,7):
            if not cards[i].matched: # If card status not matched, only then make the card appear
                cards[i].appear() 
    elif len(card_order) == 12:
        for i in range(4,8):
            if not cards[i].matched: # If card status not matched, only then make the card appear
                cards[i].appear()
    game_status.hideturtle()
    update_status()

def error_alert(error_number):
    '''
        This function makes the game display a specific error and then exits
    '''
    global SPRITES, game
    
    game.penup()
    game.goto(-130, 75)
    game.showturtle()
    game.shape(SPRITES[error_number])
    time.sleep(2.5)
    game.screen.bye()

def victory():
    '''
        This function executes the section after completing the game
    '''
    global SPRITES, guesses, game

    # Roll Credits
    roll_credits()
    
    # Display victory message
    victory = Turtle()
    victory.penup()
    victory.goto(-130, 75)
    victory.shape(SPRITES[6])

    #Update leaderboard
    add_to_leader(guesses, 'leaderboard.txt')
    time.sleep(3)
    game.screen.bye()

def roll_credits():
    '''
        Calling this function rolls the credits
    '''
    global game_status

    # Updates Game status to show credits
    game_status.clear()
    game_status.goto(game_status.xcor() - 120, game_status.ycor() - 20)
    game_status.write("Credits", font = ('Arial', 50))

    # Initializing credits text turtle
    START_CREDITS = 315
    lines = Turtle()
    lines.penup()
    lines.hideturtle()
    lines.goto(-375, 315)
    
    END_CREDITS = -205
    speed = 17

    #Each time, we clear, and write again slightly below the previous statement
    while lines.ycor() > END_CREDITS: # Credits above bottom of play area
        lines.clear()
        lines.goto(-375, lines.ycor() - speed)
        lines.color('purple')
        lines.write("Game Design and Program : KARTIK KULKARNI\n\n\nGame Concept and Update gifs : CS5001 COURSE CONTENT\n\n\nWallpaper gifs : ChatGPT, GEMINI Nano Banana", align = "left", font = ("Arial", 13, 'bold'))
        time.sleep(0.125)
    time.sleep(2)
    lines.clear()
    
    
'''
----------------X------------------------------X----------------------- GAME LOGIC -------------------X----------------------X----------------------------X------------------------------X
'''

def get_num_of_cards()-> int:
    '''
        This function obtains the number of cards that the user wants to play with and returns it
        window does not disappear till correct input has been entered.
    '''
    global game
    switch = True
    number = game.screen.textinput("Choose!","# of cards to play with (8, 10 or 12)")
    while switch: 
        if number in ['8', '10', '12']:
            switch = False # Loop set to stop repeating
            
        else:
            number = game.screen.textinput("Error!","Sorry! 8, 10 or 12 only")
            
    return int(number)

def check_click_card(cards, x, y):
    '''
        This function exectues a card flip if clicked on the cards
        If the first card has already been selected, then it checks the values of the two cards
    '''
    global card_number_one, card_number_two, card_one, card_two, card_order
    
    for i in range(len(cards)):
        if cards[i].x - 50 <= x and cards[i].x + 50 >= x and cards[i].y - 75 <= y and cards[i].y + 75 >= y and cards[i].flipped == False:
            # If in card zone
            if card_number_one == -1: # Card one not picked till now

                # Assigns as card one and flips it
                card_one = cards[i]
                card_number_one = i
                cards[i].flip()
            else: # Card one already picked

                # Assigns as card 2 and then checks values
                card_two = cards[i]
                card_number_two = i
                cards[i].flip()
                time.sleep(1.5)
                check(card_order)

                # If matches reaches max value
                if matches == len(cards) / 2:
                    victory()

def check(card_order):
    '''
        This function checks the two given selected cards
        and resets the game for the next round
    '''
    global card_one, card_two, card_number_one, card_number_two, matches, guesses, game, SPRITES
    
    if card_order[card_number_one] == card_order[card_number_two]: # Both cards are the same
        matches = matches + 1 # Increase matches by 1
        card_one.match()
        card_two.match() # Matches both cards
    else: # Both cards are different
        guesses = guesses + 1 # Increase guesses by 1
        card_one.flip() 
        card_two.flip() # Flips the cards over

    # Update game status after round
    update_status()

    # Resets global variables to default (currently none) value
    card_number_one = card_number_two = card_one = card_two = -1

def generate() -> list:
    '''
        This function returns a randomly generated list allotting each card to a skin number from whichever config file is selected
        it returns a list containing the index number of the card photo to be used on the card at the list index
    '''
    global num_cards
    if num_cards == 8: # For 8 cards
        final_list = [0, 0, 1, 1, 2, 2, 3, 3]
    elif num_cards == 10: # For 10 cards
        final_list = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    else: # For 12 cards
        final_list = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

    # Shuffling list to randomize
    random.shuffle(final_list)
    return final_list
    
'''
----------------X------------------------------X-----------------------FILES RELATED-------------------X----------------------X----------------------------X------------------------------X
'''

def read_config(filename: str) -> list:
    '''
        This function reads the contents of any config file
        Outputs a list of the card file names (empty if no file)
    '''
    global game
    
    # Try to open and read specific file, and return empty list if failed
    config_data = ''
    try:
        config_file = open(filename)
        config_data = config_file.read()
        config_file.close()
    except FileNotFoundError:
        return []

    # Converted to a list with entries of file content
    deck = config_data.split('\n')

    # Registers the shapes that are being read on the screen
    for i in range(len(deck)):
        game.screen.register_shape(deck[i])
        
    return deck
    

def add_to_leader(num_of_guess: int, filename: str):
    '''
        This function updates the leaderboards file
        with the contents of new score of the player
    '''
    global name
    
    # If file not found, print error (no alert because the alert shown when file not found during game start-up)
    try:
        file = open(filename, 'a')

        #Writes to file in the format 'name score'
        file.write('\n' + name + ' ' + str(num_of_guess))
        file.close()
    except FileNotFoundError:
        print("Error in updating leaderboard")



'''
----------------X------------------------------X-----------------------ALL GLOBAL VARIABLES / CONSTANTS-------------------X----------------------X----------------------------X------------------------------X
'''

# Keep track of matches and guesses in the game
matches = 0
guesses = 0

# Keep track of which cards has the user selected in the round
card_number_one = card_number_two = card_one = card_two = -1

# Main game turtle
game = Turtle()

# Turtle to update text of game status
game_status = Turtle()
game_status.color('black')
game_status.hideturtle()
game.screen.setup(width = 800, height = 650)

# Read and register all game images
SPRITES = read_config('pictures.txt')
if len(SPRITES) != 11:
    game.write("Missing / corrupted game sprite file \n'pictures.txt', cannot play game", font = (15))
    time.sleep(3.5)
    game.screen.bye()     
for i in range(11):
    game.screen.register_shape(SPRITES[i])

# Process the default deck
deck = read_config('config.txt')
if len(deck) == 0:
    game.penup()
    game.goto(-130, 75)

    # Default deck config file not found
    error_alert(3)

# Take name of user
name = game.screen.textinput("Welcome!", "Player name:")
if name is None or name == '':
    name = "N/A"

# Gets number of cards from user
num_cards = get_num_of_cards()

# Generates the order array for the game
card_order = generate()

# Intitialize buttons for global functional use
quit_button = ''
load_button = ''

# The following constants describe the coordinate layouts of the cards for each mode
X_8_CARDS = [-285, -180, -75, 30] * 2
Y_8_CARDS = [225, 225, 225, 225, -115, -115, -115, -115]
X_10_CARDS = [-285, -127, 31, -285, -180, -75, 30, -285, -127, 31]
Y_10_CARDS = [225, 225, 225, 55, 55, 55, 55, -115, -115, -115]
X_12_CARDS = [-285, -180, -75, 30] * 3
Y_12_CARDS = [225, 225, 225, 225, 55, 55, 55, 55, -115, -115, -115, -115]

busy = False

'''
----------------X------------------------------X-----------------------MAINLOOP-------------------X----------------------X----------------------------X------------------------------X
'''
        
def main():
    global game, game_status, cards, SPRITES, num_cards, deck, card_order

    # Design Turtle screen for game
    board_design()
    render_buttons()
    update_leaderboard('leaderboard.txt')
    update_status()

    # Places the cards on turtle screen and hides loading screen
    cards = render_game()

    # Onclick function
    game.screen.onclick(lambda x, y: screen_click(x, y, cards))
    game.screen.mainloop()
if __name__ == '__main__':
    main()
