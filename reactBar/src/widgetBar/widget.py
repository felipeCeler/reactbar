#
#  Widgets Definitions
#
#  Author: Andre Maximo
#  Date: October 29, 2008
#

from pymt import *

#
#  Image Widget
#
class ImageWidget(DragableWidget):
    def __init__(self, image_file, parent=None, level=0, pos=(0,0), size=(1,1), scale = 1.0):
        DragableWidget.__init__(self, parent, pos, size)
    self.level = level
        img = pyglet.image.load(image_file)
        self.image = pyglet.sprite.Sprite(img)
        self.image.x, self.image.y = self.x, self.y
        self.scale =  scale
        self.image.scale = self.scale
        self.width, self.height = (self.image.width, self.image.height)

    def on_touch_down(self, touches, touchID, x, y):
    if DragableWidget.on_touch_down(self, touches, touchID, x, y):
        self.parent.layers[self.level].remove(self)
        self.parent.layers[self.level].append(self)
        return True
        
    def draw_widget(self): pass

    def draw(self):
        self.image.x, self.image.y = (self.x, self.y)
        self.image.scale = self.scale
        self.width, self.height = (self.image.width, self.image.height)
        self.image.draw()

#
#  Widget 3D Class
#
#    This is a widget to display a 3D scene. It can be dragged by
#  'touch' in the PyMT (Python Multi-Touch) context. See PyMT
#  DraggableWidget in ui.py for more details.
#
#  To-Do List:
#    -- Allow zoomming using fovy (or eye) without changing class
#      heritance for ZoomingWidget, nevertheless it can be used
#      as a model.
#
class Widget3D(DragableWidget):
    def __init__(self, parent=None, level=0, fovy = 45., znear=.1, zfar=255.,
        eye=(0., 0., 3.), center=(0., 0., 0.), up=(0., 1., 0.), showBorder=True,
        borderColor=(255,255,255), pos=(0,0), size=(100,100)):
    DragableWidget.__init__(self, parent, pos, size)
    self.level = level
    self.fovy = fovy; self.znear = znear; self.zfar = zfar
    self.eye = eye; self.center = center; self.up = up
    self.showBorder = showBorder; self.borderColor = borderColor

    def on_touch_down(self, touches, touchID, x, y):
    if DragableWidget.on_touch_down(self, touches, touchID, x, y):
        self.parent.layers[self.level].remove(self)
        self.parent.layers[self.level].append(self)
        return True

    def draw_widget(self):
    glLineWidth(1)
    glBegin(GL_LINE_LOOP)
    glColor3ub(self.borderColor[0], self.borderColor[1], self.borderColor[2])
    glVertex2i(int(self.x), int(self.y))
    glVertex2i(int(self.x)+self.width, int(self.y))
    glVertex2i(int(self.x)+self.width, int(self.y)+self.height)
    glVertex2i(int(self.x), int(self.y)+self.height)
    glEnd()

    def draw(self):
    if self.showBorder: self.draw_widget()
    glViewport(int(self.x), int(self.y), self.width, self.height)
    h = self.parent.parent.height
    w = self.parent.parent.width
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(self.fovy, w/h, self.znear, self.zfar)
    gluLookAt(self.eye[0], self.eye[1], self.eye[2],
        self.center[0], self.center[1], self.center[2],
        self.up[0], self.up[1], self.up[2])

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    self.draw3DScene()
    
    glPopMatrix()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    
    glViewport(0, 0, w, h)
    
    def draw3DScene(self):
    pass
