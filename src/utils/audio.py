import pygame

from models.assets.index import Assets


class Sounds:
      """
      A class to handle sound effects and background music using pygame's mixer module.
      """
      def __init__(self):
            """
            Initializes the Sound class and sets up the mixer.
            """
            pygame.mixer.init()
            self.background_channel = pygame.mixer.Channel(0)
            self.effect_channel = pygame.mixer.Channel(1)

      def background_music(self):
            """
            Loads and plays the background music in a loop on channel 0.
            """
            self.background_channel.play(pygame.mixer.Sound(Assets.audio_background), loops=-1)

      def take_soldier(self):
            """
            Loads and plays the sound effect for taking a soldier on channel 1.
            """
            self.effect_channel.play(pygame.mixer.Sound(Assets.audio_take_pawn))

      def game_completed(self):
            """
            Loads and plays the sound effect for game completion on channel 1.
            """
            self.effect_channel.play(pygame.mixer.Sound(Assets.audio_game_completed))

      def stop(self):
            """
            Stops the currently playing music or sound effect.
            """
            self.background_channel.stop()
            self.effect_channel.stop()

      def pause(self):
            """
            Pauses the currently playing music or sound effect.
            """
            self.background_channel.pause()
            self.effect_channel.pause()

      def unpause(self):
            """
            Unpauses the currently paused music or sound effect.
            """
            self.background_channel.unpause()
            self.effect_channel.unpause()
