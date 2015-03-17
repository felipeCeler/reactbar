from pymt import *
from math import *
from copy import *
from datetime import *

import socket
import pickle

import time
import osc
from  pyglet import font 

            
class Canvas(DragableWidget):
    def __init__(self, parent=None, min=0, max=100, pos=(0,0), size=(640,480),file="fbo.react"):
        RectangularWidget.__init__(self,parent, pos, size)
        self.fbo = Fbo((self.width, self.height))
        self.l = []
        self.keytouch = {}
        self.touch_positions = {}
        self.state = ('normal', None)
        #self.bgcolor = (0.8,0.8,0.7,1.0)
        self.bgcolor = (1.0,1.0,1.0,1.0)
        self.color = (0,1,0,1.0)
        setBrush('images/particle.png')
        self.rX = 0
        self.rY = 0
        self.file = file
        self.clear()


    def open(self):

        pkl_file = open(self.file, 'rb')
        
        self.keytouch = pickle.load(pkl_file)
        
        pkl_file.close()
        

    def clear(self):
        
        # Pickle dictionary using protocol 0.
        output = open( self.file, 'wb')        
        pickle.dump(self.keytouch, output)
        
        # Pickle the list using the highest protocol available.
        output.close()        
        
        self.fbo.bind()
        glClearColor(*self.bgcolor)
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(1,0,1,1)
        self.fbo.release()
        self.touch_positions = {}
        self.keytouch = {}
        self.l=[]    
            
       
    def draw(self):
        self.fbo.bind()
        glColor4f(*self.color)
        for i in self.keytouch.itervalues():
            for p in i:
                     paintLine((p[0],p[1],p[2],p[3]))
        
        self.fbo.release()                
        glColor4f(1,1,1,1)
        drawTexturedRectangle( self.fbo.texture,pos=(self.x,self.y), size=(self.width, self.height))

            
    def on_touch_down(self, touches, touchID, x, y):
        self.touch_positions[touchID] = (x,y)
        self.l.append((x,y,x,y))
        self.keytouch[touchID] = self.l
        

    def on_touch_move(self, touches, touchID, x, y):
      if  touchID  in self.touch_positions:
        if self.touch_positions[touchID]:
            ox,oy = self.touch_positions[touchID]            
            self.l.append((ox,oy,x,y))
            self.keytouch[touchID] = self.l
            self.touch_positions[touchID] = (x,y)

    def on_touch_up(self, touches, touchID, x, y):
        if self.touch_positions.has_key(touchID):
            del self.touch_positions[touchID]
        if not self.keytouch.has_key(touchID):
            self.keytouch[touchID] = self.l
            self.l = []
                     
    
#    def __init__(self, parent=None, min=0, max=100, pos=(0,0), size=(640,480)):
#        RectangularWidget.__init__(self,parent, pos, size)
#        self.touch_positions = {}
#        self.fbo = Fbo((self.width, self.height))
#        self.bgcolor = (0.8,0.8,0.7,1.0)
#        self.color = (0,1,0,1.0)
#        setBrush('images/particle.png')
#        self.dict = {}
#        self.clear()
#        self.rX = 0
#        self.rY = 0
#        self.l = []
#
#    def open(self):
#
#        
#        pkl_file = open('fbo.react', 'rb')
#        
#        self.dict = pickle.load(pkl_file)
#        
#        pkl_file.close()
#            
#        
#    def clear(self):
#        #        
#        # Pickle dictionary using protocol 0.
#        output = open('fbo.react', 'wb')        
#        pickle.dump(self.dict, output)
#        
#        # Pickle the list using the highest protocol available.
#        output.close()        
#        
#        
#        self.fbo.bind()
#        glClearColor(*self.bgcolor)
#        glClear(GL_COLOR_BUFFER_BIT)
#        glClearColor(1,0,1,1)
#        self.fbo.release()
#        self.dict = {}
#        
#    def draw(self):
#        #self.clear()
#
#        
#        self.fbo.bind()
#        glColor4f(*self.color)
#        for i in self.dict.itervalues():
#            for p in i:
#                     paintLine((p[0],p[1],p[2],p[3]))
#        
#        self.fbo.release()                
#        glColor4f(1,1,1,1)
#        drawTexturedRectangle( self.fbo.texture, size=(self.width, self.height))    
#
#        
#               
#    def on_touch_down(self, touches, touchID, x, y):
#        self.touch_positions[touchID] = (x,y)
#        #self.dict[touchID] = [(x,y,x,y)]
#        self.l.append((x,y,x,y))
#        #self.fbo.bind()
#        #glColor4f(*self.color)
#        #paintLine((x,y,x,y))
#        #glColor4f(1,1,1,1)
#        #self.fbo.release()
#
#    def on_touch_move(self, touches, touchID, x, y):
#      print self.dict
#      if  touchID  in self.touch_positions:
#        if self.touch_positions[touchID]:
#            ox,oy = self.touch_positions[touchID]            
#            #self.fbo.bind()
#            #glColor4f(*self.color)
#            #paintLine((ox,oy,x,y))
#            #self.dict[touchID] = [(ox,oy,x,y)]
#            self.l.append((ox,oy,x,y))
#            #self.fbo.release()
#            self.touch_positions[touchID] = (x,y)
#    
#    def on_touch_up(self, touches, touchID, x, y):
#        print self.dict
#        if self.touch_positions.has_key(touchID):
#            del self.touch_positions[touchID]
#        if not self.dict.has_key(touchID):
#            self.dict[touchID] = self.l
#            self.l = []         

    
#    def __init__(self, parent=None, min=0, max=100, pos=(0,0), size=(640,480)):
#        RectangularWidget.__init__(self,parent, pos, size)
#        self.fbo = Fbo((self.width, self.height))
#        
#        self.keytouch = {}
#        self.touch_positions = {}
#        self.state = ('normal', None)
#        #self.bgcolor = (0.8,0.8,0.7,1.0)
#        self.bgcolor = (1.0,1.0,1.0,1.0)
#        self.color = (0,1,0,1.0)
#        setBrush('images/particle.png')
#        self.rX = 0
#        self.rY = 0
#        self.clear()
#
#    def open(self):
#
#        global fboT
#        
#        self.fbo.texture = deepcopy(fboT)
#        
#
#    def clear(self):
#        
#        global fboT
#        
#        fboT =deepcopy(self.fbo.texture)
#        
#        self.fbo.bind()
#        glClearColor(*self.bgcolor)
#        glClear(GL_COLOR_BUFFER_BIT)
#        glClearColor(1,0,1,1)
#        self.fbo.release()
#        self.touch_positions = {}    
#            
#       
#    def draw(self):
#        glColor4f(1,1,1,1)
#        drawTexturedRectangle( self.fbo.texture,pos=(self.x,self.y), size=(self.width, self.height))
#
#            
#    def on_touch_down(self, touches, touchID, x, y):
#        self.keytouch[touchID] = [(x,y,x,y)]
#        self.touch_positions[touchID] = (x,y)
#        self.fbo.bind()
#        glColor4f(*self.color)
#        paintLine((x,y,x,y))
#        glColor4f(1,1,1,1)
#        self.fbo.release()
#
#    def on_touch_move(self, touches, touchID, x, y):
#        if  touchID  in self.touch_positions:
#            if self.touch_positions[touchID]:
#                ox,oy = self.touch_positions[touchID]
#                self.fbo.bind()
#                glColor4f(*self.color)
#                self.keytouch[touchID] = [(ox,oy,x,y)]
#                paintLine((ox,oy,x,y))
#                self.fbo.release()
#                self.touch_positions[touchID] = (x,y)
                
          

    
class PaintWidget(Button):

    def __init__(self, image_file, parent=None, pos=(0,0), size=(1,1), scale = 1.0,layer=0,file=""):
        Button.__init__(self,parent,pos,size)
        img = pyglet.image.load(image_file)
        
        self.file = file
        self.image = pyglet.sprite.Sprite(img)
        self.image.x, self.image.y = self.x, self.y
        self.scale =  scale
        self.layer = layer
        self.image.scale = self.scale
        self.width, self.height = (self.image.width, self.image.height)
        self.canvas =  Canvas(parent=parent,size=(250,150),file="fbo.react")
        self.buttonClean = ImageButton("images/clear.png",parent=c, pos=(0,50), size=(10,10))
        self.buttonClose = ImageButton("images/clear.png",parent=c, pos=(0,50), size=(10,10))
        self.buttonSend = ImageButton("images/send.png",parent=c, pos=(0,70), size=(10,10))
        
        self.buttonR = ImageButton("images/red.png",parent=c, pos=(0,70), size=(10,10))
        self.buttonG = ImageButton("images/green.png",parent=c, pos=(0,70), size=(10,10))
        self.buttonB = ImageButton("images/blue.png",parent=c, pos=(0,70), size=(10,10))
        self.buttonBlack = ImageButton("images/black.png",parent=c, pos=(0,70), size=(10,10))
        
        self.n =  pyglet.text.Label("OLA - mesa 4" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
        
        self.canvas.rX = 25
        self.canvas.rY = 25
        
        self.bsx = 125
        self.bsy = -20
        
        self.bcx =  0
        self.bcy = 50
        
        self.bclx =  0
        self.bcly = 0
        # --- 
        self.bredx = 10
        self.bredy = -20
        
        self.bgreenx = 70  
        self.bgreeny = -20
        
        self.bblackx =  185
        self.bblacky = -20
        
        self.bbluex =  245
        self.bbluey = -20
        
        
        
    def draw(self):
        self.canvas.x,self.canvas.y=self.x+self.canvas.rX, self.y+self.canvas.rY
        self.buttonClean.x,self.buttonClean.y=self.x+self.bcx, self.y+self.bcy
        self.buttonClose.x,self.buttonClose.y=self.x+self.bclx, self.y+self.bcly
        self.buttonSend.x,self.buttonSend.y=self.x+self.bsx, self.y+self.bsy
        
        self.buttonR.x,self.buttonR.y = self.x+self.bredx, self.y+self.bredy
        self.buttonG.x,self.buttonG.y =   self.x+self.bgreenx, self.y+self.bgreeny
        self.buttonB.x,self.buttonB.y = self.x+self.bbluex, self.y+self.bbluey
        self.buttonBlack.x,self.buttonBlack.y = self.x+self.bblackx, self.y+self.bblacky 
        
        
        self.n.x ,self.n.y  = self.x+20 ,self.y+170
        self.image.x, self.image.y = (self.x, self.y)
        self.image.scale = self.scale
        self.width, self.height = (self.image.width, self.image.height)
        self.image.draw()
        self.canvas.draw()
        self.buttonClean.draw()
        self.buttonClose.draw()
        self.buttonSend.draw()
        self.n.draw()
#        self.buttonBlack.draw()
#        self.buttonR.draw()
#        self.buttonG.draw()
#        self.buttonB.draw()                

#    def __init__(self, parent=None, pos=(0,0), size=(200,300),layer=0):
#        RectangularWidget.__init__(self,parent, pos, size)
#        self.state = ('normal', None)
#        self.canvas =  Canvas(parent=parent,size=(200,100))
#        
#    def draw(self):
#        self.canvas.x,self.canvas.y=self.x+50, self.y+50
#        drawRectangle((self.x, self.y) ,(self.width, self.height))
#        self.canvas.draw()
        
    def on_touch_down(self, touches, touchID, x, y):

        if self.buttonClean.collidePoint(x,y):
            self.canvas.clear()

        if self.buttonClose.collidePoint(x,y):
            self.parent.layers[self.layer].remove(self)
            return True
            print "opa"
        
        if self.buttonSend.collidePoint(x,y):
            self.canvas.open()
            print "opa"

        
        if self.canvas.collidePoint(x,y):
            self.canvas.on_touch_down(touches, touchID,x+self.x,y+self.y)
            return True
        if self.collidePoint(x,y):
            self.state = ('dragging', touchID, x, y)
            return True
    def on_touch_move(self, touches, touchID, x, y):
        if self.canvas.collidePoint(x,y):
            self.canvas.on_touch_move(touches, touchID ,x-self.x-self.canvas.rX,y-self.y-self.canvas.rY)
            return True
        
        if self.state[0] == 'dragging' and self.state[1]==touchID:
            self.x, self.y = (self.x + (x - self.state[2]) , self.y + y - self.state[3])
            self.state = ('dragging', touchID, x, y)
            return True
    def on_touch_up(self, touches, touchID, x, y):
        if self.canvas.collidePoint(x, y):
            self.canvas.on_touch_up(touches, touchID, x, y)
        if self.state[1] == touchID:
            self.state = ('normal', None)
            return True


class ImageWidget(ZoomableImage):
    def __init__(self, image_src,id= 0, parent=None,pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,string=""):
        
        ZoomableImage.__init__(self,image_src, parent, pos, size,layer)
        self.id = id
        img = pyglet.image.load(image_src)
        self.string = string
        self.image = image_src
        self.texture = img.get_texture()
        self.texture.width , self.texture.height = size
        
        self.alfaC = 0.01
        self.zoomC = 0.1
        
        self.cont = 0
        
        self.velocity = 10.0
        self.acceleration = 0.5
        
        
        self.x , self.y = pos
        self.scale =  scale
        self.alfa = alfa
        
       
        glBindTexture(self.texture.target, self.texture.id)
       
   
    def radius(self):
            radius = sqrt(self.width*self.width + self.height*self.height)*0.75 *self.zoom
            #radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
    # It tests if tow widget  collided   
    def collideWidget(self,widget):
            
            radius = self.radius() + widget.radius()
            
            dist = Length(self.translation - widget.translation)
            
            if radius >= dist:
               return True
            else:
              return False
     
     # It tests if touch Point is on the widget     
    def collidePoint(self, x,y):
            radius = sqrt(self.width*self.width+0.5 + self.height*self.height*0.5)/2 *self.zoom
            dist = Length(self.translation - Vector(x,y))
            if radius >= dist:
               #self.parent.layers[self.layer].remove(self) 
               return True
 
            else:
              return False
          
    def on_object_down(self, touches, touchID,id, x, y,angle):
        return False    
    def on_object_move(self, touches, touchID, id ,x, y,angle):
        return False
    def on_object_up(self, touches, touchID, id ,x, y,angle):
        return False           
    def drawSelf(self):

#       glTranslatef(self.translation[0], self.translation[1], 0)
#       #glRotatef(self.rotation , 0, 0, 1)
       glPushMatrix()
       glColor4f(1,1,1,self.alfa) 
       glScalef(self.zoom, self.zoom, 1)
       glScalef(self.width, self.height, 1)
       self.draw_widget()
       glPopMatrix()
       
    def draw(self):

       glPushMatrix()
       glTranslatef(self.translation[0], self.translation[1], 0)
       glRotatef(self.rotation , 0, 0, 1)
       glScalef(self.zoom, self.zoom, 1)
       glScalef(self.width, self.height, 1)
       self.draw_widget()
       glPopMatrix()
        
    def draw_widget(self):
        
      
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        #glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        glPopAttrib()
        

    

class Bill(ImageWidget):
    def __init__(self, image_src,id=0, parent=None, pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,name="Guest"):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)

        self.iconPos = self.width*0.50
        
        self.iconPosReal = -(-size[0]*0.155 )*0.5 
        
        self.e = self.width*0.5

        data = datetime.today().strftime("%d/%m/%y")
        hora = datetime.today().strftime("%H:%M")

        self.e -= self.iconPosReal                
        m1 = ImageWidget(id=self.id,image_src="images/cima_laranja.png",parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
        b1 = ImageWidget(id=self.id,image_src="images/icon_beer.png",parent=parent,pos=(-self.height*0.40,self.e+10), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
        l1 = pyglet.text.Label(name+"                     "+data ,font_size=size[0]*0.025,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
        self.e -= self.iconPosReal
                
#        m2 = ImageWidget(id=self.id,image_src="images/faixa_verde.png",id=self.id,parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b2 = ImageWidget(id=self.id,image_src="images/icon_beer.png",id=self.id,parent=parent,pos=(-self.height*0.40,self.e+10), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l2 = pyglet.text.Label("draft beer brahama 300ml               $3,30" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
#        self.e -= self.iconPosReal
#        
#        m3 = ImageWidget(id=self.id,image_src="images/faixa_laranja.png",id=self.id,parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b3 = ImageWidget(id=self.id,image_src="images/icon_beer.png",id=self.id,parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l3 = pyglet.text.Label("draft beer brahama 200ml               $2,30" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#        
#        m4 = ImageWidget(id=self.id,image_src="images/faixa_verde.png",id=self.id,parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b4 = ImageWidget(id=self.id,image_src="images/icon_beer.png",id=self.id,parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l4 = pyglet.text.Label(" beer itaipava 330ml                       $3,30" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#        
#        m5 = ImageWidget(id=self.id,image_src="images/faixa_laranja.png",id=self.id,parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b5 = ImageWidget(id=self.id,image_src="images/icon_beer.png",id=self.id,parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l5 = pyglet.text.Label("draft beer skol 330ml                      $3,50" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#        
#        m6 = ImageWidget(id=self.id,image_src="images/faixa_verde.png",id=self.id,parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b6 = ImageWidget(id=self.id,image_src="images/icon_beer.png",id=self.id,parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l6 = pyglet.text.Label("beer stella artroir 330ml                 $4,00" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#
#        m7 = ImageWidget(id=self.id,image_src="images/faixa_laranja.png",id=self.id,parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b7 = ImageWidget(id=self.id,image_src="images/icon_beer.png",id=self.id,parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l7 = pyglet.text.Label("beer stella artroir 330ml               $4,00" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#        
#        m8 = ImageWidget(id=self.id,image_src="images/faixa_verde.png",id=self.id,parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b8 = ImageWidget(id=self.id,image_src="images/icon_beer.png",parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l8 = pyglet.text.Label("beer stella artroir 330ml               $4,00" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#
#        m9 = ImageWidget(id=self.id,image_src="images/faixa_verde.png",parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b9 = ImageWidget(id=self.id,image_src="images/icon_beer.png",parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l9 = pyglet.text.Label("beer stella artroir 330ml               $4,00" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#
#        m10 = ImageWidget(id=self.id,image_src="images/faixa_verde.png",parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b10 = ImageWidget(id=self.id,image_src="images/icon_beer.png",parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l10 = pyglet.text.Label("beer stella artroir 330ml               $4,00" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
#        
#        m11 = ImageWidget(id=self.id,image_src="images/faixa_verde.png",parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
#        b11 = ImageWidget(id=self.id,image_src="images/icon_beer.png",parent=parent,pos=(-self.height*0.40,self.e), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=layer )
#        l11 = pyglet.text.Label("beer stella artroir 330ml               $4,00" ,font_size=10,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)        
#        self.e -= self.iconPosReal
        
        m12 = ImageWidget(id=self.id,image_src="images/baixo_laranja.png",parent=parent,pos=(0,self.e), size=(size[0],size[1] ),alfa = 1.0,layer=layer )
        #self.e -= self.iconPosReal
        
        self.place = ["m2","m3","m4","m5","m6","m7","m8","m9","m10"]
        self.widgets =  {"m1":m1,"m12":m12}#,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"z1":b1,"z2":b2,"z3":b3,"z2":b4,"z4":b5,"z5":b5,"m8":m8,"m9":m9,"m10":m10,"m11":m11}
        
        
        self.cont = 2
        
        self.labels = [l1]#,l2,l3,l4,l5,l6,l7,l8,l9,l10]
        
        #l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11
        self.labelPos = 0.075

       
        
        #self.menuInicial =  {"m1":m1,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"m8":m8}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius        

    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
        x = 0.41150 
        for l in self.labels:
            l.x = -self.width*0.25
            l.y = self.height*x
            l.draw()
            x -= self.labelPos
               
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        

        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    pass
                    #widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

        #ic = ImageWidget(id=self.id,image_src="images/icon_wine.png",parent=self.parent,pos=(-self.height*0.40,self.iconPos), size=(self.height*0.033333*self.scale,self.width*0.04166*self.scale ),alfa = 1.0,layer=self.layer )
#        ic = ImageWidget(id=self.id,image_src="images/icon_wine.png",parent=self.parent,pos=(-self.height*0.40,self.iconPos), size=(self.height*0.035*self.scale,self.width*0.035*self.scale ),alfa = 1.0,layer=self.layer )
#        self.iconPos -= self.iconPosReal
#        self.widgets["z"+str(self.iconPos)] = ic
        
        if len(self.touchDict) == 1:
                    print 'rotated'
#                    self.rotation +=180
                    self._oldrotation +=180
                    
        if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):                
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()       
class MenuMessage(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,principal = None):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)

        self.principal = principal 
        
        self.posW = size[0]*0.18*0.685
        self.posO = size[0]*0.325*0.7
        
        self.move = True
        
        
        e = self.posO

        beer  = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="1" )
        drink = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="2")
        wine = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-2*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="3")
        coke = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-3*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="4" )
        coffe = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-4*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="5")
        back = ImageWidget(id=self.id,image_src="images/cback.png",parent=parent,pos=(-size[0]*0.375,self.posO-5*self.posW), size=(size[0]*0.1,size[1]*0.1),alfa = 1.0,layer=layer )
        # "hi" , ":)", ";)","hey","long"
        self.widgets =  {"1":beer,
                                "2":drink,
                                "3":wine,
                                "4":coke,
                                "5":coffe,
                                "back":back}#{"m1":m1,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"z2":b1}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius        

    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if widget.layer == 9:
                        
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)                                                                                                                                    # Terceiro Slot do BILL                                               
                       beer = ImageWidget(id=self.id,image_src="images/cartinha_selecao.png",parent=self.parent,pos=(widget.x,widget.y), size=(widget.height*4,widget.width*4),alfa = 1.0,layer=self.layer+4,string=widget.string )
                       beer.translation[0], beer.translation[1] = self.translation[0]+wx+100,self.translation[1]+wy+100 
                       beer.rotation = self.rotation 
                       widget.parent.add_widget(beer,beer.layer,'cur')
                       self.move = False
                                        
                    if key == "back":
                     self.move = True
                     self.parent.layers[self.layer].remove(self)
#                     self.principal.translation[0], self.principal.translation[1] = self.translation[0],self.translation[1] 
#                     self.principal.rotation = self.rotation
#                     self.principal.zoom = self.zoom
                      
                     self.principal.move = True
                     #self.parent.layers[self.principal.layer].append(self.principal)
                     return True
                    # widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

        if self.move: 
        
            if len(self.touchDict) == 1:
                    print 'rotated'
#                    self.rotation +=180
                    self._oldrotation +=180
                    
            if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


            self.parent.layers[self.layer].remove(self)
            self.parent.layers[self.layer].append(self)
            self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):         
        if self.move:       
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                                                
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                        
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
        if self.move:
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()      
class MapaBar(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 1.0,alfa = 1.0,layer=0, clients ={}):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)
        self.move = True
        self.posW = size[0]*0.25
        self.posOc = size[0]*0.05
        self.posOf = size[0]*0.25 
        
        m5 = size[0]*0.40,size[0]*0.50
        m6 = size[0]*0.28,size[0]*0.50
        m7 = size[0]*0.16,size[0]*0.50
        m8 = size[0]*0.40,-size[0]*0.50
        
        m9 = size[0]*0.20,size[0]*0.225
        m10 = -size[0]*0.20,size[0]*0.225
        
        m1 = -size[0]*0.25,self.posOc
        m2 =  size[0]*0.25,self.posOc
        m3 = -size[0]*0.25,-self.posOf
        m4 =  size[0]*0.15,-self.posOf
        
        self.clients = clients
        
        self.cadeira1 = ImageWidget(id=self.id,image_src="images/fem_verde.png",parent=parent,pos=m9, size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer ) 
        self.cadeira2 = ImageWidget(id=self.id,image_src="images/fem_verde.png",parent=parent,pos=m10, size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        
        self.canvas = PaintWidget("images/text.png",parent=self.parent, pos=(0,0), size=(500,600),layer=self.layer+3+4 )

        self.carta = ImageWidget(id=self.id,image_src="images/novo_icone_message.png",parent=parent,pos=m5, size=(size[0]*0.1,size[1]*0.10),alfa = 1.0,layer=layer )
        self.join  = ImageWidget(id=self.id,image_src="images/novo_icone_join.png",parent=parent,pos=m6, size=(size[0]*0.10,size[1]*0.10),alfa = 1.0,layer=layer )
        self.drink =  ImageWidget(id=self.id,image_src="images/novo_icone_drink.png",parent=parent,pos=m7, size=(size[0]*0.10,size[1]*0.10),alfa = 1.0,layer=layer )
        self.refresh =  ImageWidget(id=self.id,image_src="images/refresh.png",parent=parent,pos=m8, size=(size[0]*0.10,size[1]*0.10),alfa = 1.0,layer=layer )
                        
        mesa1 = ImageWidget(id=self.id,image_src="images/bola_mesa1.png",parent=parent,pos=m1, size=(size[0]*0.05,size[1]*0.05),alfa = 1.0,layer=layer )
        mesa2 = ImageWidget(id=self.id,image_src="images/bola_mesa2.png",parent=parent,pos=m2, size=(size[0]*0.05,size[1]*0.05),alfa = 1.0,layer=layer)
        mesa3 = ImageWidget(id=self.id,image_src="images/bola_mesa3.png",parent=parent,pos=m3, size=(size[0]*0.05,size[1]*0.05),alfa = 1.0,layer=layer)
        mesa4 = ImageWidget(id=self.id,image_src="images/bola_mesa4.png",parent=parent,pos=m4, size=(size[0]*0.05,size[1]*0.05),alfa = 1.0,layer=layer )
        
        #PerfilBar("images/background_perfil_bar.png",parent=parent,pos=(m1[0]-size[0]*0.07,m1[1]-size[0]*0.07) ,size=((100),(100) ),scale=scale,alfa = 1.0,layer = layer,sex="M",name="Guest",age="21",status="on")
        self.m11  = ImageWidget(id=self.id,image_src="images/fem_verde.png",parent=parent,pos=(m1[0]-size[0]*0.08,m1[1]), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        #self.m12  = ImageWidget(id=self.id,image_src="images/masc_amarelo.png",parent=parent,pos=(m1[0]-size[0]*0.07,m1[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        #self.m13  = ImageWidget(id=self.id,image_src="images/masc_verde.png",parent=parent,pos=(m1[0]+size[0]*0.07,m1[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m14  = ImageWidget(id=self.id,image_src="images/fem_vermelho.png",parent=parent,pos=(m1[0]+size[0]*0.08,m1[1]), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        
        self.m21  = ImageWidget(id=self.id,image_src="images/fem_verde.png",parent=parent,pos=(m2[0]-size[0]*0.07,m2[1]-size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        #self.m22  = ImageWidget(id=self.id,image_src="images/masc_amarelo.png",parent=parent,pos=(m2[0]-size[0]*0.07,m2[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m23  = ImageWidget(id=self.id,image_src="images/masc_verde.png",parent=parent,pos=(m2[0]+size[0]*0.07,m2[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        #self.m24  = ImageWidget(id=self.id,image_src="images/fem_vermelho.png",parent=parent,pos=(m2[0]+size[0]*0.07,m2[1]-size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
                
        self.m31  = ImageWidget(id=self.id,image_src="images/fem_verde.png",parent=parent,pos=(m3[0]-size[0]*0.07,m3[1]-size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m32  = ImageWidget(id=self.id,image_src="images/masc_amarelo.png",parent=parent,pos=(m3[0]-size[0]*0.07,m3[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m33  = ImageWidget(id=self.id,image_src="images/masc_verde.png",parent=parent,pos=(m3[0]+size[0]*0.07,m3[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m34  = ImageWidget(id=self.id,image_src="images/fem_vermelho.png",parent=parent,pos=(m3[0]+size[0]*0.07,m3[1]-size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        
        self.m41 = ImageWidget(id=self.id,image_src="images/fem_verde.png",parent=parent,pos=(m4[0]-size[0]*0.07,m4[1]-size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m42  = ImageWidget(id=self.id,image_src="images/masc_amarelo.png",parent=parent,pos=(m4[0]-size[0]*0.07,m4[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m43  = ImageWidget(id=self.id,image_src="images/masc_verde.png",parent=parent,pos=(m4[0]+size[0]*0.07,m4[1]+size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )
        self.m44  = ImageWidget(id=self.id,image_src="images/fem_vermelho.png",parent=parent,pos=(m4[0]+size[0]*0.07,m4[1]-size[0]*0.07), size=(size[0]*0.1,size[1]*0.1),alfa = 0.1,layer=layer )        

        self.Perfil =  PerfilBar(id=self.id,image_src="images/background_perfil_bar.png",parent=self.parent, size=((100),(100) ),scale=2,alfa = 1.0,layer = self.layer+4 ,perfil=[])
        print self.Perfil.layer, "PERFIL LAYER"
                                                                                                                                                                                                        #Slot  Menu Bill                                     
        self.msg = MenuMessage(id=self.id,image_src="images/mbase.png",parent=parent, pos=m5, size=((150),(150) ),alfa = 1.0 ,layer=self.layer+1+4, principal = self)
        self.msg.move = True
                                                                                                                                                                                                        #Slot  Menu                                                  
        self.drinks = MenuDrinKBar(id=self.id,image_src="images/menu_drink.png",parent=parent, pos=m7, size=((250),(250) ),alfa = 1.0 ,layer=self.layer+2+4, principal = self)
        self.drinks.move = True

        #self.widgets = {"zjoin":self.join,"zdrink":self.drink,"zcarta":self.carta,"zrefresh":self.refresh,"mesa1":mesa1,"mesa2":mesa2,"mesa3":mesa3,"mesa4":mesa4,"mz1":self.m11,"mz5":self.m12,"mz9":self.m13,"mz13":self.m14,"mz2":self.m21,"mz6":self.m22,"mz10":self.m23,"mz14":self.m24,"mz3":self.m31,"mz7":self.m32,"mz11":self.m33,"mz15":self.m34,"mz4":self.m41,"mz8":self.m42,"mz12":self.m43,"mz16":self.m44}
        self.widgets = {"127.0.0.1":self.cadeira2,"127.0.0.2":self.cadeira1,"zjoin":self.join,"zdrink":self.drink,"zcarta":self.carta,"zrefresh":self.refresh,
                                "mesa1":mesa1,"mesa2":mesa2,"mesa3":mesa3,"mesa4":mesa4,
                                "mz11":self.m11,"127.0.0.3":self.m14,"127.0.0.4":self.m21,"127.0.0.5":self.m23,
                                "mz31":self.m31,"127.0.0.6":self.m32,"127.0.0.7":self.m33,"127.0.0.8":self.m34,
                                "mz41":self.m41,"127.0.0.10":self.m42,"127.0.0.11":self.m43,"127.0.0.12":self.m44}#"mz1":self.m11,"mz13":self.m14,"mz2":self.m21,"mz10":self.m23,"mz3":self.m31,"mz7":self.m32,"mz11":self.m33,"mz15":self.m34,"mz4":self.m41,"mz8":self.m42,"mz12":self.m43,"mz16":self.m44}
        
        self.places = {"127.0.0.2":self.m11,"127.0.0.3":self.m14,"mz21":self.m21,"mz23":self.m23,"mz31":self.m31,"mz32":self.m32,"mz33":self.m33,"mz34":self.m34,"mz41":self.m41,"mz42":self.m42,"mz43":self.m43,"mz44":self.m44} 
        self.place = ["mz11","mz12","mz13","mz14","mz21","mz22","mz23","mz24","mz31","mz32","mz33","mz34","mz41","mz42","mz43","mz44"]
         
        self.personal = {}
         
        self.active =  {"mesa1":True,"mesa2":True,"mesa3":True,"mesa4":True,"mz11":False,"mz1":False,"mz5":False,"mz9":False,"mz13":False,"mz2":False,"mz6":False,"mz10":False,"mz3":False,"mz7":False,"mz11":False,"mz15":False,"mz4":False,"mz8":False,"mz12":False,"mz16":False}  
              
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
      
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
        
    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        if len(self.parent.layers[self.layer+3]) == 0 and len(self.parent.layers[self.layer+3+4]) == 0 and len(self.parent.layers[self.layer+1+4]) == 0 and len(self.parent.layers[self.layer+2+4]) == 0 and len(self.parent.layers[self.layer+4])==0:
            self.alfa = 1.0
        else:
            self.alfa = 0.25    
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
            #widget.update()
        
    def on_touch_down(self, touches, touchID, x, y):

       for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                 if key == "zjoin"  or key == "zdrink"  or key == "zcarta":
                     pass
# COM REDE                     
#                        if len(self.parent.layers[self.layer+4]) > 0:
#                            osc.sendMsg("/tuio/Set",self.parent.obj[self.id][1].client[self.id],'127.0.0.1',30001)
                 if key == "zcarta":   
                 
                    self.msg.translation[0], self.msg.translation[1] = self.translation[0],self.translation[1] 
                    self.msg.rotation = self.rotation
                    self.msg.zoom = self.zoom
                    self.msg.parent.add_widget(self.msg,self.msg.layer,'cur')  
#                    self.canvas = PaintWidget("images/text.png",parent=self.parent, pos=(0,0), size=(500,600),layer=self.layer+3+4 )
#                    self.canvas.x, self.canvas.y = 300,300
#                    print self.canvas.layer
#                    self.parent.add_widget(self.canvas,self.canvas.layer,'cur')           
                    self.move = False

                 if key == "zdrink":   
                    self.drinks.translation[0], self.drinks.translation[1] = self.translation[0],self.translation[1] 
                    self.drinks.rotation = self.rotation
                    self.drinks.zoom = self.zoom
                    self.drinks.parent.add_widget(self.drinks,self.drinks.layer,'cur')           
                    self.move = False                                                                  
                 if key == "zrefresh":
                        print self.id 
#                        osc.sendMsg("/tuio/Get", [self.parent.obj[self.id][1].client_host,self.parent.obj[self.id][1].client_port,self.parent.obj[self.id][1].client_host,self.parent.obj[self.id][1].name,self.parent.obj[self.id][1].age,self.parent.obj[self.id][1].sex,self.parent.obj[self.id][1].status,"mulher1.png","33333"],self.parent.obj[self.id][1].server_host,self.parent.obj[self.id][1].server_port)
#                        self.parent.obj[self.id][1].getClients()
                        print self.clients, "RECEBIDO"
   
                        for (key,w) in self.parent.clients.iteritems():#self.parent.obj[self.id][1].client.iteritems():
                           print key , "CIDADO"
                           print w , 'PERFIL'
                           status = w[5] 
                           sex = w[4]
                           if sex == "m" :
                               if status ==  "on":
                                   sex = "images/masc_verde.png"
                               elif status == "off" :
                                   sex = "images/masc_vermelho.png"
                               else:
                                   sex = "images/masc_amarelo.png"
                           if sex == "f" :
                               if status ==  "on":
                                   sex = "images/fem_verde.png"
                               elif status == "off" :
                                   sex = "images/fem_vermelho.png"
                               else:
                                   sex = "images/fem_amarelo.png"
                           if w[1] == self.parent.obj[self.id][1].client_port:
				   if status == "on"  :
					sex = "images/status_on.png"
				   elif status == "off":  	
					sex = "images/status_off.png"
				   else	:
				       sex = "images/status_yellow.png"
                                   self.widgets[w[0]] = ImageWidget(id=self.id,image_src=sex,parent=self.widgets[w[0]].parent,pos=(self.widgets[w[0]].x,self.widgets[w[0]].y), size=(self.widgets[w[0]].height,self.widgets[w[0]].width),alfa = 1.0,layer=self.widgets[w[0]].layer )
                           else:
                                    self.widgets[w[0]] = ImageWidget(id=self.id,image_src=sex,parent=self.widgets[w[0]].parent,pos=(self.widgets[w[0]].x,self.widgets[w[0]].y), size=(self.widgets[w[0]].height,self.widgets[w[0]].width),alfa = 1.0,layer=self.widgets[w[0]].layer )
                           print w[0] , "cadeira"         
                           
                           for i in w[7]:
                                    if int(i) == int(self.id):
                                        w[5] = "mark_on"
                           print w             
                           self.personal[w[0]] = w
                           print self.personal , "o que esta na minha lista"

                 elif key == "mesa1" or key == "mesa2" or key == "mesa3" or key == "mesa4":
#                     self.Perfil = PerfilBar("images/background_perfil_bar.png",parent=self.parent, size=((2*100),(2*100) ),scale=2,alfa = 1.0,layer = self.Perfil.layer,sex="M",name="Guest",age="21",status="on",photo="images/mulher1.png")   
#                     self.Perfil.translation[0], self.Perfil.translation[1] = self.translation[0],self.translation[1] 
#                     self.Perfil.rotation = self.rotation
#                     self.Perfil.zoom = self.zoom
#                     self.Perfil.parent.add_widget(self.Perfil,self.Perfil.layer,'cur') 
#                     self.move = False          
                     return True
                 else:
                   if key in self.personal:  
                     if len(self.personal[key]) > 0:
                         self.Perfil = PerfilBar(id=self.id,image_src="images/background_perfil_bar.png",parent=self.parent, size=((2*100),(2*100) ),scale=2,alfa = 1.0,layer = self.Perfil.layer,perfil=self.personal[key])   
                         self.Perfil.translation[0], self.Perfil.translation[1] = self.translation[0],self.translation[1] 
                         self.Perfil.rotation = self.rotation
                         self.Perfil.zoom = self.zoom
			 if self.personal[key][1] == self.id:
			     self.parent.obj[self.id][1].perfil.translation =  self.translation 
			     self.Perfil.parent.add_widget(self.parent.obj[self.id][1].perfil,self.parent.obj[self.id][1].perfil.layer,'cur')
                         elif len(self.Perfil.parent.layers[self.Perfil.layer]) > 0:
                             self.Perfil.parent.layers[self.Perfil.layer][0]= self.Perfil
                         else:     
                             self.Perfil.parent.add_widget(self.Perfil,self.Perfil.layer,'cur')
                         self.move = False          
                     return True                     
                     
#                    if key == "beer" :       
#                       self.beer.translation[0], self.beer.translation[1] = self.translation[0],self.translation[1] 
#                       self.beer.rotation = self.rotation
#                       self.beer.zoom = self.zoom
#                       self.beer.parent.add_widget(self.beer,self.beer.layer,'cur')           
#                       self.parent.layers[self.layer].remove(self)
#                       return True
#                    if key == "drink" :       
#                       self.drink.translation[0], self.drink.translation[1] = self.translation[0],self.translation[1] 
#                       self.drink.rotation = self.rotation
#                       self.drink.zoom = self.zoom
#                       self.drink.parent.add_widget(self.drink,self.drink.layer,'cur')           
#                       self.parent.layers[self.layer].remove(self)
#                       return True          
                       #widget.alfa -=0.1          
  
       if not self.collidePoint(x,y):
            return False

       if len(self.parent.layers[self.layer+3]) == 0 and len(self.parent.layers[self.layer+3+4]) == 0 and len(self.parent.layers[self.layer+1+4]) == 0 and len(self.parent.layers[self.layer+2+4]) == 0 and len(self.parent.layers[self.layer+4]) == 0:       
        if len(self.touchDict) == 1:
                    print 'rotated'
                    # aqui so pra rotacionar
                    #self.rotation +=180
                    self._oldrotation +=180
                    
        if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
         
                  
       return True
                        
    def on_touch_move(self, touches, touchID, x, y):          
        if len(self.parent.layers[self.layer+3]) == 0 and len(self.parent.layers[self.layer+3+4]) == 0 and len(self.parent.layers[self.layer+1+4]) == 0 and len(self.parent.layers[self.layer+2+4]) == 0 and len(self.parent.layers[self.layer+4]) == 0:      
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                        
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
        if len(self.parent.layers[self.layer+3]) == 0 and len(self.parent.layers[self.layer+1+4]) == 0  and len(self.parent.layers[self.layer+1+4]) == 0 and len(self.parent.layers[self.layer+2+4]) == 0 and len(self.parent.layers[self.layer+4]) == 0:
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()       
            
class Menu(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 1.0,alfa = 1.0,layer=0):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)
        
        self.posW = size[0]*0.335*0.5
        self.posO = size[0]*0.25 + self.posW
        
        beer  = ImageWidget(id=self.id,image_src="images/icon_beer.png",parent=parent,pos=(-size[0]*0.225,self.posO), size=(size[0]*0.15,size[1]*0.15),alfa = 1.0,layer=layer )
        drink = ImageWidget(id=self.id,image_src="images/icon_drink.png",parent=parent,pos=(-size[0]*0.225,self.posO-self.posW), size=(size[0]*0.15,size[1]*0.15),alfa = 1.0,layer=layer)
        wine = ImageWidget(id=self.id,image_src="images/icon_wine.png",parent=parent,pos=(-size[0]*0.225,self.posO-2*self.posW), size=(size[0]*0.15,size[1]*0.15),alfa = 1.0,layer=layer)
        coke = ImageWidget(id=self.id,image_src="images/icon_coke.png",parent=parent,pos=(-size[0]*0.225,self.posO-3*self.posW), size=(size[0]*0.15,size[1]*0.15),alfa = 1.0,layer=layer )
        coffe = ImageWidget(id=self.id,image_src="images/icon_coffe.png",parent=parent,pos=(-size[0]*0.225,self.posO-4*self.posW), size=(size[0]*0.15,size[1]*0.15),alfa = 1.0,layer=layer )
        food = ImageWidget(id=self.id,image_src="images/icon_food.png",parent=parent,pos=(-size[0]*0.225,self.posO-5*self.posW), size=(size[0]*0.15,size[1]*0.15),alfa = 1.0,layer=layer)

        self.beer = MenuBeeR(id=self.id,image_src="images/menu_beer.png",parent=parent, pos=(0,0), size=(size[0]*1.25,size[1]*1.25),alfa = 1.0 ,layer=self.layer+4, principal = self)
        self.drink = MenuDrinK(id=self.id,image_src="images/menu_drink.png",parent=parent, pos=(0,0), size=(size[0]*1.25,size[1]*1.25),alfa = 1.0 ,layer=self.layer+4, principal = self)

        self.widgets =  {"beer":beer,"drink":drink,"wine":wine,"coke":coke,"coffe":coffe,"food":food}#{"m1":m1,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"z2":b1}
        
              
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        

        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if key == "beer" :       
                       self.beer.translation[0], self.beer.translation[1] = self.translation[0],self.translation[1] 
                       self.beer.rotation = self.rotation
                       self.beer.zoom = self.zoom
                       self.beer.parent.add_widget(self.beer,self.beer.layer,'cur')           
                       self.parent.layers[self.layer].remove(self)
                       return True
                    if key == "drink" :       
                       self.drink.translation[0], self.drink.translation[1] = self.translation[0],self.translation[1] 
                       self.drink.rotation = self.rotation
                       self.drink.zoom = self.zoom
                       self.drink.parent.add_widget(self.drink,self.drink.layer,'cur')           
                       self.parent.layers[self.layer].remove(self)
                       return True          
                       #widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

       
        if len(self.touchDict) == 1:
                    print 'rotated'
                    self.rotation +=180
                    self._oldrotation +=180
                    
        if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):
                                      
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                        
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):

                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()  
class MenuMenssageBar(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,photoname="images/nome_marco.png"):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)

 
        name  = ImageWidget(id=self.id,image_src=photoname,parent=parent,pos=(-size[0]*0.2,size[0]*0.3), size=(size[0]*0.5,size[1]*0.5),alfa = 1.0,layer=9 ,string="1" )        
        #yes  = ImageWidget(id=self.id,image_src="images/drink_yes.png",parent=parent,pos=(-size[0]*0.175,-size[0]*0.3), size=(size[0]*0.2,size[1]*0.2),alfa = 1.0,layer=9 ,string="1" )
        #go =   ImageWidget(id=self.id,image_src="images/go.png",parent=parent,pos=(-size[0]*0.175,-size[0]*0.3), size=(size[0]*0.25,size[1]*0.25),alfa = 1.0,layer=9 ,string="2")

        self.widgets =  {"name":name}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius        

    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if key == "go":
                       print key
                       self.parent.layers[self.layer].remove(self)         
                       return True       
                    
                    # widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

        if len(self.touchDict) == 1:
                    print 'rotated'
                    # aqui so pra rotacionar
                    #self.rotation +=180
                    self._oldrotation +=180
                
        if len(self.touchDict) < 2:
                    v = Vector(x,y)
                    self.original_points[len(self.touchDict)] = v
                    self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
        return True
    def on_touch_move(self, touches, touchID, x, y):         

                if len(self.touchDict) == 1 and touchID in self.touchDict:
                   self.translation = Vector(x,y) - self.original_points[0] + self._translation
                   for (key,widget) in self.widgets.iteritems():             
                       if self.collidePointButton(x, y,widget):
                          if key == "name":#widget.alfa -=0.1
                            self.parent.layers[self.layer].remove(self)
                            return True                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                                                
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                        
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):

                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()            
                                
class MenuMarked(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,photoname="images/nome_marco.png"):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)

 
        name  = ImageWidget(id=self.id,image_src=photoname,parent=parent,pos=(-size[0]*0.1,size[0]*0.3), size=(size[0]*0.5,size[1]*0.5),alfa = 1.0,layer=9 ,string="1" )        
        #yes  = ImageWidget(id=self.id,image_src="images/drink_yes.png",parent=parent,pos=(-size[0]*0.175,-size[0]*0.3), size=(size[0]*0.2,size[1]*0.2),alfa = 1.0,layer=9 ,string="1" )
        go =   ImageWidget(id=self.id,image_src="images/go.png",parent=parent,pos=(-size[0]*0.175,-size[0]*0.3), size=(size[0]*0.25,size[1]*0.25),alfa = 1.0,layer=9 ,string="2")

        self.widgets =  {"go":go,"name":name}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius        

    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if key == "go":
                       print key
                       self.parent.layers[self.layer].remove(self)         
                       return True       
                    
                    # widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

            if len(self.touchDict) == 1:
                    print 'rotated'
                    #self.rotation +=180
                    self._oldrotation +=180
                
        if len(self.touchDict) < 2:
                    v = Vector(x,y)
                    self.original_points[len(self.touchDict)] = v
                    self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
        return True
    def on_touch_move(self, touches, touchID, x, y):         

                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                                                
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                        
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):

                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()                
class MenuDrinkOffer(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,photoname="images/nome_marco.png"):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)

 
        name  = ImageWidget(id=self.id,image_src=photoname,parent=parent,pos=(-size[0]*0.1,size[0]*0.3), size=(size[0]*0.5,size[1]*0.5),alfa = 1.0,layer=9 ,string="1" )        
        yes  = ImageWidget(id=self.id,image_src="images/drink_yes.png",parent=parent,pos=(-size[0]*0.175,-size[0]*0.3), size=(size[0]*0.2,size[1]*0.2),alfa = 1.0,layer=9 ,string="1" )
        no =   ImageWidget(id=self.id,image_src="images/drink_no.png",parent=parent,pos=(size[0]*0.175,-size[0]*0.3), size=(size[0]*0.2,size[1]*0.2),alfa = 1.0,layer=9 ,string="2")

        self.widgets =  {"yes":yes,"no":no,"name":name}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius        

    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if key == "yes":
                        print key
                        self.parent.layers[self.layer].remove(self)
                        return True     
                    if key == "no":
                        print key
                        self.parent.layers[self.layer].remove(self)
                        return True
                    # widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

            if len(self.touchDict) == 1:
                    print 'rotated'
                    #self.rotation +=180
                    self._oldrotation +=180
                
        if len(self.touchDict) < 2:
                    v = Vector(x,y)
                    self.original_points[len(self.touchDict)] = v
                    self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):         

                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                                                
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                        
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):

                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()      
                
                
class MenuBeeR(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,principal = None):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)

        self.principal = principal 
        
        self.posW = size[0]*0.18*0.4925
        self.posO = size[0]*0.325*0.5 
        
        self.move = True
        
        
        e = self.posO

        beer  = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=                    "draft brahma         300ml            $3.30" )
        drink = ImageWidget(id=self.id,image_src="images/selecao_verde_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=       "draft brahma         200ml            $3.30")
        wine = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-2*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=  "beer itaipava          330ml            $3.30")
        coke = ImageWidget(id=self.id,image_src="images/selecao_verde_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-3*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=    "beer SKOL             330ml            $3.50 ")
        coffe = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-4*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=  "beer stella artroit  330ml             $4.00")
        back = ImageWidget(id=self.id,image_src="images/back.png",parent=parent,pos=(-size[0]*0.375,self.posO-5*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=layer )
        
        self.widgets =  {"draft brahma          300ml              $3.30":beer,
                                "draft brahma          200ml              $3.30":drink,
                                "beer itaipava            330ml              $3.30":wine,
                                "beer SKOL               330ml               $3.50":coke,
                                "beer stella artroit     330ml               $4.00":coffe,
                                "back":back}#{"m1":m1,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"z2":b1}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if widget.layer == 6:
                        
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
                       beer = ImageWidget(id=self.id,image_src="images/selecao_cerveja.png",parent=self.parent,pos=(widget.x,widget.y), size=(widget.height*3,widget.width*3),alfa = 1.0,layer=self.layer+4,string=widget.string )
                       beer.translation[0], beer.translation[1] = self.translation[0]+wx+100,self.translation[1]+wy+100 
                       beer.rotation = self.rotation 
                       widget.parent.add_widget(beer,beer.layer,'cur')
                       self.move = False
                                        
                    if key == "back":
                     self.parent.layers[self.layer].remove(self)
                     self.principal.translation[0], self.principal.translation[1] = self.translation[0],self.translation[1] 
                     self.principal.rotation = self.rotation
                     self.principal.zoom = self.zoom
                     self.move = True
                     self.parent.layers[self.principal.layer].append(self.principal)
                     return True
                    # widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

        if self.move: 
        
            if len(self.touchDict) == 1:
                    print 'rotated'
                    #self.rotation +=180
                    self._oldrotation +=180
                    
            if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


            self.parent.layers[self.layer].remove(self)
            self.parent.layers[self.layer].append(self)
            self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):         
        if self.move:       
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                                                
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                        
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
        if self.move:
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()       
             
class MenuDrinKBar(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,principal=None):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)
        self.principal = principal
        self.posW = size[0]*0.18*0.5
        self.posO = size[0]*0.325*0.5 

        beer  = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 )
        drink = ImageWidget(id=self.id,image_src="images/selecao_verde_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 )
        wine = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-2*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 )
        coke = ImageWidget(id=self.id,image_src="images/selecao_verde_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-3*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 )
        coffe = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-4*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 )
        back = ImageWidget(id=self.id,image_src="images/back.png",parent=parent,pos=(-size[0]*0.375,self.posO-5*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=layer )
        
        self.widgets =  {"beer":beer,"drink":drink,"wine":wine,"coke":coke,"coffe":coffe,"back":back}#{"m1":m1,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"z2":b1}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        

        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if widget.layer == 9:
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)                                                                                                                 # Terceiro Slot do Menu                                       
                       drink = ImageWidget(id=self.id,image_src="images/selecao_drink.png",parent=self.parent,pos=(widget.x,widget.y), size=(widget.height*3,widget.width*3),alfa = 1.0,layer=self.layer+4 )
                       drink.translation[0], drink.translation[1] = self.translation[0]+wx+100,self.translation[1]+wy+100 
                       drink.rotation = self.rotation
                       widget.parent.add_widget(drink,drink.layer,'cur')
                       self.move = False
                                        
                    if key == "back":
                     self.parent.layers[self.layer].remove(self)
#                     self.principal.translation[0], self.principal.translation[1] = self.translation[0],self.translation[1] 
#                     self.principal.rotation = self.rotation
#                     self.principal.zoom = self.zoom
                     self.principal.move = True
                     self.parent.layers[self.principal.layer].append(self.principal)
                     return True
        
        if not self.collidePoint(x,y):
            return False

#        
        if len(self.touchDict) == 1:
                    print 'rotated'
                    #self.rotation +=180
                    self._oldrotation +=180
                    
        if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):            
            if self.move:           
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                        self.zoom = distNew/distOld * self._zoom
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
            if self.move:       
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()        
class MenuDrinK(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,principal=None):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)
        self.principal = principal 
        
        self.posW = size[0]*0.18*0.4925
        self.posO = size[0]*0.325*0.5 
        
        self.move = True
        
        
        e = self.posO

        beer  = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=                    "draft brahma         300ml            $3.30" )
        drink = ImageWidget(id=self.id,image_src="images/selecao_verde_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=       "draft brahma         200ml            $3.30")
        wine = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-2*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=  "beer itaipava          330ml            $3.30")
        coke = ImageWidget(id=self.id,image_src="images/selecao_verde_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-3*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=    "beer SKOL             330ml            $3.50 ")
        coffe = ImageWidget(id=self.id,image_src="images/selecao_laranja_vazia.png",parent=parent,pos=(-size[0]*0.375,self.posO-4*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=6 ,string=  "beer stella artroit  330ml             $4.00")
        back = ImageWidget(id=self.id,image_src="images/back.png",parent=parent,pos=(-size[0]*0.375,self.posO-5*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=layer )
        
        self.widgets =  {"draft brahma          300ml              $3.30":beer,
                                "draft brahma          200ml              $3.30":drink,
                                "beer itaipava            330ml              $3.30":wine,
                                "beer SKOL               330ml               $3.50":coke,
                                "beer stella artroit     330ml               $4.00":coffe,
                                "back":back}#{"m1":m1,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"z2":b1}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        

        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if widget.layer == 6:
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
                       drink = ImageWidget(id=self.id,image_src="images/selecao_drink.png",parent=self.parent,pos=(widget.x,widget.y), size=(widget.height*3,widget.width*3),alfa = 1.0,layer=self.layer+4,string=widget.string )
                       drink.translation[0], drink.translation[1] = self.translation[0]+wx+100,self.translation[1]+wy+100 
                       drink.rotation = self.rotation 
                       widget.parent.add_widget(drink,drink.layer,'cur')
                       self.move = False
                                        
                    if key == "back":
                     self.parent.layers[self.layer].remove(self)
                     self.principal.translation[0], self.principal.translation[1] = self.translation[0],self.translation[1] 
                     self.principal.rotation = self.rotation
                     self.principal.zoom = self.zoom
                     self.move = True
                     self.parent.layers[self.principal.layer].append(self.principal)
                     return True
        
        if not self.collidePoint(x,y):
            return False

#        
        if len(self.touchDict) == 1:
                    print 'rotated'
                    self.rotation +=180
                    self._oldrotation +=180
                    
        if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):
        if self.move:                
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                        self.zoom = distNew/distOld * self._zoom
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
        if self.move:
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()         

class ReciveDrink(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,principal = None):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)

        self.principal = principal 
        
        self.posW = size[0]*0.18*0.685
        self.posO = size[0]*0.325*0.7
        
        self.move = True
        
        
        e = self.posO

        beer  = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="1" )
        drink = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="2")
        wine = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-2*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="3")
        coke = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-3*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="4" )
        coffe = ImageWidget(id=self.id,image_src="images/mselecao.png",parent=parent,pos=(-size[0]*0.375,self.posO-4*self.posW), size=(size[0]*0.0750,size[1]*0.0750),alfa = 1.0,layer=9 ,string="5")
        back = ImageWidget(id=self.id,image_src="images/cback.png",parent=parent,pos=(-size[0]*0.375,self.posO-5*self.posW), size=(size[0]*0.1,size[1]*0.1),alfa = 1.0,layer=layer )
        
        self.widgets =  {"1":beer,
                                "2":drink,
                                "3":wine,
                                "4":coke,
                                "5":coffe,
                                "back":back}#{"m1":m1,"m2":m2,"m3":m3,"m4":m4,"m5":m5,"m6":m6,"m7":m7,"z2":b1}
        
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius        

    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()
        
        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        
             
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if widget.layer == 9:
                        
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)                                                                                                                                    # Terceiro Slot do BILL                                               
                       beer = ImageWidget(id=self.id,image_src="images/cartinha_selecao.png",parent=self.parent,pos=(widget.x,widget.y), size=(widget.height*3,widget.width*3),alfa = 1.0,layer=self.layer+4,string=widget.string )
                       beer.translation[0], beer.translation[1] = self.translation[0]+wx+100,self.translation[1]+wy+100 
                       beer.rotation = self.rotation + 180
                       widget.parent.add_widget(beer,beer.layer,'cur')
                       self.move = False
                                        
                    if key == "back":
                     self.parent.layers[self.layer].remove(self)
                     self.principal.translation[0], self.principal.translation[1] = self.translation[0],self.translation[1] 
                     self.principal.rotation = self.rotation
                     self.principal.zoom = self.zoom
                     self.principal.move = True
                     #self.parent.layers[self.principal.layer].append(self.principal)
                     return True
                    # widget.alfa -=0.1          
        
        if not self.collidePoint(x,y):
            return False

        if self.move: 
        
            if len(self.touchDict) == 1:
                    print 'rotated'
            #        self.rotation +=180
                    self._oldrotation +=180
                    
            if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


            self.parent.layers[self.layer].remove(self)
            self.parent.layers[self.layer].append(self)
            self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):         
        if self.move:       
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                                                
                        self.zoom = distNew/distOld * self._zoom
                        
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5
                        
                
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
        if self.move:
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()      
class PerfilBar(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,perfil=[]):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)
        
        self.perfil = perfil

        if perfil == []:
            sex="m" 
            name="Guest" 
            age="21"
            status="on"
            photo="images/mulher1.png"
        else:
            name= perfil[2]
            age= perfil[3] 
            sex=perfil[4]
            status=perfil[5]
            photo=perfil[6]        
        
        
        if sex == "m":
            s = ImageWidget(id=self.id,image_src="images/simbolo_homem.png",parent=parent,pos=(-size[0]*0.30*0.65,size[1]*0.65*0.65), size=((size[0]*0.05*scale),(size[0]*0.05*scale) ),alfa = 1.0,layer=layer )    
        else:    
            s = ImageWidget(id=self.id,image_src="images/simbolo_feminino.png",parent=parent,pos=(-size[0]*0.30*0.65,size[1]*0.65*0.65), size=((size[0]*0.06*scale),(size[0]*0.06*scale) ),alfa = 1.0,layer=layer )
#        if status == "mark_on":
        if len(perfil) == 0:
         self.st = ImageWidget(id=self.id,image_src="images/estrela_apagada.png" ,parent=parent,pos=(0,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
        else:
            print perfil[1] ,"client"
            print self.parent.obj[self.id][1].ficha[7] , "eu"
            if  perfil[1] in self.parent.obj[self.id][1].ficha[7]:

                 if    self.parent.obj[self.id][1].ficha[1] in perfil[7]:         
                        self.st = ImageWidget(id=self.id,image_src="images/estrela_marcado_acesa.png" ,parent=parent,pos=(0,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
                 else:
                        self.st = ImageWidget(id=self.id,image_src="images/estrela_acesa.png" ,parent=parent,pos=(0,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
            else:
                 if    self.parent.obj[self.id][1].ficha[1] in perfil[7]:         
                        self.st = ImageWidget(id=self.id,image_src="images/estrela_marcado_apagada.png" ,parent=parent,pos=(0,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
                 else:
                        self.st = ImageWidget(id=self.id,image_src="images/estrela_apagada.png" ,parent=parent,pos=(0,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
            
        photo = ImageWidget(id=self.id,image_src=photo,parent=parent,pos=(0,size[0]*0.1), size=((scale*size[0]*0.25),(scale*size[1]*0.25) ),alfa = 1.0 ,layer=layer)            
        
        
        s_mark_on = ImageWidget(id=self.id,image_src="images/estrela_acesa.png"       ,parent=parent,pos=(size[0]*0.50,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
        s_mark_off      = ImageWidget(id=self.id,image_src="images/estrela_apagada.png"      ,parent=parent,pos=(size[0]*0.50,size[1]*0.5*0.0), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
        s_mark = ImageWidget(id=self.id,image_src="images/estrela_marcado_acesa.png" ,parent=parent,pos=(size[0]*0.50,size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )

        self.status = {"images/estrela_acesa.png" :s_mark_on,"images/estrela_apagada.png" :s_mark_off}
        
        self.status_show = False 
                        
        n = pyglet.text.Label(name ,font_size=size[0]*0.065,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
        a = pyglet.text.Label(age ,font_size=size[0]*0.035,color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
        
        self.widgets ={"photo":photo,"sex":s,"status":self.st}
        self.labels = [n,a]
             
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False

                 
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget()
        glPopMatrix()

        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        
        if self.status_show:    
            for widget in self.status.itervalues():
                glPushMatrix()
                glTranslatef(widget.x*self.zoom,widget.y*self.zoom, 0)
                widget.drawSelf()#_widget()
                glPopMatrix()            
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)             
        self.labels[0].x = -self.width*0.15
        self.labels[0].y = +self.height*0.40
        self.labels[0].draw()
        
        self.labels[1].x = self.width*0.15 
        self.labels[1].y = self.height*0.40
        self.labels[1].draw()
        glPopMatrix()
        
    def draw_widget(self):

        glPushAttrib(GL_ALL_ATTRIB_BITS)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for widget in self.widgets.itervalues():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
            
        
        
    def on_touch_down(self, touches, touchID, x, y):

        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
#                    if key == "sex":#widget.alfa -=0.1
#                        self.parent.layers[self.layer].remove(self)
#                        return True
                    if key == "status": 
                        print self.parent.obj[ self.id  ][1].ficha[7] ,"minhas ficha antes"
                        if self.widgets["status"].image == "images/estrela_apagada.png": 
                               self.widgets["status"] = ImageWidget(id=self.id,image_src="images/estrela_acesa.png" ,parent=widget.parent,pos=(self.widgets["status"] .x,self.widgets["status"] .y), size=(self.widgets["status"] .height,self.widgets["status"] .width ),alfa = 1.0,layer=widget.layer )

                               self.parent.obj[ self.perfil[1]  ][1].drinks = True
                               self.parent.obj[ self.perfil[1]  ][1].menumarked = MenuMarked("images/fundo_mark.png", parent=self.parent,   pos=(0,0), size=(200,200), layer=2,photoname=self.parent.obj[self.id][1].photoname)
                               self.parent.obj[ self.perfil[1]  ][1].alert = {"carta":[False,self.parent.obj[ self.perfil[1]  ][1].carta],"drink":[False,self.parent.obj[ self.perfil[1]  ][1].drink],"mark":[True,self.parent.obj[ self.perfil[1]  ][1].mark]}
                               if   self.perfil[1] not  in  self.parent.obj[ self.id  ][1].ficha[7]:
                                   self.parent.obj[ self.id  ][1].ficha[7].append(self.perfil[1])
                                                                       
                        elif self.widgets["status"].image == "images/estrela_acesa.png": 
                               self.widgets["status"] = ImageWidget(id=self.id,image_src="images/estrela_apagada.png" ,parent=widget.parent,pos=(self.widgets["status"] .x,self.widgets["status"] .y), size=(self.widgets["status"] .height,self.widgets["status"] .width ),alfa = 1.0,layer=widget.layer )
                               if   self.perfil[1] in  self.parent.obj[ self.id  ][1].ficha[7]:
                                   self.parent.obj[ self.id  ][1].ficha[7].remove(self.perfil[1])
                               
                        elif self.widgets["status"].image == "images/estrela_marcado_acesa.png": 
                               self.widgets["status"] = ImageWidget(id=self.id,image_src="images/estrela_marcado_apagada.png" ,parent=widget.parent,pos=(self.widgets["status"] .x,self.widgets["status"] .y), size=(self.widgets["status"] .height,self.widgets["status"] .width ),alfa = 1.0,layer=widget.layer )
                               if   self.perfil[1] in  self.parent.obj[ self.id  ][1].ficha[7]:
                                   self.parent.obj[ self.id  ][1].ficha[7].remove(self.perfil[1])

                        elif self.widgets["status"].image == "images/estrela_marcado_apagada.png":
                               self.parent.obj[ self.perfil[1]  ][1].drinks = True
                               self.parent.obj[ self.perfil[1]  ][1].menumarked = MenuMarked("images/fundo_mark.png", parent=self.parent,   pos=(0,0), size=(200,200), layer=2,photoname=self.parent.obj[self.id][1].photoname)
                               self.parent.obj[ self.perfil[1]  ][1].alert = {"carta":[False,self.parent.obj[ self.perfil[1]  ][1].carta],"drink":[False,self.parent.obj[ self.perfil[1]  ][1].drink],"mark":[True,self.parent.obj[ self.perfil[1]  ][1].mark]}
                               if   self.perfil[1] not in  self.parent.obj[ self.id  ][1].ficha[7]: 
                                   self.parent.obj[ self.id  ][1].ficha[7].append(self.perfil[1])
                               self.widgets["status"] = ImageWidget(id=self.id,image_src="images/estrela_marcado_acesa.png" ,parent=widget.parent,pos=(self.widgets["status"] .x,self.widgets["status"] .y), size=(self.widgets["status"] .height,self.widgets["status"] .width ),alfa = 1.0,layer=widget.layer )
                               
                        else:
                            pass
                        print self.parent.obj[ self.id  ][1].ficha[7] ,"minhas ficha depois"              
#        if self.status_show:
#            for (key,widget) in self.status.iteritems():  
#               if self.collidePointButton(x, y,widget):
#                    print key
#                    self.widgets["status"] = ImageWidget(id=self.id,image_src=key ,parent=widget.parent,pos=(self.widgets["status"] .x,self.widgets["status"] .y), size=(self.widgets["status"] .height,self.widgets["status"] .width ),alfa = 1.0,layer=widget.layer )
#                    self.status_show = False
                    
        if not self.collidePoint(x,y):
            return False
        
        if len(self.touchDict) == 1:
                    print 'rotated'
                    #self.rotation +=180
                    self._oldrotation +=180
                    
        if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v


        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()                              
         
                  
        return True
                        
    def on_touch_move(self, touches, touchID, x, y):       
        
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                        self.translation = Vector(x,y) - self.original_points[0] + self._translation
                        
                        for (key,widget) in self.widgets.iteritems():             
                            if self.collidePointButton(x, y,widget):
                                if key == "sex":#widget.alfa -=0.1
                                    self.parent.layers[self.layer].remove(self)
                                    self.parent.layers[self.layer-4][0].move = True
                        return True        
                                            
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                        
                        self.zoom = distNew/distOld * self._zoom
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5                
                        #translate
#                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
#                        self.newCenter = points[0] + (points[1] - points[0])*0.5
#                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()       



                                
class Perfil(ImageWidget):
    def __init__(self, image_src,id=0, parent=None,  pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,layer=0,sex="M",name="Guest",age="21",status="on",photo="images/foto_mulher.png"):
        
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)
        
        if sex == "m":
            s = ImageWidget(id=self.id,image_src="images/simbolo_homem.png",parent=parent,pos=(-size[0]*0.50*0.55,size[1]*0.5*0.65), size=((size[0]*0.07*scale),(size[0]*0.07*scale) ),alfa = 1.0,layer=layer )    
        else:    
            s = ImageWidget(id=self.id,image_src="images/simbolo_feminino.png",parent=parent,pos=(-size[0]*0.50*0.55,size[1]*0.5*0.65), size=((size[0]*0.07*scale),(size[0]*0.07*scale) ),alfa = 1.0,layer=layer )
         
        if status == "on":
             st = ImageWidget(id=self.id,image_src="images/status_on.png",parent=parent,pos=(size[0]*0.50*0.45,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
        elif status == "off":
             st = ImageWidget(id=self.id,image_src="images/status_off.png",parent=parent,pos=(size[0]*0.50*0.45,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )             
        else:        
            st = ImageWidget(id=self.id,image_src="images/status_yellow.png",parent=parent,pos=(size[0]*0.50*0.45,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
        
        photo = ImageWidget(id=self.id,image_src=photo,parent=parent,pos=(0,-size[0]*0.5*0.2), size=((scale*size[0]*0.35),(scale*size[1]*0.35) ),alfa = 1.0 ,layer=layer)
        
        
        s_on = ImageWidget(id=self.id,image_src="images/status_on.png"       ,parent=parent,pos=(size[0]*0.50,-size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
        s_off      = ImageWidget(id=self.id,image_src="images/status_off.png"      ,parent=parent,pos=(size[0]*0.50,size[1]*0.5*0.0), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )
        s_yellow = ImageWidget(id=self.id,image_src="images/status_yellow.png" ,parent=parent,pos=(size[0]*0.50,size[1]*0.5*0.55), size=((size[0]*0.1*scale),(size[0]*0.1*scale) ),alfa = 1.0,layer=layer )

        self.status = {"images/status_on.png" :s_on,"images/status_off.png":s_off,"images/status_yellow.png" :s_yellow}
        
        self.status_show = False
                        
        n = pyglet.text.Label(name ,font_size=size[0]*0.1,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
        a = pyglet.text.Label(age ,font_size=size[0]*0.075,color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
        
        self.widgets ={"photo":photo,"sex":s,"status":st}
        self.labels = [n,a]

        self.gesture = []
             
        glBindTexture(self.texture.target, self.texture.id)   
        self.x,self.y = pos
        self.acceleration = 5.0
        self.direction = Vector(0.0,0.0)

    def Animate(self,dt):
                print self.translation , self.direction,"zoom"
                if self.velocity > 0.0:
                    pyglet.clock.schedule_once(self.Animate,1.0/60.0)
                    self.velocity -=  0.5
                    self.translation += self.direction*1.1
                else:
                  self.velocity = 5.0   
            
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
    def collidePointButton(self, x,y,widget):
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            if radius >= dist:
              return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)
        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget()
        glPopMatrix()

        langs = self.widgets.keys()
        langs.sort()
    
        for key in langs:
            glPushMatrix()
            glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
            self.widgets[key].drawSelf()#_widget()
            glPopMatrix()
        
        if self.status_show:    
            for widget in self.status.itervalues():
                glPushMatrix()
                glTranslatef(widget.x*self.zoom,widget.y*self.zoom, 0)
                widget.drawSelf()#_widget()
                glPopMatrix()            
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1] , 0)
        glRotatef(self.rotation , 0, 0, 1)  
        glScalef(self.zoom, self.zoom, 1)         
        self.labels[0].x = -self.width*0.195
        self.labels[0].y = +self.height*0.30
        self.labels[0].draw()
        
        self.labels[1].x = self.width*0.215 
        self.labels[1].y = self.height*0.30
        self.labels[1].draw()
        glPopMatrix()
        
    def draw_widget(self):

        glPushAttrib(GL_ALL_ATTRIB_BITS)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
        
    def update(self):
        
        for widget in self.widgets.itervalues():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter
        

    def on_touch_down(self, touches, touchID, x, y):
        self.direction = Vector(x,y)
        print self.gesture
                    
        
        for (key,widget) in self.widgets.iteritems():             
             if self.collidePointButton(x, y,widget):
                    if key == "status":
                        self.status_show = True         
       
        if self.status_show:
            for (key,widget) in self.status.iteritems():  
               if self.collidePointButton(x, y,widget):

                    self.widgets["status"] = ImageWidget(id=self.id,image_src=key ,parent=widget.parent,pos=(self.widgets["status"] .x,self.widgets["status"] .y), size=(self.widgets["status"] .height,self.widgets["status"] .width ),alfa = 1.0,layer=widget.layer )
                    if key == "images/status_off.png":
                        self.parent.obj[self.id][1].widgets["afundo"] =  ImageWidget(id=self.id,image_src="images/vermelho.png",parent=self.parent, pos=(0,0), size=(self.parent.obj[self.id][1].widgets["afundo"].height,self.parent.obj[self.id][1].widgets["afundo"].width),alfa = 1.0,layer= self.parent.obj[self.id][1].widgets["afundo"].layer )
                        self.parent.clients[self.id][5] = "off"
                        #self.parent.obj[self.id][1].client[self.id][5] = "off"
                    if key == "images/status_on.png":
                        self.parent.obj[self.id][1].widgets["afundo"] =  ImageWidget(id=self.id,image_src="images/verde.png",parent=self.parent, pos=(0,0), size=(self.parent.obj[self.id][1].widgets["afundo"].height,self.parent.obj[self.id][1].widgets["afundo"].width),alfa = 1.0,layer= self.parent.obj[self.id][1].widgets["afundo"].layer )
                        self.parent.clients[self.id][5] = "on"
                        #self.parent.obj[self.id][1].client[self.id][5] = "on"
                    if key == "images/status_yellow.png":
                        self.parent.obj[self.id][1].widgets["afundo"] =  ImageWidget(id=self.id,image_src="images/amarelo.png",parent=self.parent, pos=(0,0), size=(self.parent.obj[self.id][1].widgets["afundo"].height,self.parent.obj[self.id][1].widgets["afundo"].width),alfa = 1.0,layer= self.parent.obj[self.id][1].widgets["afundo"].layer )
                        self.parent.clients[self.id][5] = "yellow"
                        #self.parent.obj[self.id][1].client[self.id][5] = "yellow"                                                
                    self.status_show = False
                    # COM REDE
                    #osc.sendMsg("/tuio/Set", self.parent.obj[self.id][1].client[self.id],self.parent.obj[self.id][1].server_host,self.parent.obj[self.id][1].server_port)
        if not self.collidePoint(x,y):
            return False
        
        if touchID not in self.gesture:
            self.gesture.append(touchID)
            
          
                         
        if len(self.touchDict) == 1:
                    print 'rotated'
                    # aqui so pra rotacionar
                    #self.rotation +=180
                    self._oldrotation +=180
#                    
        if len(self.touchDict) < 2:
                         
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v
#            
        self.parent.layers[self.layer].remove(self)
        self.parent.layers[self.layer].append(self)
        self.update()      
                                
#                  
        return True
#                        
    def on_touch_move(self, touches, touchID, x, y):
                        
                if len(self.touchDict) == 1 and touchID in self.touchDict:
                   self.translation = Vector(x,y) - self.original_points[0] + self._translation
                   for (key,widget) in self.widgets.iteritems():             
                       if self.collidePointButton(x, y,widget):
                          if key == "sex":#widget.alfa -=0.1
                            self.parent.layers[self.layer].remove(self)
			    if len(self.parent.layers[self.layer-3]) == 0:
				self.parent.obj[self.id][1].actived =  {"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}
                        
                   return True
                if len(self.touchDict) == 2 and touchID in self.touchDict:
                        points = self.touchDict.values()                       

                        #scale
                        distOld = Distance(self.original_points[0], self.original_points[1])
                        distNew = Distance(points[0], points[1])
                        self.zoom = distNew/distOld * self._zoom
                        if distNew/distOld * self._zoom > 2.0 or self.zoom < 0.5:
                            self.zoom = 2.0
                        if distNew/distOld * self._zoom < 0.5 :   
                            self.zoom = 0.5    
                        #comenta aqui para so rotacionar                 
                        #translate
                        self.originalCenter = self.original_points[0] + (self.original_points[1] - self.original_points[0])*0.5
                        self.newCenter = points[0] + (points[1] - points[0])*0.5
                        self.translation = (self.newCenter - self.originalCenter)  + self._translation
                       
                        #rotate
                        v1 = self.original_points[1] - self.original_points[0]
                        v2 = points[0] - points[1]
                        if((v1[0] < 0 and v2[0]>0) or (v1[0] > 0 and v2[0]<0)):
                            self._rotation =  ( 180+(self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                        else:
                            self._rotation =  ((self.getAngle(v1[0], v1[1]) - self.getAngle(v2[0], v2[1]))*-18)  %360
                       
                        self.rotation = (self._rotation + self._oldrotation) %360

                if touchID in self.touchDict:
                        self.touchDict[touchID] = Vector(x,y)
                self.update()       
                         
    def on_touch_up(self, touches, touchID, x, y):
                self.direction = Vector(x,y) - self.direction  
                self.direction = Normalize(self.direction)
#                pyglet.clock.schedule_once(self.Animate,1.0/60.0)        
                if touchID in self.gesture:
                    self.gesture.remove(touchID)
                    
#                if len(self.gesture) > 2:
#                    print "oi"
#                    self.gesture = []
#                    self.update()
#                    self.parent.layers[self.layer].remove(self)
#                    return False
                            
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.update()       


                
class PerfilWidget(ImageWidget):
    def __init__(self, image_src, id=0,parent=None,pos=(0,0), size=(1,1), scale = 1.0,alfa = 0.5,layer=0,address=("127.0.0.2",40002),sex="m",name="Guest",age="21",status="on",photo="images/mulher1.png",photoname=""):
        ImageWidget.__init__(self,image_src,id, parent, pos, size,scale,alfa,layer)
        self.pos = self.layer*12+4   
        
        self.layerMapa = self.pos
        self.layerBill = self.pos + 1
        self.layerMenu = self.pos +2
        self.layerPerfil = self.pos + 3
        
        self.center = (0,0)
        
        self.typemsg = {}
        
        self.visible = False
        self.x,self.y = pos        

        self.cont = 0
        self.posi = 1
        self.name = name
        self.sex = sex
        self.age= age
        self.status =status
        self.photo = photo
        self.photoname = photoname
        
        if status == "on":
            img_src= "images/verde.png"
        elif status == "off":
            img_src= "images/vermelho.png"
        else:
            img_src= "images/amarelo.png"
                    
        fundo =  ImageWidget(id=self.id,image_src=img_src,parent=parent, pos=(0,0), size=size,alfa = 1.0,layer= self.layer )
        
        
        net =                       ImageWidget(id=self.id,image_src="images/net.png",parent=parent, pos=(45,120), size=((70),(70) ),alfa = 1.0,layer=self.layerMapa )
        bill =               ImageWidget(id=self.id,image_src="images/bill.png",parent=parent, pos=(-45,120), size=((70),(70) ),alfa = 1.0 ,layer=self.layerBill)
        menu =                    ImageWidget(id=self.id,image_src="images/menu.png",parent=parent, pos=(-112,65), size=((70),(70) ),alfa = 1.0 ,layer=self.layerMenu)
        profile=                       ImageWidget(id=self.id,image_src="images/profile.png",parent=parent, pos=(112,65), size=((70),(70) ),alfa = 1.0,layer= self.layerPerfil )
        
        self.li = [fundo,profile,net,bill, menu,bill,net]
        self.w = fundo
        
        #pyglet.clock.schedule(self.animate,fundo)

        
        self.carta =  ImageWidget(id=self.id,image_src="images/msgcarta.png",parent=parent, pos=(-140,0), size=((70),(70) ),alfa = 1.0 ,layer=self.layer)
        self.carta.rotation = 180
        self.drink = ImageWidget(id=self.id,image_src="images/msgdrink.png",parent=parent, pos=(-140,0), size=((70),(70) ),alfa = 1.0 ,layer=self.layer)
        self.drink.rotation = 180 
        self.mark = ImageWidget(id=self.id,image_src="images/msgmark.png",parent=parent, pos=(-140,0), size=((70),(70) ),alfa = 1.0 ,layer=self.layer)
        self.mark.rotation = 180 
        alert = ImageWidget(id=self.id,image_src="images/particle.png",parent=parent, pos=(-140,0), size=((70),(70) ),alfa = 1.0 ,layer=self.layer)
        
        self.widgets ={"afundo":fundo,"profile":profile,"net":net,"bill":bill,"menu":menu,"alert":alert}
        
        self.alert = {"carta":[False,self.carta],"drink":[False,self.drink],"mark":[False,self.mark]}
        
        self.alerts = True
        
        self.actived ={"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}
        

        self.message = ImageWidget(id=self.id,image_src="images/himarcio.png",parent=parent, pos=(-140,0), size=((150),(150) ),alfa = 1.0 ,layer=self.layer+2) 
        self.coquetel = ImageWidget(id=self.id,image_src="images/himarcio.png",parent=parent, pos=(-140,0), size=((100),(100) ),alfa = 1.0 ,layer=self.layer+2)
        self.marcado = ImageWidget(id=self.id,image_src="images/himarcio.png",parent=parent, pos=(-140,0), size=((100),(100) ),alfa = 1.0 ,layer=self.layer+2)
        
        self.drinkoffer = MenuDrinkOffer("images/drink_back.png", parent=self.parent,   pos=(0,0), size=(200,200), layer=2)
        self.menumarked = MenuMarked("images/fundo_mark.png", parent=self.parent,  pos=(0,0), size=(200,200), layer=2)
        self.canvas = PaintWidget("images/text.png",parent=self.parent, pos=(0,0), size=(500,600),layer=2,file =str(self.id) )
        self.menumessage = MenuMenssageBar("images/hi_background.png", parent=self.parent,  pos=(0,0), size=(200,200), layer=2)
        
        self.mapa = MapaBar(id=self.id,image_src="images/fundo_partes_fixas.png",parent=parent, pos=(0,0), size=((scale*200),(scale*200) ),alfa = 1.0 ,layer=self.layerMapa)
        self.bill  = Bill(id=self.id,image_src="images/comanda_fundo.png",parent=parent, pos=(0,0), size=((scale*200),(scale*200) ),alfa = 1.0 ,layer=self.layerBill,name=name)        
        self.menu = Menu(id=self.id,image_src="images/cardapio_base.png",parent=parent, pos=(0,0), size=((scale*150),(scale*150) ),alfa = 1.0 ,layer=self.layerMenu)
        self.perfil = Perfil(id=self.id,image_src="images/background_perfil3.png",parent=parent, size=((scale*100),(scale*100) ),scale=scale,alfa = 1.0,layer = self.layerPerfil,sex=sex,name=name,age=age,status=status,photo=photo)#PerfilBar("images/background_perfil_bar.png",parent=parent, size=((scale*100),(scale*100) ),scale=scale,alfa = 1.0,layer = 4,sex=sex,name=name,age=age,status=status,photo=photo)          
         
         
        self.rot = {fundo.layer:0,profile.layer:-60,net.layer:-20,bill.layer:20,menu.layer:60,self.layer:0}
       
        
        """ { port : [ ip,name,sex,age,status,marrk_me,marked ] }  """
                      
        server, client = address

        self.client_host = str(address[0])
        self.client_port = int(address[1])
        
        self.server_host = str('127.0.0.1')
        self.server_port = int(30001)                     

        self.client ={}
        self.ficha = [self.client_host,self.client_port,name,age,sex,status,photo,[],"images/"]
#    COM REDE  ---- 
        
        osc.init()
        print self.client_host,self.client_port
        
        osc.listen(self.client_host,self.client_port)

#        osc.bind(self.getClients,"/tuio/Set")
        osc.bind(self.send, "/tuio/msg")         
#        
#        osc.sendMsg("/tuio/Set", [self.client_host,self.client_port,name,age,sex,status,photo,"40003"],self.server_host,self.server_port)
#        self.client[self.client_port] =  [self.client_host,self.client_port,name,age,sex,status,photo,"40003"]
                    
        glBindTexture(self.texture.target, self.texture.id)   

    def getClients(self,*msg):
         
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
#        if len(msg) > 0:
#            print msg[0], "passou"
#            if msg[0][2] == "msg":
#                        s.bind((self.client_host,self.client_port+1000))
#                        s.listen(1)                
#                        print "Aceitando a conexao..."
#                        conn,addr= s.accept()
#                         
#                        print "recebendo o arquivo..."
#                        photo = 'msg.react'
#                        
#                        arq = open(photo,'wb')
#                          
#                        while 1:
#                         
#                             dados=conn.recv(1024)
#                             if not dados:
#                                  break
#                             arq.write(dados)
#                         
#                        print "saindo..."
#                
#                        arq.close()
#                        conn.close()        
#                        s.close()    
#                        
#                        pkl_file = open('msg.react', 'rb')
#                        
#                        data1 = pickle.load(pkl_file)
#                        
#                        pkl_file.close()
#                                
#                        m = data1
#                
#                        print  m
#
#                        print self.name,self.id, " recebi mensagem de " , msg[0][2], msg[0][3]
#                        self.msg = True                
#                        return


        s.bind((self.client_host,self.client_port+500))
        s.listen(1)
             
        print "Aceitando a conexao..."
        conn,addr= s.accept()
         
        print "recebendo o arquivo..."
        photo = 'data.react'
        
        arq = open(photo,'wb')
          
        while 1:
         
             dados=conn.recv(1024)
             if not dados:
                  break
             arq.write(dados)
         
        print "saindo..."

        arq.close()
        conn.close()        
        s.close()    
        
        pkl_file = open('data.react', 'rb')
        
        data1 = pickle.load(pkl_file)
        
        pkl_file.close()
                
        self.client = data1

        print  self.client
        

               
    def send(self,*msg):
        
               
        """deals with "print" tagged OSC addresses """
        print "printing in the printStuff function ", msg
        print "the oscaddress is ", msg[0][0]
        
        print "the value is ", msg[0][2]
        print "the value is ", msg[0][3]
#        print "the value is ", msg[0][4]
#        print "the value is ", msg[0][5]

        print self.name,self.id, " recebi mensagem de " , msg[0][2], msg[0][3]
        
        if msg[0][2] == "msg":
            self.typemsg[msg[0][3]] = "msg"

        elif msg[0][2] == "drink":
            self.typemsg[msg[0][3]] ="drink"
            
        elif msg[0][2] == "mark":   
             self.typemsg[msg[0][3]] ="mark" 
        else:
            pass                
                       
#        for i in self.client.itervalues():
#            osc.sendMsg("/tuio/Get", i, msg[0][2], msg[0][3])
#            time.sleep(0.25)
#        print self.name,self.id, " recebi mensagem de " , msg[0][2], msg[0][3]              
#        self.client[msg[0][3]] = []
#        
#        for i in range(2,len(msg[0])):
#            self.client[msg[0][3]].append(msg[0][i])
#        #print self.client, "eu recebi isso "  , self.client_port                 
#        output = open('msg.react', 'wb')
#        
#        # Pickle dictionary using protocol 0.
#        pickle.dump(msg, output)
#        
#        # Pickle the list using the highest protocol available.
#        
#        output.close()        
#        
#        
#        host = str(msg[4])
#        print host
#        port = int(msg[5])+1000
#        print port 
#        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         
#        print "conectando com servidor..."
#        s.connect((host,port))
#         
#        print "abrindo arquivo..."
#        
#        arq=open('msg.react','rb')
#         
#        print "enviado  arquivo"
#        for i in arq.readlines():
#            s.send(i)
#         
#        print "saindo..."
#        arq.close()
#        s.close() 
             
    def radius(self):
            
            radius = sqrt(self.width*self.width*0.10 + self.height*self.height*0.10)/3 *self.zoom
            return radius
             
    def collidePointButton(self, x,y,widget):

  
            wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
            wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
            
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom
                
            dist = Length(Vector(self.translation[0]+wx*self.zoom,self.translation[1]+wy*self.zoom) - Vector(x,y))
            
            if radius >= dist:
               return True
            else:
              return False
          
    def animateWidget(self,dt,w):
                print w.alfa , "zoom"
                if w.alfa < 1.0:
                    pyglet.clock.schedule_once(self.animateWidget,w=w,delay=1.0/60.0)
                    w.alfa += w.alfaC
                    if w.alfa > 1.0:
                        w.alfaC *= -1 
                else:
                  w.cont += 1
                  if w.cont > 2:   
                    w.alfa = 1.0
                                        
    def animate(self,dt):
                
                print self.w.zoom , "zoom"
                if self.w.zoom < 2.0:
                    pyglet.clock.schedule_once(self.animate,1.0/60.0)
                    self.w.zoom += self.w.zoomC
                else:
                  self.w.zoom = 1.0                 
                

            
    def draw(self):
     self.actived["alert"] = False  
     

     for (key,w) in self.typemsg.iteritems(): 
        if w == "msg":
            print "FELIPE"
            self.menumessage = MenuMenssageBar("images/hi_background.png", parent=self.parent,   pos=(0,0), size=(200,200), layer=2,photoname=self.parent.obj[int(key)][1].photoname)
            self.alert = {"carta":[True,self.carta],"drink":[False,self.drink],"mark":[False,self.mark]}
#            pyglet.clock.schedule_once(self.animateWidget,w=self.carta,delay=1.0/60.0)
            del self.typemsg[key]
            break
            print self.alert

        elif w == "drink":
            self.drinkoffer = MenuDrinkOffer("images/drink_back.png", parent=self.parent,   pos=(0,0), size=(200,200), layer=2,photoname=self.parent.obj[int(key)][1].photoname)
#            pyglet.clock.schedule_once(self.animateWidget,w=self.drink,delay=1.0/60.0)
            self.alert = {"carta":[False,self.carta],"drink":[True,self.drink],"mark":[False,self.mark]}
            del self.typemsg[key]
            break
        elif w == "mark":   
             self.menumarked = MenuMarked("images/fundo_mark.png", parent=self.parent,   pos=(0,0), size=(200,200), layer=2,photoname=self.parent.obj[int(key)][1].photoname)
             self.alert = {"carta":[False,self.carta],"drink":[False,self.drink],"mark":[True,self.mark]}
#             pyglet.clock.schedule_once(self.animateWidget,w=self.mark,delay=1.0/60.0)
             if   self.id not  in  self.parent.obj[int(key)][1].ficha[7]:
                  self.parent.obj[int(key)][1].ficha[7].append(self.ficha[1])  
             del self.typemsg[key]
             break                           
        else:
            pass       
     
     if self.visible: 
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], 0)
        glRotatef(self.rotation , 0, 0, 1)

        glPushMatrix()
        glScalef(self.zoom, self.zoom, 1)
        glScalef(self.width, self.height, 1)
        self.draw_widget(self.x,self.y)
        glPopMatrix()    
        langs = self.widgets.keys()
        langs.sort()

        for (key,widget) in self.alert.iteritems():
            if widget[0]:
                glPushMatrix()
                glTranslatef(widget[1].x*self.zoom,widget[1].y*self.zoom, 0)
                glRotatef(widget[1].rotation, 0, 0, 1)
                widget[1].drawSelf()#_widget()
                glPopMatrix()

                 
        for key in langs:
            if self.actived[key]:
                glPushMatrix()
                glTranslatef(self.widgets[key].x*self.zoom,self.widgets[key].y*self.zoom, 0)
                glRotatef(self.rot[self.widgets[key].layer]+180, 0, 0, 1)
                self.widgets[key].drawSelf()#_widget()
                glPopMatrix()
     
        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        
        glPopAttrib()
      
        
    def update(self):
        
        for (key,widget) in self.widgets.iteritems():
            widget.rotation     =       self.rotation   
            widget.translation =        self.translation  
            widget.zoom =        self.zoom  
    
            widget.touchDict =  self.touchDict                
            widget.original_points =        self.original_points
            widget.originalCenter =        self.originalCenter  
            widget.newCenter =       self.newCenter

    def on_touch_down(self, touches, touchID, x, y):  
        for (key,widget) in self.widgets.iteritems():
            if self.collidePointButton(x, y,widget):
                     
                    if key == "alert" :
                        
                        if self.alert["carta"][0]:
                          self.alert = {"carta":[False,self.carta],"drink":[False,self.drink],"mark":[False,self.mark]}
                          #self.parent.add_widget(self.menumarked,self.menumarked.layer,'cur')
                          wx = self.alert["carta"][1].x*cos(self.rotation/180*pi)  - self.alert["carta"][1].y *sin(self.rotation/180*pi)
                          wy = self.alert["carta"][1].y *cos(self.rotation/180*pi) + self.alert["carta"][1].x* sin(self.rotation/180*pi)
                          
                          self.menumessage.translation[0], self.menumessage.translation[1] = self.translation[0]+wx,self.translation[1]+wy
                          self.parent.add_widget(self.menumessage,self.menumessage.layer,'cur')

#                          self.canvas.x, self.canvas.y = self.center[0]+50,self.center[1]
#                          self.parent.add_widget(self.canvas,self.canvas.layer,'cur')  
                            
                        elif self.alert["drink"][0]:
                           self.alert = {"carta":[False,self.carta],"drink":[False,self.drink],"mark":[False,self.mark]}
                           #self.parent.add_widget(self.menumarked,self.menumarked.layer,'cur')
                           wx = self.alert["carta"][1].x*cos(self.rotation/180*pi)  - self.alert["carta"][1].y *sin(self.rotation/180*pi)
                           wy = self.alert["carta"][1].y *cos(self.rotation/180*pi) + self.alert["carta"][1].x* sin(self.rotation/180*pi)
                           self.drinkoffer.translation[0], self.drinkoffer.translation[1] = self.translation[0]+wx,self.translation[1]+wy
                           self.parent.add_widget(self.drinkoffer,self.drinkoffer.layer,'cur')  
                           
                        elif self.alert["mark"][0]:
                           self.alert = {"carta":[False,self.carta],"drink":[False,self.drink],"mark":[False,self.mark]}
                           wx = self.alert["carta"][1].x*cos(self.rotation/180*pi)  - self.alert["carta"][1].y *sin(self.rotation/180*pi)
                           wy = self.alert["carta"][1].y *cos(self.rotation/180*pi) + self.alert["carta"][1].x* sin(self.rotation/180*pi)
                           self.menumarked.translation[0], self.menumarked.translation[1] = self.translation[0]+wx,self.translation[1]+wy
                           self.parent.add_widget(self.menumarked,self.menumarked.layer,'cur')  
                        else  : 
                            self.alert = {"carta":[False,self.carta],"drink":[False,self.drink],"mark":[False,self.mark]}
                        
                    if widget.layer == self.layerMapa  and len(self.parent.layers[self.layerMapa]) == 0 and self.actived[key]:
                       self.actived ={"afundo":True,"profile":False,"net":True,"bill":False,"menu":False,"carta":True,"drink":True,"mark":True}
                       # COM REDE
                       #osc.sendMsg("/tuio/Get", [self.client_host,self.client_port,self.name,self.age,self.sex,self.status,self.photo,"33333"],self.server_host,self.server_port)
                       #self.getClients()
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
                       self.mapa.translation[0], self.mapa.translation[1] = self.translation[0]+wx,self.translation[1]+wy 
                       self.mapa.rotation = self.rotation+180
                       self.mapa.zoom = 1.0
                       widget.parent.add_widget(self.mapa,self.mapa.layer,'cur')

                    if widget.layer == self.layerBill and len(self.parent.layers[self.layerBill]) == 0 and self.actived[key]:
                       self.actived ={"afundo":True,"profile":False,"net":False,"bill":True,"menu":False,"carta":True,"drink":True,"mark":True}
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
                       self.bill.translation[0], self.bill.translation[1] = self.translation[0]+wx,self.translation[1]+wy 
                       self.bill.rotation  = self.rotation+180
                       self.bill.zoom = 1.0
                       widget.parent.add_widget(self.bill,self.bill.layer,'cur')     

                    if widget.layer == self.layerMenu and len(self.parent.layers[self.layerMenu]) == 0 and self.actived[key]:
                       self.actived ={"afundo":True,"profile":False,"net":False,"bill":False,"menu":True,"carta":True,"drink":True,"mark":True}
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
                       self.menu.translation[0], self.menu.translation[1] = self.translation[0]+wx,self.translation[1]+wy
                       self.menu.x,self.menu.y = wx,wy 
                       self.menu.rotation  = self.rotation+180
                       self.menu.zoom = 1.0
                       widget.parent.add_widget(self.menu,self.menu.layer,'cur')
                  
                    if widget.layer == self.layerPerfil and len(self.parent.layers[self.layerPerfil]) == 0 and self.actived[key]:
                       self.actived ={"afundo":True,"profile":True,"net":False,"bill":False,"menu":False,"carta":True,"drink":True,"mark":True}
                       wx = widget.x*cos(self.rotation/180*pi)  - widget.y *sin(self.rotation/180*pi)
                       wy = widget.y *cos(self.rotation/180*pi) + widget.x* sin(self.rotation/180*pi)
                       self.perfil.translation[0], self.perfil.translation[1] = self.translation[0]+wx,self.translation[1]+wy 
                       self.perfil.rotation = self.rotation+180
                       self.perfil.zoom = 1.0
                       self.perfil.gesture = []
                       widget.parent.add_widget(self.perfil,self.perfil.layer,'cur')
                                       

                    return True                      
    def on_object_down(self, touches, touchID,id, x, y,angle):
        self.center = (x,y)
        self.translation = Vector(x,y)
        self.rotation = -angle/pi*180
        self.visible = True
        self.state = ('dragging', touchID, x, y)
        self.update()
        return True
    def on_object_move(self, touches, touchID,id, x, y,angle):
        self.center = (x,y)
        if self.state[0] == 'dragging' and self.state[1]==touchID:
            self.rotation = -angle/pi*180
            self.translation += Vector (self.x + (x - self.state[2]) , self.y + y - self.state[3]) 
            self.state = ('dragging', touchID, x, y)
            self.update()
            return True
    def on_object_up(self, touches, touchID,id, x, y,angle):
        self.center = (10000,10000)
        if self.state[1] == touchID:
            self.rotation = -angle/pi*180
            self.visible = False 
            for i in range(self.pos,self.pos+12):
                    self.parent.layers[i] = []
            self.actived ={"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}        
            self.state = ('normal', None)
            self.update()
            return True   
        
        
class LineTool(ZoomableWidget):
    def __init__(self, pos=(0,0), size=(100,100)):
        ZoomableWidget.__init__(self, pos=pos, size=size)
    
            
            
    def draw_widget(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.7,0.7,0.7, 0.2)
        drawCircle((0,0), radius=0.5)
        glColor4f(0.4,0.7,0.4, 0.4)
        drawCircle((0,0), radius=0.3)
        glDisable(GL_BLEND)



class BarLooping(Container):
    def __init__(self, parent=None, layers=60):
        self.parent = parent
        self.layers = []
        self.obj = {}
        self.clients = {}
        self.circleX ,        self.circleY = 0 ,0
        
        self.buttonClean = ImageButton("images/opa.png",parent=c, pos=(0,0), size=(10,10))
        for i in range(layers):
                    self.layers.append([])

                    
    def add_widget(self,w, z=0,type='cur',id=0):
        if  type == 'cur':
          self.layers[z].append(w)
        elif type == 'obj':
            self.clients[w.client_port] = w.ficha
            self.obj[w.client_port] = [z,w,id]
            self.obj[w.client_port][1].layer = z
            self.obj[w.client_port][1].visible = False
            self.move = False
            self.touches = {}
    def draw(self):
                    
                       
                for l in range(0,3):
                    for w in self.layers[l]:
                            w.draw()
                # for (key1,w1) in self.obj.iteritems():
                          # for (key2,w2) in self.obj.iteritems():
                                # if  key1 != key2 and w1[1].visible and w2[1].visible:
                                    # glColor4f(1.0,1.0,1.0,0.5)
                                    # drawLine((w1[1].center[0],w1[1].center[1],w2[1].center[0],w2[1].center[1]))
                
                for (key,w) in self.obj.iteritems():
                         w[1].draw()   

                            
                for l in range(3,len(self.layers)):
                    for w in self.layers[l]:
                            w.draw()
#                if self.move:        
#            # self.buttonClean.draw()
#                     drawCircle(pos=( self.circleX , self.circleY), radius=20.0)
#                     drawCircle(pos=( self.circleX-30 , self.circleY,-30), radius=10.0)    
#                for (key1,w1) in self.obj.iteritems():
#                    for (key2,w2) in self.obj.iteritems():
#                        if   key1 == key2 :

                for  t in self.touches.values():
                    p = (t.xpos,t.ypos)
                    print p,"POOO"
                    glColor4f(0.8,0.2,0.2,0.5)
                    drawCircle(pos=p, radius=10)
                
                for (key,w) in self.obj.iteritems():
                    pos = w[0]*12 + 4

                    # MAPA
                    for i in self.layers[pos]:
                            if w[1].collideWidget(i):
                                self.layers[pos][0].move = True
                                self.layers[pos].remove(i)
                                if len(self.layers[pos+4]) > 0:   
                                    self.layers[pos+4] = []
                                # Menu Menssage,    
                                if len(self.layers[pos+4+1]) > 0:   
                                    self.layers[pos+4+1] = []
                                # Menu Mapa Drink    
                                if len(self.layers[pos+4+2]) > 0:   
                                    self.layers[pos+4+2] = []
                                # Fly Drink                                                                            
                                if len(self.layers[pos+8]) > 0:   
                                    self.layers[pos+8] = []
                                                                        
                                w[1].actived ={"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}
                    # MAPA
                    for i in self.layers[pos+4]:
                            if w[1].collideWidget(i):
                                self.layers[pos][0].move = True
                                self.layers[pos+4].remove(i)
                                
                    for i in self.layers[pos+1+4+4]:
                            if w[1].collideWidget(i):
                                if len(self.layers[pos+4+1]) > 0:   
                                    self.layers[pos+4+1][0].move = True
                                    self.layers[pos+1+4+4].remove(i)  
                    #MAPA  Msg Perfil
                    for i in self.layers[pos+1+4+4]:
                            if len(self.layers[pos+4]) > 0:
                                if self.layers[pos+4][0].collideWidget(i):
                                    if self.layers[pos+1+4+4][0].string == "1":
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].msg = True
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].menumessage = MenuMenssageBar("images/hi_background.png", parent=self.obj[ self.layers[pos+4][0].perfil[1]  ][1].parent,   pos=(0,0), size=(200,200), layer=2,photoname=w[1].photoname)
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].alert = {"carta":[True,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].carta],"drink":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drink],"mark":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].mark]}
                                        
                                    if self.layers[pos+1+4+4][0].string == "2":
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].msg = True
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].menumessage = MenuMenssageBar("images/hi_background.png", parent=self.obj[ self.layers[pos+4][0].perfil[1]  ][1].parent,   pos=(0,0), size=(200,200), layer=2,photoname=w[1].photoname)
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].alert = {"carta":[True,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].carta],"drink":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drink],"mark":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].mark]}
                                        
                                    if self.layers[pos+1+4+4][0].string == "3":
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].msg = True
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].menumessage = MenuMenssageBar("images/hi_background.png", parent=self.obj[ self.layers[pos+4][0].perfil[1]  ][1].parent,   pos=(0,0), size=(200,200), layer=2,photoname=w[1].photoname)
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].alert = {"carta":[True,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].carta],"drink":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drink],"mark":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].mark]}
                                        
                                    if self.layers[pos+1+4+4][0].string == "4":
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].msg = True
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].menumessage = MenuMenssageBar("images/hi_background.png", parent=self.obj[ self.layers[pos+4][0].perfil[1]  ][1].parent,   pos=(0,0), size=(200,200), layer=2,photoname=w[1].photoname)
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].alert = {"carta":[True,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].carta],"drink":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drink],"mark":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].mark]}
                                        
                                    if self.layers[pos+1+4+4][0].string == "5":
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].msg = True
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].menumessage = MenuMenssageBar("images/hi_background.png", parent=self.obj[ self.layers[pos+4][0].perfil[1]  ][1].parent,   pos=(0,0), size=(200,200), layer=2,photoname=w[1].photoname)
                                        self.obj[ self.layers[pos+4][0].perfil[1]  ][1].alert = {"carta":[True,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].carta],"drink":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drink],"mark":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].mark]}                                                                                                                                                                                                    
                                    self.layers[pos+1+4+4].remove(i)
                    #MAPA DRINK Perfil
                    for i in self.layers[pos+2+4+4]:
                            if len(self.layers[pos+4]) > 0:
                                if self.layers[pos+4][0].collideWidget(i):
                                    self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drinks = True
                                    self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drinkoffer = MenuDrinkOffer("images/drink_back.png", parent=self.obj[ self.layers[pos+4][0].perfil[1]  ][1].parent,   pos=(0,0), size=(200,200), layer=2,photoname=w[1].photoname)
                                    self.obj[ self.layers[pos+4][0].perfil[1]  ][1].alert = {"carta":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].carta],"drink":[True,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].drink],"mark":[False,self.obj[ self.layers[pos+4][0].perfil[1]  ][1].mark]}
                                    self.layers[pos+2+4+4].remove(i)                                                             
                    #BILL            
                    for i in self.layers[pos+1]:                                                           
                            if w[1].collideWidget(i):
                                self.layers[pos+1].remove(i)
                                w[1].actived ={"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}   
                    #MENU    
                    for i in self.layers[pos+2]:                                                           
                            if w[1].collideWidget(i):
                                self.layers[pos+2].remove(i)
                                if  len(self.layers[pos+2+4]) > 0:
                                    self.layers[pos+2+4][0].move = True
                                w[1].actived ={"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}
                                
                  # Sub Menu Cardapio               
                    for i in self.layers[pos+2+4]:               
                            if w[1].collideWidget(i):
                                self.layers[i.layer].remove(i)
                                if  len(self.layers[pos+2+4]) > 0:
                                    self.layers[pos+2+4][0].move = True                                
                                w[1].actived ={"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}                                                            
                    #PERFIL                
                    for i in self.layers[pos+3]:                                                           
                            if w[1].collideWidget(i):
                                self.layers[pos+3].remove(i)
				if len(self.layers[pos-3]) == 0:
				    w[1].actived ={"afundo":True,"profile":True,"net":True,"bill":True,"menu":True,"carta":True,"drink":True,"mark":True}
                                
                    # Menu Item  
                    for i in self.layers[pos+2+8]:         
                            if w[1].collideWidget(i):
                                pyglet.clock.schedule_once(w[1].animate,1.0/60.0)
                                if w[1].bill.cont % 2 == 0:
                                    str = "images/faixa_verde.png"
                                else:
                                    str = "images/faixa_laranja.png"
                                cont =   w[1].bill.cont     
                                if len(w[1].bill.place) > 0:
                                    m = w[1].bill.place[0]    
                                    w[1].bill.place.pop(0)     
                                
                                    w[1].bill.widgets[m] = ImageWidget(id=w[1].id,image_src=str,parent=w[1].bill.parent,pos=(0,w[1].bill.e), size=(w[1].bill.height,w[1].bill.width ),alfa = 1.0,layer=w[1].bill.layer )
                                    w[1].bill.e -= w[1].bill.iconPosReal
                                    w[1].bill.widgets["m12"] = m12 = ImageWidget(id=w[1].id,image_src="images/baixo_laranja.png",parent=w[1].bill.parent,pos=(0,w[1].bill.e),size=(w[1].bill.height,w[1].bill.width ),alfa = 1.0,layer=w[1].bill.layer )
                                    l = pyglet.text.Label(i.string ,font_size=w[1].bill.height*0.025,bold=True, color=(0,0,0,255),font_name='AFBattersea-Medium',x=200, y= 100)
                                    w[1].bill.cont += 1
                                    w[1].bill.labels.append(l)   
                                    if  len(self.layers[pos+2+4]) > 0:                         
                                        self.layers[pos+2+4][0].move = True
                                    self.layers[i.layer].remove(i)                                                    

                                               
    def on_touch_down(self, touches, touchID, x, y):
        self.touches = touches
        for (key,w) in self.obj.iteritems():
                    if w[1].visible:
                        if w[1].on_touch_down(touches, touchID,x, y):
                            print w[0]
                            pass
                        
        for l in self.layers:
                    for w in reversed(l):
                        if w.on_touch_down(touches, touchID, x, y):
                            pass
        
    def on_touch_move(self, touches, touchID, x, y):
        self.touches = touches
        for l in self.layers:
                    for w in reversed(l):
                        if w.on_touch_move(touches, touchID, x, y):
                            pass

    def on_touch_up(self, touches, touchID, x, y):
        self.touches = touches
        for l in self.layers:
                    for w in reversed(l):
                        if w.on_touch_up(touches, touchID, x, y):
                            pass
# ------------
    def on_object_down(self, touches, touchID,id, x, y,angle):
        # Por Rede Aqui
        for (key,w) in self.obj.iteritems():
                        if w[2] == id:
                            w[1].visible = True
                            if w[1].on_object_down(touches, touchID,id, x, y,angle):
                                pass
        
    def on_object_move(self, touches, touchID,id, x, y,angle):
        for (key,w) in self.obj.iteritems():
                    if w[2] == id:
                       if w[1].on_object_move(touches, touchID,id, x, y,angle):
                            pass

    def on_object_up(self, touches, touchID,id, x, y,angle):
        # Por Rede Aqui

        for (key,w) in self.obj.iteritems():
                      if w[2] == id:
                          w[1].visible = False
                          if w[1].on_object_up(touches, touchID,id, x, y,angle): 
                              pass    
     


   
                      