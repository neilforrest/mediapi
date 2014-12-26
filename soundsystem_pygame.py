import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

class Player:
  
  def play ( self, url ):
    pygame.mixer.music.load ( url )
    pygame.mixer.music.play ( -1 )
    
  def stop ( self ):
    pygame.mixer.music.stop ()
    
class Mixer:

  def setVolume ( self, volume ):
    pygame.mixer.music.set_volume ( volume/100.0 )
