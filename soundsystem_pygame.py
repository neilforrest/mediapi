import pygame
import threading
import time

poll_interval= 5

class Player ( threading.Thread ):
  
  def __init__ ( self ):
    threading.Thread.__init__ ( self )
    
    self.now_playing= None
    self.queue= []
    
    self.callbacks= []
    self.condition= threading.Condition()
    self.sync_callbacks= threading.Condition()
    
    self.mutex= threading.Lock ()
    
    self.daemon = True
    self.start()
    
  def run ( self ):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    
    while True:
      
      self.condition.acquire ()
      self.condition.wait ( poll_interval )
      
      self.processCallbacks ()
      self.processQueue ()
      
      self.condition.release ()
    
  def processCallbacks ( self ):
  
    if len(self.callbacks) > 0:
      while len(self.callbacks) > 0:
        (callback, data)= self.callbacks[0]
        if data is None:
          callback ()
        else:
          callback ( data )
        del self.callbacks[0]
      
      self.sync_callbacks.acquire()
      self.sync_callbacks.notify()
      self.sync_callbacks.release()
  
  def processQueue ( self ):
    
    if not pygame.mixer.music.get_busy ():
      if len(self.queue) > 0:
        url= self.queue[0]
        self.now_playing= url
        del self.queue[0]
        pygame.mixer.music.load ( url )
        pygame.mixer.music.play ()
      elif self.now_playing:
        self.now_playing= None
  
  def addCallback ( self, callback, data= None, sync= False ):
  
    self.condition.acquire ()
    self.callbacks.append ( (callback,data) )
    self.condition.notify ()
    self.condition.release ()
    
    if sync:
      self.sync_callbacks.acquire()
      self.sync_callbacks.wait()
      self.sync_callbacks.release()
  
  def play ( self ):
    """ 
    """
    
    self.addCallback ( self.playCallback )
    
  def playCallback ( self ):
    pygame.mixer.music.unpause ()
    
  def stop ( self ):
    """ 
    """
    
    self.addCallback ( self.stopCallback )
    
  def stopCallback ( self ):
    pygame.mixer.music.pause ()
    
  def appendItem ( self, url ):
    self.condition.acquire ()
    self.queue.append ( url )
    self.condition.notify ()
    self.condition.release ()

  def deleteItem ( self, index ):

    self.addCallback ( self.skipCallback, sync= True )
    
  def skipCallback ( self ):
    pygame.mixer.music.stop ()
    
  def getQueue ( self ):
  
    self.condition.acquire ()
    q= []
    if self.now_playing:
      q.append ( self.now_playing )
    q.extend ( self.queue )
    self.condition.release ()
    
    return q

  def setVolume ( self, volume ):
    self.addCallback ( self.setVolumeCallback, volume )
  
  def setVolumeCallback ( self, volume ):
    pygame.mixer.music.set_volume ( volume/100.0 )
