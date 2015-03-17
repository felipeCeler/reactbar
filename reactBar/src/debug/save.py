
#import ctypes 
from pyglet.gl import * 
from pyglet import window 
from pyglet.window import mouse 
from pyglet.window import key 
import pyglet.clock 
from Tkinter import * 
from tkMessageBox import * 
from tkColorChooser import askcolor 
from tkFileDialog   import askopenfilename 
root = Tk() 
root.withdraw() 
#stuff_to_draw = [(1,'line',(10,15,30,35))] 
global win 
win = window.Window(width=640,height=480,visible=False) 
win.set_location(40,40) 
win.set_caption('drawer by noyan') 
global tex 
tex = pyglet.image.Texture.create(width=640,height=480) 
global std 
std = [] 
global state 
state = 'line' 
global begpt 
begpt = [] 
global endpt 
endpt = [] 
global mousecur 
mousecur = [0,0] 
global pressed 
pressed = False 
global ptsize 
ptsize = 3 
global color 
color = [0,0,0] 
global image 
image = None 
global drag 
drag = False 
global win2 
win2 = window.Window(width=100,height = 480) 
win2.set_location(700,40) 
win2.set_caption('controls') 
global linebut, circbut, brushbut, colorbut 
linebut = pyglet.image.load('line.png') 
circbut = pyglet.image.load('circ.png') 
brushbut = pyglet.image.load('brush.png') 
colorbut = pyglet.image.load('choose.png') 
global polys 
polys = [] 
win2.switch_to() 
#linebut.blit(20,20) 
@win2.event 
def on_mouse_press(x,y,button,modifiers): 
    global state 
    if x > 10 and x < 40 and y > 10 and y < 40: 
       state = 'line' 
    if x > 10 and x < 40 and y > 60 and y < 90: 
       state = 'brush' 
    if x > 60 and x < 90 and y > 60 and y < 90: 
       asd = askcolor() 
       global color 
       color = [asd[0][0]*1.0/255,asd[0][1]*1.0/255,asd[0][2]*1.0/255] 
def draw2(): 
    global win2 
    global linebut,circbut, brushbut, colorbut 
    win2.switch_to() 
    glClearColor(1.0, 1.0, 1.0, 0.0) 
    glClear(GL_COLOR_BUFFER_BIT) 
    linebut.blit(10,10) 
    circbut.blit(60,10) 
    brushbut.blit(10,60) 
    colorbut.blit(60,60) 
def init(w,h): 
        glClearColor(1.0, 1.0, 1.0, 0.0) 
        glMatrixMode(GL_PROJECTION) 
        gluOrtho2D (0.,w,0.,h) 
        glClear(GL_COLOR_BUFFER_BIT) 
@win.event 
def on_resize(width, height): 
        if height==0: 
                height=1 
        glViewport(0, 0, width, height) 
        init(width,height) 
@win.event 
def on_mouse_press(x,y,button,modifiers): 
    global begpt 
    begpt = [x,y] 
    if state == 'brush': 
       global ptsize 
       std.append(['brush',begpt[0],begpt[1],ptsize, 
[color[0],color[1],color[2]]]) 
    elif state == 'poly': 
       global polys,color,ptsize 
       if len(polys) == 0: 
          polys.append((x,y,color)) 
       elif len(polys) == 1: 
          if button == 4: 
             std.append(['line',polys[0][0],polys[0][1],x,y,ptsize, 
[color[0],color[1],color[2]]]) 
       elif len(polys) == 2: 
          if button == 4: 
             std.append(['tri',polys[0][0],polys[0][1],polys[1] 
[0],polys[1][0],x,y,ptsize,[color[0],color[1],color[2]]]) 
@win.event 
def on_mouse_release(x,y,button,modifiers): 
    global std 
    global begpt 
    global ptsize 
    global state 
    global drag 
    if state == 'line': 
       std.append(['line',begpt[0],begpt[1],x,y,ptsize, 
[color[0],color[1],color[2]]]) 
       drag = False 
@win.event 
def on_mouse_drag(x,y,dx,dy,buttons,modifiers): 
    global state 
    global drag 
    if state == 'brush': 
       global ptsize 
       std.append(['brush',x,y,ptsize,[color[0],color[1],color[2]]]) 
    elif state == 'line': 
       drag = True 
       global endpt 
       endpt = [x,y] 
@win.event 
def on_mouse_scroll(x,y,scroll_x,scroll_y): 
    global ptsize 
    ptsize += scroll_y 
    if ptsize < 1: 
       ptsize = 1 
    if ptsize > 100: 
       ptsize = 100 
def draw(): 
        global std 
        global win 
        win.switch_to() 
        global tex 
        glClear(GL_COLOR_BUFFER_BIT) 
        global image 
        glEnable(GL_TEXTURE_2D) 
        glBindTexture(GL_TEXTURE_2D,tex.id) 
        #colorBits = GLchar() 
        glTexImage2D(GL_TEXTURE_2D,0 ,3 , 640, 480, 0 , GL_RGB, 
GL_UNSIGNED_BYTE, colorBits) 
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, 
GL_LINEAR) 
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, 
GL_LINEAR) 
        glViewport(0,0,640,480) 
        if image: 
           glBindTexture(GL_TEXTURE_2D,image.id) 
           #tex.blit_into(image,0,0,0) 
        glBindTexture(GL_TEXTURE_2D,0) 
        for item in std: 
            if item[0] == 'line': 
               glLineWidth(item[5]) 
               glColor3f(item[6][0],item[6][1],item[6][2]) 
               pyglet.graphics.draw(2, pyglet.gl.GL_LINES,('v2i', 
(item[1], item[2], item[3], item[4]))) 
            elif item[0] == 'brush': 
               glPointSize( item[3] ) 
               glColor3f(item[4][0],item[4][1],item[4][2]) 
               pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,('v2i', 
(item[1], item[2]))) 
        global drag 
        if drag: 
           global begpt 
           global endpt 
           global color 
           global ptsize 
           glColor3f(color[0],color[1],color[2]) 
           glLineWidth(ptsize) 
           pyglet.graphics.draw(2, pyglet.gl.GL_LINES,('v2i', 
(begpt[0], begpt[1], endpt[0], endpt[1]))) 
        glBindTexture(GL_TEXTURE_2D,tex.id) 
        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,0,0, 640, 480, 0) 
        '''glBindTexture (GL_TEXTURE_2D, tex.id); 
        glBegin (GL_QUADS); 
        glTexCoord2f (0.0, 0.0); 
        glVertex3f (0.0, 0.0, 0.0); 
        glTexCoord2f (0.5, 0.0); 
        glVertex3f (640.0, 0.0, 0.0); 
        glTexCoord2f (0.5, 0.5); 
        glVertex3f (640.0, 480.0, 0.0); 
        glTexCoord2f (0.0, 0.5); 
        glVertex3f (0.0, 480.0, 0.0); 
        glEnd ();''' 
        glFinish() 
        glViewport(0,0,640,480) 
        glDisable(GL_TEXTURE_2D) 
        glFlush() 
@win.event 
def on_key_press(symbol, modifiers): 
        global state 
        if symbol == key.B: 
           state = 'brush' 
        elif symbol == key.L: 
           state = 'line' 
        elif symbol == key.P: 
           state = 'poly' 
        elif symbol == key.C: 
           asd = askcolor() 
           global color 
           color = [asd[0][0]*1.0/255,asd[0][1]*1.0/255,asd[0] 
[2]*1.0/255] 
        elif symbol == key.O: 
           global image 
           fn = askopenfilename() 
           image = pyglet.image.load(fn).get_texture() 
        elif symbol == key.S: 
           global tex 
           tex.save('lol.png') 
def main(): 
        global win 
        global win2 
        win.switch_to() 
        win.set_visible() 
        win2.set_visible() 
        clock=pyglet.clock.Clock() 
        while not win.has_exit: 
                #glClear(GL_COLOR_BUFFER_BIT) 
                win2.dispatch_events() 
                draw2() 
                win2.flip() 
                win.dispatch_events() 
                draw() 
                win.flip() 
                clock.tick() 
if __name__ == '__main__': main()