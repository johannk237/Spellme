import pygame
import random
import datetime
import db

class HandlePygame():
    def __init__(self): 
        pygame.init()
        pygame.display.set_caption("spellMe")
        
        #SCREEN SIZE
        #-----------
        self.WIDTH, self.HEIGHT = (800, 600) #WIDTH & HEIGHT OF PIXELS
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FPS = 10
        #----------------------
        # NUM OF ROW & COLUMNS:
        #----------------------
        self.ROWS = 5
        self.COLUMNS = 5
        
        #-----------------------------
        #WIDTH & HEIGHT OF ANY OBJECT
        #-----------------------------
        self.OBJECT_WIDTH = 50 #I CAN: change value for each object
        self.OBJECT_HEIGHT = 40 #BOX_HEIGHT
        
        self.length = 500
        
        self.rects = []  # stores inputted parameters for functions
        
        #--------------------
        #SPACES BETWEEN BOXES:
        #--------------------
        self.GAPSIZE = 5
        self.SPACE = 20
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 65) #changes size of letter_position
        self.text = pygame.font.Font(None, 45)
        
        self.text_spell = pygame.font.Font(None, 55)

        #-----------------------------
        # SCREEN POSITION ON SCREEN
        #-----------------------------
        # Leftmost topmost coordinate where first rect will be drawn
        self.MARGIN_X = (self.WIDTH / 8)
        self.MARGIN_Y = (self.HEIGHT / 4)
    
    def update_pygame(self):
        pygame.display.update()
        self.clock.tick(self.FPS)


# class Boxe():
#     def __init__(self, screen, color, x, y, width, height):
#         self.square = [width, height]
#         self.pos = [x, y]
#         self.screen = screen
#         self.color = color
    
#     def draw_square(self):
#         box_dimensions = pygame.Rect(self.pos,self.square)# gets all  the dimensions and position of box
#         pygame.draw.rect(self.screen, self.color, box_dimensions, 2)  # Makes box outlines white
        

class Game():
    def __init__(self, level):
        self.connector = db.Connector("wordlist.txt")
        self.used_words = []
        self.guess_word = ""  # current word for each position
        self.num_of_guesses = 0  # currentword
        self.current_letter = 0  # letter_position posiion
        self.correct_letter = []
        self.incorrect_letter = []
        self.level = level
        self.file_select = ""
        self.start = datetime.datetime.now().replace(microsecond=0)
        #------------
        #GET WORDLIST
        #------------
        self.wordlist = [word.replace("\n", "") for word in list(open("wordlist.txt"))] #seperates word every new line, & gets random word
        
        self.list_select = []
        self.adjectives = [word.replace("\n", "") for word in list(open("adjectives.txt"))] #seperates word every new line, & gets random word
        self.adverb = [word.replace("\n", "") for word in list(open("adverb.txt"))] #seperates word every new line, & gets random word
        self.noun = [word.replace("\n", "") for word in list(open("noun.txt"))] #seperates word every new line, & gets random word
        self.verb = [word.replace("\n", "") for word in list(open("verb.txt"))] #seperates word every new line, & gets random word
        
        if self.level == 1:
            self.list_select = self.noun
            self.file_select = "Noun"
        if self.level == 2:
            for word in self.adverb:
                self.list_select.append(word)
            for word in self.verb:
                self.list_select.append(word)
            
        if self.level == 3:
            self.list_select = self.adjectives
            self.file_select = "Adjectives"
        

        # --------------
        # FLAGS
        # --------------
        self.flag_WIN = False  # checks if user wins
        self.flag_LOSE = False  # check if user has lost
        self.flag_WORD_INVALID = False
        self.flag_NOT_ENOUGH_LETTERS = False  # too little characters
        # ----------------------------------------------------------
        self.timer_flag_1 = 0  # the time to get it takes to flag/come on screen
        self.timer_flag_2 = 0
        
        #GET ANSWER_WORD
        self.answer_word = random.choice(self.list_select)  # getAnswer word in wordlist
        self.answer_word = self.answer_word.lower()  # turns answer word lowercase
        self.WORD_LENGTH = len(self.answer_word)
        print(self.answer_word)
        
        if self.answer_word not in self.wordlist:
            self.connector.save_word(self.answer_word)
            self.wordlist.append(self.answer_word)
        
        if self.level == 2:
            if self.answer_word.capitalize() in self.adverb:
                self.file_select = "Adverb"
            elif self.answer_word.capitalize() in self.verb:
                self.file_select = "Verb"
        
    def update_score(self):
        if self.num_of_guesses == 1:
            return 5
        elif self.num_of_guesses == 2:
            return 4
        elif self.num_of_guesses == 3:
            return 3
        elif self.num_of_guesses == 4:
            return 2
        elif self.num_of_guesses == 5:
            return 1
    
    def get_wordlist(self):
        return self.wordlist
    
    def get_list_select(self):
        return self.list_select

    def get_flag_WIN(self):
        return self.flag_WIN
    
    def get_flag_LOSE(self):
        return self.flag_LOSE
    
    def get_flag_WORD_INVALID(self):
        return self.flag_WORD_INVALID
    
    def get_flag_NOT_ENOUGH_LETTERS(self):
        return self.flag_NOT_ENOUGH_LETTERS
    
    def get_guess_word(self):
        return self.guess_word
    
    def get_current_letter(self):
        return self.current_letter
    
    def get_num_of_guesses(self):
        return self.num_of_guesses
    
    def get_used_words(self):
        return self.used_words
    
    def get_timer_flag_1(self):
        return self.timer_flag_1
    
    def get_timer_flag_2(self):
        return self.timer_flag_2
    
    def set_guess_word(self, new_value):
        self.guess_word = new_value
        
    def set_current_letter(self, new_value):
        self.current_letter = new_value
        
    def set_num_of_guesses(self, new_value):
        self.num_of_guesses = new_value
    
    def set_flag_WIN(self, new_value):
        self.flag_WIN = new_value
        
    def set_flag_LOSE(self, new_value):
        self.flag_LOSE = new_value
        
    def set_flag_WORD_INVALID(self, new_value):
        self.flag_WORD_INVALID = new_value
        
    def set_flag_NOT_ENOUGH_LETTERS(self, new_value):
        self.flag_NOT_ENOUGH_LETTERS = new_value
        
    def set_timer_flag_1(self, new_val):
        self.timer_flag_1 = new_val
    
    def set_timer_flag_2(self, new_val):
        self.timer_flag_2 = new_val
        
    def add_to_used_words(self, new_value):
        self.used_words.append(new_value)


class MyColor():
    def __init__(self):
        self.BLUE = (0, 0, 200)
        self.GREY = (211,211,211)
        self.DARK_GREY = (20, 20, 20)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 22, 108)
        self.SCREEN_COLOUR = (20, 20, 20)
        self.COLOUR_INCORRECT = (169,169,169) # colour: letter is not in answer word
        self.COLOR_MISPLACED = (255, 193, 53)  # colour: correct letter in wrong position
        self.COLOR_CORRECT = (0, 185, 6)  #colour: letter in correct position
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('grey15')