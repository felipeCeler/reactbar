from pymt import *



class ImageWidget(ZoomableImage):
    def __init__(self, image_src, parent=None, level=0, pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0):
        
        ZoomableImage.__init__(self,image_src, parent, pos, size)
        self.level = level
        img = pyglet.image.load(image_src)
            
        self.texture = img.get_texture()
        self.texture.width , self.texture.height = size
        
        self.x , self.y = pos
 
        self.scale =  scale
        
        self.alfa = alfa
        
        
    def collidePoint(self, x,y):
            radius = sqrt(self.width*self.width+0.5 + self.height*self.height*0.5)/2 *self.zoom
            dist = Length(self.translation - Vector(x,y))
            if radius >= dist:
               return True
            else:
              return False
           
    def draw(self):
        
#       glPushMatrix()
#       radius = sqrt(self.width*self.width*0.5 + self.height*self.height*0.5)/2 *self.zoom
#
#       drawCircle((self.translation[0], self.translation[1]) ,radius=radius, color=(1.0,.0,.0))
#        
#       glPopMatrix()
#                


       glPushMatrix()
       glTranslatef(self.translation[0], self.translation[1], 0)
       glRotatef(self.rotation , 0, 0, 1)
       glScalef(self.zoom, self.zoom, 1)
       glScalef(self.width, self.height, 1)
       self.draw_widget()
       glPopMatrix()

        
    def draw_widget(self):
        
#        glPushMatrix()
#        glPointSize(5.0)
#        glColor3f(0.0,1.0,0.0)
#        glBegin(GL_POINTS)
#        glVertex2f(self.x,self.y)
#        glEnd()
#        glPopMatrix()
##                
#        glPushMatrix()
#        glPointSize(5.0)
#        glColor3f(0.0,1.0,0.25)
#        glBegin(GL_POINTS)
#        glVertex2f(self.x+0.5,self.y+0.5)
#        glEnd()
#        glPopMatrix()
        
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        glBindTexture(self.texture.target, self.texture.id)
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture.height,1.0/self.texture.height,1.0)
        self.texture.blit(0,0)
        glDisable(self.texture.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        glPopAttrib()
        


    
class PerfilWidget(ImageWidget):
    def __init__(self, image_src, parent=None, level=0, pos=(0,0), size=(1,1), scale = 2.0,alfa = 1.0,widgets=[("",(0,0),(0,0))]):
        
        ImageWidget.__init__(self,image_src, parent,level, pos, size,scale,alfa)
        
        self.widgets = []
          
        for i in widgets:
            self.widgets.append(ImageWidget(i[0],parent,i[1] ,i[2],alfa = 0.5 ))
   
        print "AFFFF",self.widgets[0].x   
        self.x,self.y = pos
        

    def collidePointButton(self, x,y,widget):
            radius = sqrt(widget.width*widget.width*0.5 + widget.height*widget.height*0.5)/2 *self.zoom    
            dist = Length(Vector(self.translation[0]+widget.x*self.zoom,self.translation[1]+widget.y*self.zoom) - Vector(x,y))
            if radius >= dist:
               return True
            else:
              return False
          
    def draw(self):
        
        glPushMatrix()
        radius = sqrt(self.width*self.width*0.5 + self.height*self.height*0.5)/2 *self.zoom

        drawCircle((self.translation[0], self.translation[1]) ,radius=radius, color=(1.0,.0,.0))

        
        glPopMatrix()
   
        
#        glPushMatrix()
#        glTranslatef(self.translation[0], self.translation[1], 0)
#        glRotatef(self.rotation , 0, 0, 1)
#        glScalef(self.zoom, self.zoom, 1)
#        
        for i in self.widgets:     
            glPushMatrix()
            glTranslatef(i.x*self.zoom,i.y*self.zoom, 0)
#        glScalef(self.z1.width, self.z1.height, 1)
            i.draw()#_widget()
            glPopMatrix()
#        glPushMatrix()
#        glScalef(self.texture1.width, self.texture1.height, 1)
#        self.draw_widget(-40,0)
#        glPopMatrix()
#        
#        glPushMatrix()
#        glScalef(self.texture1.width, self.texture1.height, 1)
#        self.draw_widget(40,0)
#        glPopMatrix()
#        
#        glPushMatrix()
#        glScalef(self.texture1.width, self.texture1.height, 1)
#        self.draw_widget(0,-40)
#        glPopMatrix()
#        
#        glPushMatrix()
#        glScalef(self.texture1.width, self.texture1.height, 1)
#        self.draw_widget(0,40)
#        glPopMatrix()
#        
#        glPopMatrix()

        
    def draw_widget(self,x,y):

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1,1,1,self.alfa)
        glEnable(self.texture1.target)        # typically target is GL_TEXTURE_2D
        glBindTexture(self.texture1.target, self.texture1.id)
        glTranslatef(-0.5,-0.5,0)
        glPushMatrix()
        glScalef(1.0/self.texture1.height,1.0/self.texture1.height,1.0)
        self.texture1.blit(0,0)
        glDisable(self.texture1.target)
        glPopMatrix()
         
        glEnable(GL_BLEND)
        glPopAttrib()
        

#        glPushMatrix()
#        glTranslatef(0.0,0.0,0)
#        self.z1.draw_widget()
#        glPopMatrix()
        

        

        
    def upDate(self):
        
        for i in self.widgets:
             i.rotation     =       self.rotation   
             i.translation =        self.translation  
             i.zoom =        self.zoom  

             i.touchDict =  self.touchDict                
             i.original_points =        self.original_points
             i.originalCenter =        self.originalCenter  
             i.newCenter =       self.newCenter
        
        
    def on_touch_down(self, touches, touchID, x, y):
        
        for i in self.widgets:
            if self.collidePointButton(x, y,i):
                print "uiiiiiiiiiiiiiiiii Z!PORRA"        
        if not self.collidePoint(x,y):

            return False
#        if self.collidePointButton(x, y):
#            print "uiiiiiiiiiiiiiiiii Z!"
#        if  self.collidePointButton(x+40,y):
#            print "x+40"
#        if  self.collidePointButton(x-40,y):
#            print "x-40"
#        if  self.collidePointButton(x,y+40):
#            print "y+40"              
#        if  self.collidePointButton(x,y-40):
#            print "y-40"
#        print  "x,y" , x,y
#        print "size", self.width*self.zoom, self.height*self.zoom
        if len(self.touchDict) == 1:
                    print 'rotated'
                    self.rotation +=180
                    self._oldrotation +=180
                            
                   
        if len(self.touchDict) < 2:
                        v = Vector(x,y)
                        self.original_points[len(self.touchDict)] = v
                        self.touchDict[touchID] = v
        self.upDate()                
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
                self.upDate()       
                         
    def on_touch_up(self, touches, touchID, x, y):
                if touchID in self.touchDict: #end interaction 
                        self._zoom = self.zoom
                        self._translation += self.translation - self._translation
                        self._oldrotation = (self._rotation + self._oldrotation) %360

                        self.touchDict = {}
                self.upDate()       