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
      
      def background_music(self):
            """
                  Loads and plays the background music in a loop.
            """
            pygame.mixer.music.load(Assets.audio_background)
            pygame.mixer.music.play(-1)


      def take_soldier(self):
            """
                  Loads and plays the sound effect for taking a soldier.
            """
            pygame.mixer.music.load(Assets.audio_take_pawn)
            pygame.mixer.music.play()
            

      def game_completed(self):
            """
                  Loads and plays the sound effect for game completion.
            """
            pygame.mixer.music.load(Assets.audio_game_completed)
            pygame.mixer.music.play()
            
            
      def stop(self):
            """
                  Stops the currently playing music or sound effect.
            """
            pygame.mixer.music.stop()
            

      def pause(self):
            """
                  Pauses the currently playing music or sound effect.
            """
            pygame.mixer.music.pause()
      

      def unpause(self):
            """
                  Unpauses the currently paused music or sound effect.
            """
            pygame.mixer.music.unpause()