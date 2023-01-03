import pygame
import sys
import settings
import db
import spellme


class Leaderbord():
    def __init__(self, username):
        self.myPygame = settings.HandlePygame()
        self.color = settings.MyColor()
        self.connector = db.Connector("leaderbord.txt")
        
        self.leader = self.connector.get_username()
        self.score = self.connector.get_score()
        self.times = self.connector.get_time()
        
        [self.leader, self.score, self.times] = self.sort()
        self.username = username
        
    def screen (self):
        # ----------------
        # SCREENBOARD:
        # ----------------
        self.myPygame.SCREEN.fill(self.color.SCREEN_COLOUR)
        #draw_title(font) # draw title font

        #--------------------------------
        # RECT:GET BOX POSITIONS ON SCREEN
        #---------------------------------
        text_surface_rank = self.myPygame.text.render("Rank", True, self.color.RED)
        text_surface_leader = self.myPygame.text.render("Name", True, self.color.RED)
        text_surface_score = self.myPygame.text.render("Score", True, self.color.RED)
        text_surface_time = self.myPygame.text.render("Time", True, self.color.RED)
        
        position_x_rank = self.myPygame.MARGIN_X
        position_x_score = self.myPygame.MARGIN_X*2.5 + (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS))
        position_x_leader = self.myPygame.MARGIN_X/2 + (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS))
        position_x_time = self.myPygame.MARGIN_X*4 + (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS))
        
        position_y = position_y = self.myPygame.MARGIN_Y
        
        self.myPygame.SCREEN.blit(text_surface_time, (position_x_time, position_y))
        self.myPygame.SCREEN.blit(text_surface_rank, (position_x_rank, position_y))
        self.myPygame.SCREEN.blit(text_surface_leader, (position_x_leader, position_y))
        self.myPygame.SCREEN.blit(text_surface_score, (position_x_score, position_y))
        
        for i in range(len(self.score)):
            text_surface_rank = self.myPygame.text.render(str(i+1), True, self.color.RED)
            text_surface_leader = self.myPygame.text.render(self.leader[i], True, self.color.RED)
            text_surface_score = self.myPygame.text.render(self.score[i], True, self.color.RED)
            text_surface_time = self.myPygame.text.render(self.times[i], True, self.color.RED)
            
            # position_x_rank = self.myPygame.MARGIN_X
            # position_x_score = self.myPygame.MARGIN_X*2.5 + (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS))
            # position_x_leader = self.myPygame.MARGIN_X/2 + (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS))
            
            position_y = position_y = self.myPygame.MARGIN_Y*(3/2) + (i * self.myPygame.GAPSIZE) + (i * self.myPygame.OBJECT_HEIGHT)
            
            self.myPygame.SCREEN.blit(text_surface_rank, (position_x_rank, position_y))
            self.myPygame.SCREEN.blit(text_surface_leader, (position_x_leader, position_y))
            self.myPygame.SCREEN.blit(text_surface_score, (position_x_score, position_y))
            self.myPygame.SCREEN.blit(text_surface_time, (position_x_time, position_y))
            
        text_surface = self.myPygame.text.render("Press 'R' to play again", True, self.color.WHITE)
        position_x = self.myPygame.MARGIN_X - (self.myPygame.OBJECT_WIDTH * (self.myPygame.COLUMNS / 5))
        position_y = self.myPygame.MARGIN_Y*(7/4) + (self.myPygame.GAPSIZE * 7) + (self.myPygame.OBJECT_HEIGHT * self.myPygame.ROWS)
        self.myPygame.SCREEN.blit(text_surface, (position_x, position_y))
        
        leaderbord_surface= self.myPygame.text.render("LEADERBORD", True, self.color.RED)
        leaderbord_x_position = self.myPygame.MARGIN_X + 110 # CENTERS THE THEME_SURFACE
        leaderbord_y_position = self.myPygame.MARGIN_Y - 60  # position of object (horizontally)
        self.myPygame.SCREEN.blit(leaderbord_surface, (leaderbord_x_position, leaderbord_y_position))
        
        self.myPygame.update_pygame()
        
    def play(self):
        while True:
            for event in pygame.event.get(): #get entered keys
                #QUIT IF THEY EXIT: # if type of event corresponds to quit then quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        spellme.Spellme(self.username).start()  # GO BACK TO MAIN GAME
            
            Leaderbord(self.username).screen()
    
    def sort(self):
        for i in range(len(self.score)):
            a = int(self.score[i])
            for j in range(i+1,len(self.score)):
                b = int(self.score[j])
                if b>a:
                    a= b
                    self.score[i], self.score[j] = self.score[j], self.score[i]
                    self.leader[i], self.leader[j] = self.leader[j], self.leader[i]
                    self.times[i], self.times[j] = self.times[j], self.times[i]
        
        for i in range(3):
            a = int(self.score[i])
            c = self.times[i]
            for j in range(i+1,3):
                b = int(self.score[j])
                d = self.times[j]
                if b==a:
                    if c>d:
                        self.score[i], self.score[j] = self.score[j], self.score[i]
                        self.leader[i], self.leader[j] = self.leader[j], self.leader[i]
                        self.times[i], self.times[j] = self.times[j], self.times[i]
        
        return [self.leader[:3], self.score[:3], self.times[:3]]

# if __name__ == "__main__":
#     Leaderbord("Nathan").play()