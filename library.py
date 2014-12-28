import os

class Library:

  def getGroups ( self, path ):
    raise NotImplementedError("Subclasses should implement this function!")
   
  def getItems ( self, path ):
    raise NotImplementedError("Subclasses should implement this function!")
    
    
class LibraryFilesystem ( Library ):

  def __init__ ( self, path= "media" ):
    self._path= path

  def getGroups ( self, path= [] ):
  
    groups= []
    
    p= list(path)
    p.insert ( 0, self._path )
    p= os.sep.join(p)
    for (dirpath, dirnames, filenames) in os.walk(p):
      groups.extend ( dirnames )
      break
    
    return groups
   
  def getItems ( self, path= [] ):
  
    items= []
    
    p= list(path)
    p.insert ( 0, self._path )
    p= os.sep.join(p)
    for (dirpath, dirnames, filenames) in os.walk(p):
      for f in filenames:
        items.append ( os.path.join ( dirpath, f ) )
      break
    
    return items
    
