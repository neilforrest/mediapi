import web
import soundsystem_pygame as soundsystem

urls = (
  '/api/player', 'Player',
  '/api/mixer', 'Mixer',
  '/control', 'Control'
)

render = web.template.render('templates/')

player= soundsystem.Player ()
mixer = soundsystem.Mixer ()

class Player:
  
  def PUT ( self ):
    i = web.input ( action= None, url= "media/sample.ogg" )
    if i.action == "play":
      player.play ( i.url )
    elif i.action == "stop":
      player.stop ()

class Mixer:
  
  def PUT ( self ):
    i = web.input ( volume= None )
    if not i.volume is None:
      mixer.setVolume ( int(i.volume) )

class Control:
  def GET ( self ):
    return render.control()


if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()

