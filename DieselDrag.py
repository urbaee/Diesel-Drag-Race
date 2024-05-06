import pygame
from abc import ABC, abstractmethod
from button import Button
import time

class GameObject(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def accelerate(self):
        pass

    @abstractmethod
    def start_timer(self):
        pass

    @abstractmethod
    def stop_timer(self):
        pass

class Sprite(GameObject):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None

    def draw(self, screen):
        if self.image and self.rect:
            screen.blit(self.image, self.rect)

class Player(Sprite):
    def __init__(self, char_type, x, y, scale, initial_speed, max_speed, acceleration_rate, screen_width, screen_height):
        super().__init__()
        self.__char_type = char_type
        self.__speed = initial_speed
        self.__max_speed = max_speed
        self.__acceleration_rate = acceleration_rate
        img = pygame.image.load(f'img/{self.__char_type}/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.__distance_traveled = 0
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__start_time = None

    def set_speed(self, speed):
        self.__speed = speed

    def get_speed(self):
        return self.__speed
    
    def set_max_speed(self, max_speed):
        self.__max_speed = max_speed

    def get_max_speed(self):
        return self.__max_speed

    def set_acceleration_rate(self, acceleration_rate):
        self.__acceleration_rate = acceleration_rate

    def get_acceleration_rate(self):
        return self.__acceleration_rate       

    def move(self):
        self.rect.x += self.__speed
        self.__distance_traveled += abs(self.__speed) / self.__screen_width * self.__screen_height

    def accelerate(self):
        if self.__speed < self.__max_speed:
            self.__speed += self.__acceleration_rate

    def get_distance_traveled(self):
        return self.__distance_traveled

    def start_timer(self):
        self.__start_time = time.time()

    def stop_timer(self):
        end_time = time.time()
        return end_time - self.__start_time

    def update(self):
        self.move()
        self.accelerate()

class Game:
    def __init__(self, screen_width=1280, screen_height=720):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('audio/ROTS.mp3')
        pygame.mixer.music.play(-1, 3)
        pygame.mixer.music.set_volume(0.5)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('DIESEL DRAG RACE')
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.bg_color = (144, 201, 120)
        self.font_size = 24
        self.background_img = pygame.image.load('img/backgroundgame2.jpg').convert()
        self.background_img2 = pygame.image.load('images/bgfortuner3.png').convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.screen_width, self.screen_height))
        self.background_img_x = 0
        self.PIXELS_PER_METER = 100
        self.player1 = Player('player', 100, 600, 0.35, 0, 100, 0.5, self.screen_width, self.screen_height)
        self.player2 = Player('enemy', 100, 400, 0.35, 0, 100, 0.5, self.screen_width, self.screen_height)
        self.music_muted = False
        self.engine_sound = pygame.mixer.Sound('audio/fortuner.wav')

        start_button_image = pygame.image.load('images/start.png')
        self.start_button = Button(850, 125, start_button_image, 0.4)

        rules_button_image = pygame.image.load('images/help.png')
        self.rules_button = Button(850, 325, rules_button_image, 0.4)
        
        music_button_image = pygame.image.load('images/music.png')
        self.music_button = Button(50, 50, music_button_image, 0.2)

        back_button_image = pygame.image.load('images/back.png')
        self.back_button = Button(50, 130, back_button_image, 0.2)

        home_button_image = pygame.image.load('images/back.png')
        self.home_button = Button(540, 520, home_button_image, 0.3)

        self.countdown = 3  
        self.show_rules = False
        self.rules_text = [
            "How to play :",
            "1. Player 1 menekan / spam tombol 'UP' untuk mempercepat.",
            "2. Player 2 menekan / spam tombol 'W' untuk mempercepat.",
            "3. Jika salah satu pemain mencapai jarak 2000 meter, pemain tersebut menang.",
            "4. Tekan tombol 'ESC' untuk keluar dari game."
        ]

    def draw_bg(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.background_img, (self.background_img_x, 0))
        self.screen.blit(self.background_img, (self.background_img_x + self.screen_width, 0))

    def draw_distance(self, distance, player):
        font = pygame.font.Font("textfont/Minecraft.ttf", self.font_size)
        if player == 1:
            text = font.render(f'Distance Player 1: {distance:.2f} meters', True, (0, 0, 0))
            text_rect = text.get_rect(midtop=(self.screen_width // 4, 10))
        else:
            text = font.render(f'Distance Player 2: {distance:.2f} meters', True, (0, 0, 0))
            text_rect = text.get_rect(midtop=(3 * self.screen_width // 4, 10))
        self.screen.blit(text, text_rect)

    def draw_player_text(self):
        font = pygame.font.Font('textfont/Minecraft.ttf', self.font_size)
        player1_text = font.render('Player 1', True, (255, 255, 255))
        player1_text_rect = player1_text.get_rect(midtop=self.player1.rect.midtop)
        self.screen.blit(player1_text, player1_text_rect)

        player2_text = font.render('Player 2', True, (255, 255, 255))
        player2_text_rect = player2_text.get_rect(midtop=self.player2.rect.midtop)
        self.screen.blit(player2_text, player2_text_rect)

    def check_winner(self):
        if self.player1.get_distance_traveled() >= 2000:
            return "Player 1 WIN!"
        elif self.player2.get_distance_traveled() >= 2000:
            return "Player 2 WIN!"
        return None

    def toggle_music(self):
        if self.music_muted:
            pygame.mixer.music.set_volume(0.5)
        else:
            pygame.mixer.music.set_volume(0) 
        self.music_muted = not self.music_muted 

    def run(self):
        try:
            start_game = False
            run = True

            while run:
                self.clock.tick(self.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                            start_game = True
                        elif self.rules_button.rect.collidepoint(pygame.mouse.get_pos()):
                            self.show_rules = not self.show_rules
                        elif self.music_button.rect.collidepoint(pygame.mouse.get_pos()):
                            self.toggle_music()   
                        elif self.home_button.rect.collidepoint(pygame.mouse.get_pos()):
                            self.run()       

                if start_game:
                    if self.countdown > 0:
                        self.screen.fill((0, 0, 0))  
                        font = pygame.font.Font("textfont/Minecraft.ttf", 100)
                        text = font.render(str(self.countdown), True, (255, 255, 255))
                        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                        self.screen.blit(text, text_rect)
                        pygame.display.flip()  
                        pygame.time.wait(1000)  
                        self.countdown -= 1
                    else:
                        if not self.player1.get_distance_traveled() and not self.player2.get_distance_traveled():        
                            self.player1.start_timer()
                            self.player2.start_timer()  
                        elif self.player1.get_speed() > 0 or self.player2.get_speed():
                            self.engine_sound.play()
                            self.engine_sound.set_volume(0.3)

                        self.clock.tick(self.FPS)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    run = False
                                elif event.key == pygame.K_UP:
                                    self.player1.accelerate()
                                elif event.key == pygame.K_w:
                                    self.player2.accelerate()
                                elif event.key == pygame.K_x:
                                    pygame.mixer.music.set_volume(0)  
                                elif event.key == pygame.K_z:
                                    pygame.mixer.music.set_volume(0.5)          

                        self.player1.move()
                        self.player2.move()

                        if self.player1.rect.right >= self.screen_width + 270:
                            self.player1.rect.left = -self.player1.rect.width
                        if self.player2.rect.right >= self.screen_width + 270:
                            self.player2.rect.left = -self.player2.rect.width

                        self.background_img_x -= self.player1.get_speed()
                        if self.background_img_x <= -self.screen_width:
                            self.background_img_x = 0

                        self.draw_bg()
                        self.player1.draw(self.screen)
                        self.player2.draw(self.screen)
                        self.draw_player_text()
                        self.draw_distance(self.player1.get_distance_traveled(), 1)
                        self.draw_distance(self.player2.get_distance_traveled(), 2)

                        winner = self.check_winner()

                        if winner:
                            font = pygame.font.Font("textfont/Minecraft.ttf", 36)
                            text = font.render(winner, True, (255, 255, 255))
                            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - text.get_height() // 2))
                            
                            self.home_button.draw(self.screen)

                            if winner == "Player 1":
                                time_taken = self.player1.stop_timer()
                            else:
                                time_taken = self.player2.stop_timer()
                            time_text = f"Time taken: {time_taken:.2f} seconds"
                            text = font.render(time_text, True, (0, 0, 0))
                            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 + text.get_height() // 2))

                            self.start_time = None
                            
                            self.engine_sound.stop()
                            pygame.display.update()
                            pygame.time.delay(1000)

                else:
                    self.screen.fill(self.bg_color)
                    self.screen.blit(self.background_img2, (0, 0))
                    self.start_button.draw(self.screen)
                    self.rules_button.draw(self.screen)
                    self.music_button.draw(self.screen)

                    if self.show_rules:
                        self.screen.fill((0,0,0))
                        self.back_button.draw(self.screen)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if self.back_button.rect.collidepoint(pygame.mouse.get_pos()):
                                     self.show_rules = False
                        font = pygame.font.Font("textfont/Minecraft.ttf", 24)
                        for i, text in enumerate(self.rules_text):
                            rules_text = font.render(text, True, (255, 255, 255))
                            text_rect = rules_text.get_rect(center=(630, 300 + i * 30))
                            self.screen.blit(rules_text, text_rect)

                pygame.display.update()

            pygame.quit()

        except Exception as e:
            print("An error occurred:", str(e))

if __name__ == "__main__":
    game = Game()
    game.run()
