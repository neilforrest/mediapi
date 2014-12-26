import web

urls = (
  '/api/player', 'Player',
  '/api/mixer', 'Mixer',
  '/control', 'Control'
)

render = web.template.render('templates/')

class Player:
  
  def PUT ( self ):
    i = web.input ( action= None )
    if i.action == "play":
      print "PLAY"
    elif i.action == "stop":
      print "STOP"

class Mixer:
  
  def PUT ( self ):
    i = web.input ( volume= None )
    if not i.volume is None:
      print "VOLUME: " + i.volume

class Control:
  def GET ( self ):
    return render.control()


if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()

