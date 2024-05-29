# Import necessary modules and classes
import sys
import pygame
from button import Button
from player import Player
from scripts.util import get_font, load_image, quit_game
from sfx import SFXController
from ui.ui import UIComponent

# Implementation of Game Option as a UIComponent
class UIGame(UIComponent):
    # Constructor to initialize the UIGame object
    def __init__(self, game):
        # Initialize the game object
        self.game = game
        
        # Get the screen object from the game
        self.screen = self.game.get_screen()
        
        # Set the font for UI elements
        self.font = get_font(36)
        
        # Load the background image for the game and scale it
        self.background_img = pygame.transform.scale(load_image('backgroundgame.jpg', is_color_key=False), (1280, 720))
        
        # Initialize button for UI interaction
        self.home_btn = Button(520, 520, load_image('back.png', convert_alpha=True), 0.3)
        
        # Set the background color
        self.bg_color = (144, 201, 120)
        
        # Get the sound effects controller from the game
        self.sfx_controller: SFXController = self.game.get_sfxcontroller()

    # Method to render the UI components during gameplay
    def render(self, player1, player2):
        # Reset the game state
        self.game.reset_game()

        # Set player 1 and player 2 objects
        self.player1: Player = player1
        self.player2: Player = player2

        # Apply images to player objects
        self.player1.apply_image()
        self.player2.apply_image()

        # Perform countdown before starting the game
        self.countdown(3)

        # Set the game to active state
        self.is_active = True

        # Initialize variable for victory sounds
        victory_sounds = False

        # Main game loop
        while self.is_active:
            # Start timer for players if not already started
            if not self.player1.get_distance_traveled() and not self.player2.get_distance_traveled():        
                self.player1.start_timer()
                self.player2.start_timer()  

            # Move players if the game is not stopped
            if not self.game.is_game_stop():
                self.player1.move()
                self.player2.move()        

            # Ensure players' positions loop around the screen
            if self.player1.rect.right >= self.screen.get_width() + 270:
                self.player1.rect.left = -self.player1.rect.width
            if self.player2.rect.right >= self.screen.get_width() + 270:
                self.player2.rect.left = -self.player2.rect.width

            # Move background based on players' speed
            if not self.game.is_game_stop():
                current_max_speed = max(self.player1.get_speed(), self.player2.get_speed())
                current_background_img_x = self.game.get_background_img_x() - current_max_speed

                self.game.set_background_img_x(current_background_img_x)

                # Reset background position when it reaches the end
                if current_background_img_x <= -self.screen.get_width():
                    self.game.set_background_img_x(0)   

            # Draw game elements
            self.draw_bg()
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.draw_player_text()
            self.draw_distance(self.player1.get_distance_traveled(), 1)
            self.draw_distance(self.player2.get_distance_traveled(), 2)

            # Check for winner and display victory message
            winner = self.check_winner()
            if winner:
                font = get_font(36)
                text = font.render(winner, True, (255, 255, 255))
                self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
                self.home_btn.draw(self.screen)

                # Display time taken if there is a winner
                if winner is not None:
                    if winner == "Player 1":
                        if not self.game.win:
                            self.time_taken = self.player2.stop_timer()
                            self.game.win = True
                        self.time_taken = self.player1.stop_timer()
                    else:
                        if not self.game.win:
                            self.time_taken = self.player2.stop_timer()
                            self.game.win = True
                        self.time_text = f"Time taken: {self.time_taken:.2f} seconds"

                # Render and display time taken text
                text = font.render(self.time_text, True, (0, 0, 0))
                self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 + text.get_height() // 2))
                
                # Control music and sound effects during victory
                pygame.mixer.music.set_volume(0)
                self.sfx_controller.stop('engine')
                if not victory_sounds:
                    self.sfx_controller.stop('background')
                    self.sfx_controller.play('speak')
                    self.sfx_controller.play('victory')
                    victory_sounds = True

            # Handle user events
            self.handle_event()

            # Update display and control FPS
            pygame.display.update()
            self.game.clock.tick(self.game.FPS)

    # Method to check for winner
    def check_winner(self):
        if self.player1.get_distance_traveled() >= 2000:
            self.game.game_stop = True
            return "Player 1 WIN!"
        elif self.player2.get_distance_traveled() >= 2000:
            self.game.game_stop = True
            return "Player 2 WIN!"
        return None

    # Method to toggle music on/off
    def toggle_music(self):
        if self.music_muted:
            pygame.mixer.music.set_volume(0.5)
        else:
            pygame.mixer.music.set_volume(0) 
        self.music_muted = not self.music_muted 

    # Method to draw background
    def draw_bg(self):
        background_img_x = self.game.get_background_img_x()
        self.screen.fill(self.bg_color)
        self.screen.blit(self.background_img, (background_img_x, 0))
        self.screen.blit(self.background_img, (background_img_x + self.screen.get_width(), 0))

    # Method to draw distance traveled by players
    def draw_distance(self, distance, player):
        font = get_font(24)
        if player == 1:
            text = font.render(f'Distance Player 1: {distance:.2f} meters', True, (0, 0, 0))
            text_rect = text.get_rect(midtop=(self.screen.get_width() // 4, 10))
        else:
            text = font.render(f'Distance Player 2: {distance:.2f} meters', True, (0, 0, 0))
            text_rect = text.get_rect(midtop=(3 * self.screen.get_width() // 4, 10))
        self.screen.blit(text, text_rect)

    # Method to draw player names
    def draw_player_text(self):
        font = get_font(24)
        player1_text = font.render('Player 1', True, (255, 255, 255))
        player1_text_rect = player1_text.get_rect(midtop=self.player1.rect.midtop)
        self.screen.blit(player1_text, player1_text_rect)

        player2_text = font.render('Player 2', True, (255, 255, 255))
        player2_text_rect = player2_text.get_rect(midtop=self.player2.rect.midtop)
        self.screen.blit(player2_text, player2_text_rect)

    # Method to perform countdown before the game starts
    def countdown(self, time):
        countdown = time

        while countdown > 0:
            self.sfx_controller.play('countdown')
            self.screen.fill((0, 0, 0))  
            font = get_font(100)
            text = font.render(str(countdown), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()  
            pygame.time.wait(1000)  
            countdown -= 1
        
        self.sfx_controller.play('go')

    # Method to handle user events during the game
    def handle_event(self):
        sound_stop = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.home_btn.is_clicked():
                    self.sfx_controller.stop('victory')
                    self.sfx_controller.play('background')
                    self.is_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.sfx_controller.stop('engine')
                    self.sfx_controller.stop('victory')
                    self.sfx_controller.stop('speak')
                    self.is_active = False
                if event.key == pygame.K_UP:
                    self.player1.accelerate()
                    if not sound_stop:
                        self.sfx_controller.play('engine')
                        sound_stop = True
                if event.key == pygame.K_w:
                    self.player2.accelerate()
                    if not sound_stop:
                        self.sfx_controller.play('engine')
                        sound_stop = True
                if event.key == pygame.K_x:
                    self.sfx_controller.set_volume('background', 0)
                if event.key == pygame.K_z:
                    self.sfx_controller.set_volume('background', 0.5)        
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
