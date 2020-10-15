import pygame as pg
from random import randint,uniform
import numpy as np
import math

class Environment:

    def __init__(self,W,H,mapfile,aircraftfile):

        self.W = W
        self.H = H
        self.mapfile = mapfile
        self.aircraftfile = aircraftfile
        self.aircraft_w = 90
        self.aircraft_h = 66
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (200,0,0)
        self.green = (0,200,0)
        self.blue = (0,0,200)
        
    def setup(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.gameDisplay = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption('Warzone')
        #line and aircraft
        self.startx = randint(0,self.W)
        self.starty = np.random.choice([0,self.H],1)[0]
        self.endx = randint(0,self.W)
        self.endy = self.H-self.starty
        self.line_angle = math.atan((self.endx-self.startx)/(self.endy-self.starty))*(180/math.pi) + 180*int(self.starty == 0)
        self.aircraft_velx = (self.endx-self.startx)/100
        self.aircraft_vely = (self.endy-self.starty)/100
        self.aircraft_posx = self.startx - self.aircraft_w//2 + 10
        self.aircraft_posy = self.starty - self.aircraft_h//2 + 10
        #safe's circle
        self.circle_c0 = (randint(100,self.W-100),randint(100,self.H-100))
        self.circle_r = 500
        #target point
        self.radius = randint(0,self.circle_r)
        angle = uniform(0,2*math.pi)
        self.target_x = int(self.radius*math.cos(angle)+self.circle_c0[0])
        border_x = 0.2*self.W
        if self.target_x < border_x: self.target_x = border_x
        elif self.target_x > self.W-border_x: self.target_x = self.W-border_x
        self.target_y = int(self.radius*math.sin(angle)+self.circle_c0[1])   
        self.textfont = pg.font.Font('fonts/BlackOpsOne-Regular.ttf' , 24)
        self.text = self.textfont.render('TARGET', True, self.blue)

    def render(self):
        #map
        mapimg = pg.image.load(self.mapfile)
        self.gameDisplay.blit(mapimg,(0,0))
        #aircraft and trajectory line
        self.aircraft_posx = int(self.aircraft_posx + self.aircraft_velx)
        self.aircraft_posy = int(self.aircraft_posy + self.aircraft_vely) 
        pg.draw.line(self.gameDisplay,self.white,(self.startx,self.starty),(self.endx,self.endy),2)
        aircraftimg = pg.image.load(self.aircraftfile)
        aircraftimg = pg.transform.rotate(aircraftimg,self.line_angle)
        self.gameDisplay.blit(aircraftimg,(self.aircraft_posx,self.aircraft_posy))
        #safe circle
        pg.draw.circle(self.gameDisplay,self.red,self.circle_c0,self.circle_r,2)
        #target
        pg.draw.circle(self.gameDisplay,self.blue,(self.target_x,self.target_y),10)
        self.gameDisplay.blit(self.text, (self.target_x,self.target_y-30))

class Player:

    def __init__(self):
        self.player_vel = 5
        self.g = 9.8
    def set_data(self,start,aircraft_vel,target):
        self.startx,self.starty = start
        self.aircraft_velx, self.aircraft_vely = aircraft_vel
        self.targetx,self.targety = target
    def get_jump_point(self):
        jumpx  = 

if __name__ == "__main__":
    
    env = Environment(1366,768,'images/map.png','images/aircraft.png')
    env.setup()
    crashed = False
    player = Player()
    player.set_data((env.startx,env.starty),(env.aircraft_velx,env.aircraft_vely),(env.targetx,env.targety))
    while not crashed and env.aircraft_posy <= env.H -env.aircraft_h//2+10 and env.aircraft_posy >= -env.aircraft_h//2+10:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                crashed = True

        env.gameDisplay.fill(env.black)
        env.render()
        pg.display.update()
        env.clock.tick(10)

    quit()