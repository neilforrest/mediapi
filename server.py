import web
import soundsystem_pygame as soundsystem
import library

urls = (
  '/api/player', 'Player',
  '/api/mixer', 'Mixer',
  '/api/queue', 'Queue',
  '/control/*(.*)', 'Control',
  '/library/*(.*)', 'Library'
)

render = web.template.render('templates/')

player= soundsystem.Player ()

library= library.LibraryFilesystem()

class Player:
  
  def PUT ( self ):
    i = web.input ( action= None )
    if i.action == "play":
      player.play ()
    elif i.action == "stop":
      player.stop ()

class Mixer:
  
  def PUT ( self ):
    i = web.input ( volume= None )
    if not i.volume is None:
      player.setVolume ( int(i.volume) )

class Library:
  def GET ( self, path ):
    path_list= path.split ( "/" )
    groups= library.getGroups ( path_list )
    items = library.getItems ( path_list )
    return render.library ( path, groups, items )

class Queue:

  def POST ( self ):
  
    i= web.input ( url= None )
    if i.url:
      player.appendItem ( i.url )
      
  def DELETE ( self ):
    
    i= web.input ( index= 0 )
    player.deleteItem ( i.index )
  
class Control:
  def GET ( self, path ):
    if path == "queue":
      return render.queue ( player.getQueue () )
    else:
      return render.control ()

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()

