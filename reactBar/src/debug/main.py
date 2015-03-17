from widgetBar import *


c = BarLooping()

#widgets=[("star.png",(40,0),(50,50))]

"""  LAYER E IMPORTANTE NA CRIACAO"""

z6 = PerfilWidget(image_src="images/opa.png",id=40004,parent=c,layer=2, pos=(0,0), size=(200,200),alfa = 0.5,address=('127.0.0.1',40004),scale=2.0,
                 sex="m",name="marco",age="21",status="on",photo="images/homem1.png",photoname="images/nome_marco.png")

z4 = PerfilWidget(image_src="images/opa.png",id=40005,parent=c,layer=0, pos=(0,0), size=(200,200),alfa = 0.5,address=('127.0.0.12',40005),scale=2.0,
                  sex="f",name="Alice",age="23",status="off",photo="images/mulher2.png",photoname="images/nome_alice.png")
#
#z5 = PerfilWidget(image_src="images/opa.png",id=40008,parent=c,layer=1, pos=(0,0), size=(200,200),alfa = 0.5,address=('147.65.6.190',40008),scale=2.0,
#                  sex="f",name="Julia",age="22",status="off",photo="images/mulher1.png",photoname="images/nome_julia.png")
#
##
#z7 = PerfilWidget(image_src="images/opa.png",id=40009,parent=c,layer=3, pos=(0,0), size=(200,200),alfa = 0.5,address=('147.65.6.190',40009),scale=2.0,
#                  sex="m",name="Marco",age="25",status="on",photo="images/homem2.png",photoname="images/nome_joao.png")

#z2 = MenuDrinkOffer("images/drink_back.png", parent=c,  pos=(50,50), size=(200,200), layer=2)
#z3 = MenuMarked("images/fundo_mark.png", parent=c,  pos=(0,0), size=(200,200), layer=2)
#
#canvas = PaintWidget("images/text.png",parent=c, pos=(0,0), size=(500,600),layer=1 )
z1 = ImageButton("images/background.png",parent=c, pos=(0,0), size=(500,500))
#c.add_widget(z3)

c.add_widget(z1,0,'cur')
#c.add_widget(canvas,1,'cur')
c.add_widget(z4,0,'obj',0)
#c.add_widget(z5,1,'obj',6)
c.add_widget(z6,2,'obj',6)
#c.add_widget(z7,3,'obj',39)
#c.add_widget(z2,2,'cur')
#c.add_widget(z3,2,'cur')
#c.add_widget(z4)

        
w = UIWindow(c)
#w.set_fullscreen()

runTouchApp()
