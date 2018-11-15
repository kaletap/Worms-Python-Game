import pygame

from defaults import *

class TextObject(pygame.sprite.Sprite):
    """Simple class to represent a text object displayed in Menu"""
    def __init__(self, text, x, y, font=None, font_size=25, bold=False):
        super().__init__()

        self.text = text
        self.x = x
        self.y = y

        # We don't want to open this SysFont too many times
        # it's better to pass it as an argument than create each time
        self.font = font or pygame.font.SysFont('Calibri', font_size, bold, False)

        self.image = self.font.render(text, True, GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_text(self, new_text):
        """Changes text in displayed image"""
        self.image = self.font.render(new_text, True, GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Menu:
    """Class responsible for the look of the Menu on the right"""
    def __init__(self, x=SCREEN_WIDTH + 20, y=20):
        # x and y are starting points of menu
        self.x = x
        self.y = y

        # Options
        self.language = EN 
        self.sound = ON
        self.time = 10

        self.font = pygame.font.SysFont('Calibri', 25, False, False)
        self.font_bold = pygame.font.SysFont('Calibri', 25, True, False)

        self.positions = {
            "menu": (x, y+10),

            "language" : (x, y + 50),
            "language_option" : (x + 100, y + 50),

            "sound" : (x, y + 100),
            "sound_option" : (x + 100, y + 100),

            "time" : (x, SCREEN_HEIGHT - 50),
            "time_display" : (x + 100, SCREEN_HEIGHT - 50)
        }

        self.text_objects = {
            "menu": TextObject("MENU", *self.positions["menu"]),

            "language" : TextObject("Language:", *self.positions["language"], self.font),
            "language_option" : TextObject(self.language, *self.positions["language_option"], self.font),

            "sound" : TextObject("Sound:", *self.positions["sound"], self.font),
            "sound_option" : TextObject(self.sound, *self.positions["sound_option"], self.font),

            "time" : TextObject("TIME:", *self.positions["time"], font=self.font_bold),
            "time_display": TextObject(str(0), *self.positions["time_display"], self.font)
        }

    def update_options(self, x, y):
        if self.text_objects["language_option"].rect.collidepoint(x, y):
            #print("Changing language option")
            new_language_option = EN if self.language == PL else PL
            self.language = new_language_option
            self.text_objects["language_option"] = TextObject(new_language_option, 
                                                              *self.positions["language_option"], 
                                                              self.font)
            if self.language == PL:
                self.text_objects["time"].change_text("CZAS:")
                self.text_objects["language"].change_text("Jezyk:")
                self.text_objects["sound"].change_text("Dzwiek:")

            elif self.language == EN:
                self.text_objects["time"].change_text("TIME:")
                self.text_objects["language"].change_text("Language:")
                self.text_objects["sound"].change_text("Sound:")

        elif self.text_objects["sound_option"].rect.collidepoint(x, y):
            #print("Changing sound option")
            new_sound_option = OFF if self.sound == ON else ON
            self.sound = new_sound_option
            self.text_objects["sound_option"] = TextObject(new_sound_option, 
                                                          *self.positions["sound_option"],
                                                          self.font)

    def update_time(self, seconds, font=None):
        self.time = seconds
        self.text_objects["time_display"] = TextObject(str(seconds), 
                                                        *self.positions["time_display"], 
                                                        font=self.font)