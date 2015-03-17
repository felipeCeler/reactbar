from pymt import *
from pyglet.gl import *


class Canvas(RectangularWidget):
	def __init__(self, parent=None, min=0, max=100, pos=(0,0), size=(640,480)):
		RectangularWidget.__init__(self,parent, pos, size)
		self.touch_positions = {}
		self.fbo = Fbo((self.width, self.height))
		self.bgcolor = (0.8,0.8,0.7,1.0)
		self.color = (0,1,0,1.0)
		setBrush('particle.png')
		self.dict = {}
		self.databuffer = None
		self.clear()
		
	def clear(self):
		self.fbo.bind()
		glClearColor(*self.bgcolor)
		glClear(GL_COLOR_BUFFER_BIT)
		glClearColor(1,0,1,1)
		self.fbo.release()
        
	def draw(self):
		#self.clear()
		buffer = (GLubyte * (3* 100* 100))()
		
		self.fbo.bind()
		glColor4f(*self.color)
		for i in self.dict.itervalues():
			for tup in i:
				paintLine((tup[0],tup[1],tup[2],tup[3]))

		self.fbo.release()				
		glColor4f(1,1,1,1)
		drawTexturedRectangle( self.fbo.texture, size=(self.width, self.height))	
		
		
		       
	def on_touch_down(self, touches, touchID, x, y):
		self.touch_positions[touchID] = (x,y)
		self.dict[touchID] = [(x,y,x,y)]
		#self.fbo.bind()
		#glColor4f(*self.color)
		#paintLine((x,y,x,y))
		#glColor4f(1,1,1,1)
		#self.fbo.release()

	def on_touch_move(self, touches, touchID, x, y):
		if self.touch_positions[touchID]:
			ox,oy = self.touch_positions[touchID]	    	
			#self.fbo.bind()
			#glColor4f(*self.color)
			#paintLine((ox,oy,x,y))
			self.dict[touchID] = [(ox,oy,x,y)]
			#self.fbo.release()
			self.touch_positions[touchID] = (x,y)
	
	def on_touch_up(self, touches, touchID, x, y):
		print self.dict
		if self.touch_positions.has_key(touchID):
			del self.touch_positions[touchID]
		if self.dict.has_key(touchID):
			del self.dict[touchID]			


	    
root = Container()
w = UIWindow(root)

canvas = Canvas(size=(w.width,w.height))
root.add_widget(canvas)

slider = ColorPicker(size=(130,290), target=[canvas])
root.add_widget(slider)



runTouchApp()
