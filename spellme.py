import pygame
import sys
import settings
import leaderbord
import db
import datetime

class Spellme():
    def __init__(self, username):
        self.username = username
        self.connector = db.Connector("leaderbord.txt")
        self.myPygame = settings.HandlePygame()
        self.leaderbord = leaderbord.Leaderbord(self.username)
        self.color = settings.MyColor()
        self.score = 0
        self.level = 1
        self.win = 0
        self.test = 0
        self.color_letter = self.color.GREY
        self.times_list = []
        
    def start(self):
        self.myGame = settings.Game(self.level)
        
        
        while True:
            for event in pygame.event.get(): #get entered keys
                #QUIT IF THEY EXIT: # if type of event corresponds to quit then quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Update the screen on the each step of main loop of the game
                # pygame.display.update()
                # PLAY AGAIN: IF THEY FINISHED GAME
                
                if self.myGame.get_flag_WIN():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r: #If LETTER 'R' is pressed
                            self.test = 0
                            self.start()  # GO BACK TO MAIN GAME
                elif self.myGame.get_flag_LOSE():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r: #If LETTER 'R' is pressed
                            if self.score == 0:    
                                self.test = 0
                                self.start()  # GO BACK TO MAIN GAME
                            
                else:
                    # GO BACKWARDS TO REMOVE LETTER
                    if event.type == pygame.KEYDOWN:
                        # if BACKSPACE key is pressed
                        if event.key == pygame.K_BACKSPACE:
                            if self.myGame.get_guess_word():  # IF THERE IS CURRENT WORD ENTERED
                                self.myGame.set_guess_word(self.myGame.get_guess_word()[:-1])  #GET THE LAST LETTER IN GUESS_WORD
                                self.myGame.set_current_letter(self.myGame.current_letter-1)  # REMOVE LAST LETTER
                        elif event.key == pygame.K_RETURN: #if ENTER KEY is pressed
                            if len(self.myGame.get_guess_word()) == 5: #if the guess_word entered is ==5 or (len(ROWS) - 1)
                                if self.myGame.get_guess_word().lower() in self.myGame.get_wordlist(): #if guess word (lowercase) is in English wordlist
                                    #player has maxamum of 5 guesses
                                    self.myGame.set_num_of_guesses(self.myGame.get_num_of_guesses()+1) #number of guesses increased by 1
                                    self.myGame.add_to_used_words(self.myGame.get_guess_word()) #adds word used to list of used words
                                    self.myGame.set_guess_word("")
                                    self.myGame.set_current_letter(0)#get/go to letter position 0 in guess_Word; to help compare it to answer_word letter
                                else:
                                    self.myGame.set_flag_WORD_INVALID(True)
                                    self.myGame.set_timer_flag_1(0) #time it takes to load on screen: immeditately
                            else:
                                self.myGame.set_flag_NOT_ENOUGH_LETTERS(True)
                                self.myGame.set_timer_flag_2(0)
                        else:
                            if len(self.myGame.get_guess_word()) < self.myGame.WORD_LENGTH:  #
                                if event.unicode.isalpha():
                                    self.myGame.set_guess_word(self.myGame.get_guess_word()+event.unicode.upper())
                                    self.myGame.set_current_letter(self.myGame.get_current_letter()+1)
            
            self.screen()
    
    def screen(self):
        # ----------------
        # SCREENBOARD:
        # ----------------
        self.myPygame.SCREEN.fill(self.color.SCREEN_COLOUR)
        #draw_title(font) # draw title font

        #--------------------------------
        # RECT:GET BOX POSITIONS ON SCREEN
        #---------------------------------
        for y in range(self.myPygame.ROWS):
            boxes_position = []
            for x in range(self.myGame.WORD_LENGTH):  # each item in column
                position_x = (5/2)*self.myPygame.MARGIN_X + (x * self.myPygame.GAPSIZE) + (x * self.myPygame.OBJECT_WIDTH)  #Creates a box after every GAPSIZE until it reaches number of boxes required for a row
                # GAPSIZE * the x(moves a box one towards the left), by placing the left top position of the box, further away each time, as x increases
                position_y = self.myPygame.MARGIN_Y/(3/2) + (y * self.myPygame.GAPSIZE) + (y * self.myPygame.OBJECT_HEIGHT) #Gets box position horizontally
                box_dimensions = pygame.Rect((position_x, position_y),(self.myPygame.OBJECT_WIDTH, self.myPygame.OBJECT_HEIGHT))# gets all  the dimensions and position of box
                pygame.draw.rect(self.myPygame.SCREEN, self.color.WHITE, box_dimensions, 2)  # Makes box outlines white
                boxes_position.append((position_x, position_y))  # keeps adding/stores position of each box on current row TO BOXES POSITION LIST
            self.myPygame.rects.append(boxes_position) #gets all boxes position on screen & draws them on screen

        wordhint_surface= self.myPygame.font.render("WORD HINT", True, self.color.WHITE)
        wordhint_x_position = self.myPygame.MARGIN_X + 150 # CENTERS THE THEME_SURFACE
        wordhint_y_position = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2) - 120  # position of object (horizontally)
        self.myPygame.SCREEN.blit(wordhint_surface, (wordhint_x_position, wordhint_y_position))
        
        num_guess_surface= self.myPygame.font.render("Level : " + str(self.level), True, self.color.BLUE)
        wordhint_x_position = self.myPygame.MARGIN_X - 90 # CENTERS THE THEME_SURFACE
        wordhint_y_position = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2) - 130  # position of object (horizontally)
        self.myPygame.SCREEN.blit(num_guess_surface, (wordhint_x_position, wordhint_y_position))
        
        num_guess_surface= self.myPygame.font.render("Guess : " + str(5 - self.myGame.num_of_guesses), True, self.color.BLUE)
        wordhint_x_position = self.myPygame.MARGIN_X - 90 # CENTERS THE THEME_SURFACE
        wordhint_y_position = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2) - 40  # position of object (horizontally)
        self.myPygame.SCREEN.blit(num_guess_surface, (wordhint_x_position, wordhint_y_position))
        
        score_surface= self.myPygame.font.render("Score : " + str(self.score), True, self.color.BLUE)
        wordhint_x_position = self.myPygame.MARGIN_X + 480 # CENTERS THE THEME_SURFACE
        wordhint_y_position = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2) - 40  # position of object (horizontally)
        self.myPygame.SCREEN.blit(score_surface, (wordhint_x_position, wordhint_y_position))
        
        score_surface= self.myPygame.text_spell.render("Hint : " + str(self.myGame.file_select), True, self.color.BLUE)
        wordhint_x_position = self.myPygame.MARGIN_X + 450 # CENTERS THE THEME_SURFACE
        wordhint_y_position = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2) - 100  # position of object (horizontally)
        self.myPygame.SCREEN.blit(score_surface, (wordhint_x_position, wordhint_y_position))
        
        #GAPSIZE is the space inside the box for the letter
        KEY_SIZE =45
        #LKEY = KEY_SIZE*2 + self.myPygame.GAPSIZE # width for the Enter key: LARGE KEY
        KEY_MARGIN_X = self.myPygame.MARGIN_X  + (self.myPygame.SPACE*2)# KEYPAD_X: where start drawing keypad on x-axis(left or right)
        KEY_MARGIN_Y = self.myPygame.MARGIN_Y + (self.myPygame.SPACE* 15) #KEY_PAD: # How high up or down keyboard keypad is displayed
        letters = [] #letter key pressed
        KEY_CHARS = ["Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","Z","X","C","V","B","N","M","<<","Enter"]

    #KEYBOARD
        for i in range(28): #28 letters on keypad in total
            if i == 27:  # if enter backspace is pressed
                x = letters[26][0] + KEY_SIZE + (self.myPygame.GAPSIZE* 6)
                #goes back a letter in the guess_Word
                # (characters entered in guess word so far, - 1): goes back by by 1 letter
                #gapsize is the space between keys
            else:
                x = KEY_MARGIN_X + self.myPygame.GAPSIZE + ((KEY_SIZE + self.myPygame.GAPSIZE) * (i % 9.5))
                # i%9.5 :  keyboard layout
                # (10 keys on top, 9 keys in middle, 7 letter keys
                # and a backspace and 2 size enter key on the bottom)
            y = KEY_MARGIN_Y + ((i // 9.5) * (KEY_SIZE + self.myPygame.GAPSIZE))
            
            if self.myGame.used_words:
                for word in self.myGame.used_words:
                    if KEY_CHARS[i] in word:
                        if KEY_CHARS[i].lower() in self.myGame.answer_word:
                            if KEY_CHARS[i] not in self.myGame.correct_letter:
                                self.myGame.correct_letter.append(KEY_CHARS[i])
                        else:
                            if KEY_CHARS[i] not in self.myGame.incorrect_letter:
                                self.myGame.incorrect_letter.append(KEY_CHARS[i])
            
            if KEY_CHARS[i] in self.myGame.correct_letter:
                self.color_letter = self.color.COLOR_CORRECT
            elif KEY_CHARS[i] in self.myGame.incorrect_letter:
                self.color_letter = self.color.COLOUR_INCORRECT
            else:
                self.color_letter = self.color.GREY
            
            letters.append([x, y, KEY_CHARS[i], self.color_letter]) #Stores the letters position, text message, colour
    #DRAW KEYBOARD
        for i, letter_key in enumerate(letters):
            x, y, ltr, colour =  letter_key
                # draw enter key with larger width
            if i == 27:
                width = KEY_SIZE*2
                height = KEY_SIZE
            else:
                width = KEY_SIZE
                height = KEY_SIZE
            key = pygame.Rect(x - (width / 2), y - (height / 2), width, height) #MIDDLE
            #KEY_SIZE = HAS THE SAME  WIDTH, HEIGHT  DIMENSIONS
            pygame.draw.rect(self.myPygame.SCREEN, colour, key, border_radius=5) #draws box keys ontop screen
                #border radius is : how curved the box edges are on keyboard
            letter_key= self.myPygame.text.render(ltr, 1, (self.color.DARK_GREY if colour == self.color.COLOUR_INCORRECT else self.color.WHITE))  # draw black text on LIGHT_GRAY background else white text
            self.myPygame.SCREEN.blit(letter_key, (x - letter_key.get_width() / 2, y - letter_key.get_height() / 2))
        
        # Alerts player that word is not in wordlist. Text appears for 2 seconds.
        if self.myGame.get_flag_WORD_INVALID():
            self.myGame.set_timer_flag_2(0)
            self.myGame.set_flag_NOT_ENOUGH_LETTERS(False)
            text_surface = self.myPygame.text.render("Not in word list", True,self.color.RED)

            #POSITION OF NOT ENOUGH LETTERS ON SCREEN
            position_x = self.myPygame.MARGIN_X + 180   # position of text_Surface/TITLE (vertically)
            position_y = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2) - 75  # position of object (horizontally)
            self.myPygame.SCREEN.blit(text_surface, (position_x, position_y))
            self.myGame.set_timer_flag_1(self.myGame.get_timer_flag_1() + 1)

        if self.myGame.get_flag_NOT_ENOUGH_LETTERS():
            self.myGame.set_timer_flag_1(0)
            self.myGame.set_flag_WORD_INVALID(False)
            text_surface = self.myPygame.text.render("Not enough letters", True, self.color.RED)
            position_x = self.myPygame.MARGIN_X + 180   # position of text_Surface/TITLE (vertically)
            position_y = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2) - 75  # position of object (horizontally)
            self.myPygame.SCREEN.blit(text_surface, (position_x, position_y))
            self.myGame.set_timer_flag_2(self.myGame.get_timer_flag_2() + 1)

        if self.myGame.get_timer_flag_1() == self.myPygame.FPS:
            self.myGame.set_flag_WORD_INVALID(False)
            self.myGame.set_timer_flag_1(0)

        if self.myGame.get_timer_flag_2() == self.myPygame.FPS:
            self.myGame.set_flag_NOT_ENOUGH_LETTERS(False)
            self.myGame.set_timer_flag_2(0)
        
        #Get time
        times = datetime.datetime.now().replace(microsecond=0)
        self.manage_time(times)
        
        if self.myGame.get_flag_WIN():
            if self.test == 0:
                self.score += self.myGame.update_score()
                self.times_list.append(str(self.delta_minute) + ":" + str(self.delta_second))
                self.win += 1
                self.level = self.update_level()
                self.test = 1
                
            text_surface = self.myPygame.text.render("Correct! Press 'R' to continue", True, self.color.WHITE)
            position_x = self.myPygame.MARGIN_X - (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS / 5))
            position_y = self.myPygame.MARGIN_Y  + (self.myPygame.OBJECT_HEIGHT * self.myPygame.ROWS) - 10
            self.myPygame.SCREEN.blit(text_surface, (position_x, position_y))
            
        if self.myGame.get_flag_LOSE():
            if self.score == 0:
                #HELP: Better luck next time! The answer word was,", answer_word
                text_surface = self.myPygame.text.render("The Answer was : *" + self.myGame.answer_word.upper() + "* Press 'R' to try again", True, self.color.WHITE)
                position_x = self.myPygame.MARGIN_X - (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS / 5))
                position_y = self.myPygame.MARGIN_Y  + (self.myPygame.OBJECT_HEIGHT * self.myPygame.ROWS) - 10
                self.myPygame.SCREEN.blit(text_surface, (position_x, position_y))
            else :
                self.myGame.set_timer_flag_2(self.myGame.get_timer_flag_2() + 1)
                #HELP: Better luck next time! The answer word was,", answer_word
                text_surface = self.myPygame.text.render("The Answer was : *" + self.myGame.answer_word.upper(), True, self.color.WHITE)
                position_x = self.myPygame.MARGIN_X - (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS / 5))
                position_y = self.myPygame.MARGIN_Y + (self.myPygame.OBJECT_HEIGHT * self.myPygame.ROWS) - 10
                self.myPygame.SCREEN.blit(text_surface, (position_x, position_y))
                self.myGame.set_timer_flag_1(0)
                
                if self.myGame.get_timer_flag_2() == self.myPygame.FPS:
                    self.connector.set_leaderbord(self.username, str(self.score), min(self.times_list))
                    self.leaderbord.play()
        
        
        
        # Blits each letter_position of the current word the user is currently typing.
        # Firstly renders  letter_position, then blits it on the appropriate rectangle according to which letter_position it is.
        if self.myGame.guess_word:
            for letter_position in range(len(self.myGame.guess_word)):
                word_surface = self.myPygame.text.render(self.myGame.guess_word[letter_position], True, self.color.WHITE)
                # [0] represents X coord, [1] Y.
                self.myPygame.SCREEN.blit(word_surface, (self.myPygame.rects[self.myGame.num_of_guesses][letter_position][0] + self.myPygame.GAPSIZE,self.myPygame.rects[self.myGame.num_of_guesses][letter_position][1] + self.myPygame.GAPSIZE))
        
        # Renders letters and rects of words already inputted by player.
        if self.myGame.used_words:
            
            for word_index in range(len(self.myGame.used_words)):
                remaining_letters = list(self.myGame.answer_word)
                num_correct = 0

                # Used to make sure that letters that appear more than once don't get counted if that letter_position appears in answer_word only once.
                # EG: answer_word = "proxy", word = "droop", and 'o' appears more than once. The second 'o' in droop does not get counted.

                same_letter_position = [i for i, x in enumerate(zip(self.myGame.answer_word, self.myGame.used_words[word_index].lower())) if all(y == x[0] for y in x)] #same letter = same indecies
                # Same indeces e.g.  if answerword is "beast" and guessword[word_index] is "toast", same letter poition/indeces collide@: in this case, "a","s","t" - which have indeces of [2,3,4] respectively.
                if same_letter_position:
                    for index in range(len(same_letter_position)): #index position
                        num_correct = num_correct + 1
                        remaining_letters[same_letter_position[index]] = ""
                        box_dimensions = pygame.Rect((self.myPygame.rects[word_index][same_letter_position[index]][0], self.myPygame.rects[word_index][same_letter_position[index]][1]),(self.myPygame.OBJECT_WIDTH, self.myPygame.OBJECT_HEIGHT))
                        pygame.draw.rect(self.myPygame.SCREEN, self.color.COLOR_CORRECT, box_dimensions)
                        past_letter_surface = self.myPygame.text.render(self.myGame.used_words[word_index][same_letter_position[index]].upper(), True, self.color.WHITE)
                        self.myPygame.SCREEN.blit(past_letter_surface, (self.myPygame.rects[word_index][same_letter_position[index]][0] + self.myPygame.GAPSIZE,self.myPygame.rects[word_index][same_letter_position[index]][1] + self.myPygame.GAPSIZE))

                for letter_position in range(self.myGame.WORD_LENGTH):
                    if letter_position not in same_letter_position: #same letter position
                        box_dimensions = pygame.Rect((self.myPygame.rects[word_index][letter_position][0], self.myPygame.rects[word_index][letter_position][1]),(self.myPygame.OBJECT_WIDTH, self.myPygame.OBJECT_HEIGHT))
                        cur_past_letter = self.myGame.used_words[word_index][letter_position].lower()
                        past_letter_surface = self.myPygame.text.render(cur_past_letter.upper(), True, self.color.WHITE)
                        # Incorrect Letters
                        if cur_past_letter not in remaining_letters:
                            pygame.draw.rect(self.myPygame.SCREEN, self.color.COLOUR_INCORRECT, box_dimensions)
                        # Letter exists in word, but wrong position.
                        else:
                            pygame.draw.rect(self.myPygame.SCREEN, self.color.COLOR_MISPLACED, box_dimensions)
                            remaining_letters[remaining_letters.index(cur_past_letter)] = ""
                        self.myPygame.SCREEN.blit(past_letter_surface, (self.myPygame.rects[word_index][letter_position][0] + self.myPygame.GAPSIZE, self.myPygame.rects[word_index][letter_position][1] + self.myPygame.GAPSIZE))

                # Win/lose condition
                if num_correct == 5:
                    self.myGame.set_flag_WIN (True)
                    self.myGame.set_flag_LOSE (False)
                elif  num_correct != 5 and len(self.myGame.used_words) == self.myPygame.ROWS:
                    self.myGame.set_flag_LOSE (True)
                    self.myGame.set_flag_WIN (False)

        self.myPygame.update_pygame()
    
    def manage_time(self, times):
        
        self.end = times
        self.delta_minute = self.end.minute - self.myGame.start.minute
        self.delta_second = self.end.second - self.myGame.start.second
        
        if self.delta_minute == 4 and self.level == 1:
            self.myGame.set_flag_LOSE (True)
        if self.delta_minute == 3 and self.level == 2:
            self.myGame.set_flag_LOSE (True)
        if self.delta_minute == 2 and self.level == 3:
            self.myGame.set_flag_LOSE (True)
        
    
    
    def update_level(self):
        if self.win < 3:
            return 1
        elif self.win >= 3 and self.win < 6:
            return 2
        elif self.win >= 6 and self.win < 9:
            return 3
        elif self.win >= 9 and self.win < 12:
            return 4
        elif self.win >= 12:
            return 5
    

# if __name__ == "__main__":
#     Spellme("Nathan").start()