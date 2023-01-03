import pygame
import sys

import db 
import settings
import spellme
import sign_in

class Signup():
    def __init__(self):
        self.myPygame = settings.HandlePygame()
        self.color = settings.MyColor()
        self.user_text = ''
        self.pass_text = ''

        self.user_rect = pygame.Rect(self.myPygame.MARGIN_X + 30, (self.myPygame.MARGIN_Y )*(3/2), self.myPygame.length, self.myPygame.OBJECT_HEIGHT*2)
        self.pass_rect = pygame.Rect(self.myPygame.MARGIN_X + 30, (self.myPygame.MARGIN_Y )*(5/2), self.myPygame.length, self.myPygame.OBJECT_HEIGHT*2)

        self.user_active = False
        self.pass_active = False

        self.color_active = self.color.color_active
        self.color_passive = self.color.color_passive

        self.color_pass = self.color_passive
        self.color_user = self.color_passive
        self.error_msg = ''
        
    def screen (self):
        self.myPygame.__init__()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.user_rect.collidepoint(event.pos):
                        self.user_active = True
                    else:
                        self.user_active = False
                    
                    if self.pass_rect.collidepoint(event.pos):
                        self.pass_active = True
                    else:
                        self.pass_active = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        sign_in.Signin().screen()
                    
                    if self.user_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.signup()
                        else:
                            self.user_text += event.unicode
                    
                    if self.pass_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.pass_text = self.user_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.signup()
                        else:
                            self.pass_text += event.unicode
        
            self.myPygame.SCREEN.fill(self.color.SCREEN_COLOUR)
            
            if self.user_active:
                self.color_user = self.color_active
            else:
                self.color_user = self.color_passive
            
            if self.pass_active:
                self.color_pass = self.color_active
            else:
                self.color_pass = self.color_passive
            
            pygame.draw.rect(self.myPygame.SCREEN, self.color_user, self.user_rect, 2)  # Makes box outlines white
            self.myPygame.SCREEN.blit((self.myPygame.text.render("USERNAME",True,self.color.WHITE)),(self.user_rect.x, self.user_rect.y))
            
            pygame.draw.rect(self.myPygame.SCREEN, self.color_pass, self.pass_rect, 2)  # Makes box outlines white
            self.myPygame.SCREEN.blit((self.myPygame.text.render("PASSWORD",True,self.color.WHITE)),(self.pass_rect.x, self.pass_rect.y))
            
            
            user_surface = self.myPygame.text.render(self.user_text, True, (255,255,255))
            self.myPygame.SCREEN.blit(user_surface, (self.user_rect.x + 10, self.user_rect.y + 30))
            
            encrypt = '*' * len(self.pass_text) #hides password with *
            pass_surface = self.myPygame.text.render(encrypt, True, (255,255,255))
            self.myPygame.SCREEN.blit(pass_surface, (self.pass_rect.x + 10, self.pass_rect.y + 30))
            
            wordhint_surface= self.myPygame.text.render("SIGN UP TO PLAY", True, self.color.WHITE)
            wordhint_x_position = self.myPygame.MARGIN_X + 150 # CENTERS THE THEME_SURFACE
            wordhint_y_position = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 8)  # position of object (horizontally)
            self.myPygame.SCREEN.blit(wordhint_surface, (wordhint_x_position, wordhint_y_position))
            
            signup_surface= self.myPygame.text.render("Have an Account ?  Press SPACE to signin", True, self.color.RED)
            wordhint_x_position = self.myPygame.MARGIN_X / 2 # CENTERS THE THEME_SURFACE
            wordhint_y_position = self.myPygame.MARGIN_Y * (7/2)  # position of object (horizontally)
            self.myPygame.SCREEN.blit(signup_surface, (wordhint_x_position, wordhint_y_position))
            
            error_surface= self.myPygame.text.render(self.error_msg, True, self.color.RED)
            wordhint_x_position = self.myPygame.MARGIN_X + 50 # CENTERS THE THEME_SURFACE
            wordhint_y_position = self.myPygame.MARGIN_Y - (self.myPygame.GAPSIZE * 2)  # position of object (horizontally)
            self.myPygame.SCREEN.blit(error_surface, (wordhint_x_position, wordhint_y_position))
            
            self.myPygame.update_pygame()
        
    def signup(self):
        username = self.user_text
        password = self.pass_text
        #print(username)
        signup = db.SignUp_db(username, password)
        if signup.get_signup_state() == 'OK':
            spellme.Spellme(username).start()
        else:
            self.error_msg = signup.get_signup_state()
            #print(signup.get_signup_state())


# if __name__ == "__main__":
#     Signup().screen()