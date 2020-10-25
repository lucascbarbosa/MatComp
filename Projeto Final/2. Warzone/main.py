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
        self.pink = (252,15,192)
        self.jumped = False
        self.crashed = False
        self.height = 5.
        self.m = 1.
        self.g = 7.
        self.k0  = 2.
        self.gamma = .1
        self.alfa = 10

    def setup_plane(self):
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
        self.aircraft_velx = float((self.endx-self.startx)/100)
        self.aircraft_vely = float((self.endy-self.starty)/100)
        self.aircraft_posx = self.startx - self.aircraft_w//2 
        self.aircraft_posy = self.starty - self.aircraft_h//2 

        #safe circle
        self.circle_c0 = (randint(100,self.W-100),randint(100,self.H-100))
        self.circle_r = 250

        #target point
        self.radius = randint(self.circle_r//2,self.circle_r*4//2)
        angle = uniform(0,2*math.pi)

        self.targetx = round(self.radius*math.cos(angle)+self.circle_c0[0])
        border_x = 0.2*self.W
        if self.targetx < border_x: self.targetx = round(border_x)
        elif self.targetx > self.W-border_x: self.targetx = round(self.W-border_x)

        self.targety = round(self.radius*math.sin(angle)+self.circle_c0[1])
        if self.targety < 0: self.targety = 0
        elif self.targety > self.H: self.targety = self.H

        self.textfont = pg.font.Font('fonts/BlackOpsOne-Regular.ttf' , 24)
        self.text = self.textfont.render('TARGET', True, self.blue)
        
        #Skydiving
        self.pixels = [] #array with pixels corresponding to each point (d,z)
        self.currentd = 0.0


    def render_plane(self):
        #map
        mapimg = pg.image.load(self.mapfile)
        self.gameDisplay.blit(mapimg,(0,0))

        #aircraft and trajectory line
        self.aircraft_posx = round(self.aircraft_posx + self.aircraft_velx)
        self.aircraft_posy = round(self.aircraft_posy + self.aircraft_vely) 
        pg.draw.line(self.gameDisplay,self.white,(self.startx,self.starty),(self.endx,self.endy),2)
        aircraftimg = pg.image.load(self.aircraftfile)
        aircraftimg = pg.transform.rotate(aircraftimg,self.line_angle)
        self.gameDisplay.blit(aircraftimg,(self.aircraft_posx,self.aircraft_posy))

        #safe circle
        pg.draw.circle(self.gameDisplay,self.red,self.circle_c0,self.circle_r,2)

        #target
        pg.draw.circle(self.gameDisplay,self.blue,(self.targetx,self.targety),10)
        self.gameDisplay.blit(self.text, (self.targetx,self.targety-30))

        #Player
        if abs(self.aircraft_posx + self.aircraft_w//2 - self.jump_pointx) <= 5*abs(self.aircraft_velx) and abs(self.aircraft_posy + self.aircraft_h//2 - self.jump_pointy) <= 5*abs(self.aircraft_vely):
            self.jumped = True
            print('PULA')
        print(f'PosX = {self.aircraft_posx+env.aircraft_w//2} jumpX = {self.jump_pointx} posY = {self.aircraft_posy+self.aircraft_h//2} jumpY = {self.jump_pointy}')

        

    def get_theta(self,k0,gamma,height,dist,v):
        
        def k(theta):
            return k0*abs(math.cos(theta))+gamma
        
        def z(theta):
            t = dist/v
            return (-self.m*self.g/(k(theta))**2)*(self.m*(math.exp(-k(theta)*t/self.m)-1)+k(theta)*t)+height
        
        def z_prime(theta):
            aux = math.exp(-k(theta)*dist/(self.m*v))
            return (1/((k(theta)**3)*v))*k0*(self.m**2)*self.g*math.sin(theta)*((2*self.m*v+k(theta)*self.d)*(1-aux)-2*dist*k(theta))

        N = 100
        tol = 1e-7
        count = 0
        p = .1
        dif = 1
        theta = 0.1
        
        print(f'm = {self.m} g = {self.g} k0 = {k0} gamma = {gamma} v = {v} distance = {dist} height = {height}')


        if z(0) < 0.:
            theta = 0.
        else:
            while count < N and dif > tol:
                print(f'theta = {theta} z(theta) = {z(theta)} z_prime(theta) = {z_prime(theta)}')
                clone = theta
                theta -= p*z(theta)/z_prime(theta)
                dif = abs(clone-theta)
                count += 1

                if theta > math.pi or theta < 0.:
                    theta = math.pi/2
                    break

        print(f'Theta = {theta}')
        return theta
    
    def get_dist_parachute(self):
        
        def k(theta):
            return self.k0*abs(math.cos(theta))+self.gamma
        
        def z(r):
            return ((-self.m*self.g/(k(self.theta))**2)*(self.m*(math.exp(-(k(self.theta)*r/(self.m*self.player_vel)))-1)+k(self.theta)*r/self.player_vel))+self.height
        
        def z_prime(r):
            return (self.m*self.g/self.player_vel)*((math.exp(-k(self.theta)/(self.m*self.player_vel))-1)/(self.gamma+self.k0*math.cos(self.theta)))
        
        N = 100
        tol = 1e-3
        count = 0
        p = .1
        dif = 1
        dist = 0.1
        
       
        while count < N and dif > tol:
            print(f'dist = {dist}, z(dist) = {z(dist)}, z_prime(dist) = {z_prime(dist)}')
            clone = dist
            dist -= p*z(dist)/z_prime(dist)
            dif = abs(clone-dist)
            count += 1

        if dist > self.d:
            dist = self.d
        self.dist_parachute = (self.d-dist)

        print(f'parachute_dist = {self.dist_parachute}')

    def render_jump(self):
       
        def k(theta,k0,gamma):
            return k0*abs(math.cos(theta))+gamma

        def z(r,k,v):
            return ((-self.m*self.g/(k**2))*(self.m*(math.exp(-(k*r/(self.m*v)))-1)+k*r/v))+self.height
        
        

        k_dive = k(self.theta,self.k0,self.gamma)
        k_parachute = k(self.theta_parachute,self.k0*self.alfa,self.alfa*self.gamma)
        
        chute = self.theta == 0.

        
        if chute:
            currentz = z(self.currentd,k_parachute,self.player_vel/2)
            if self.currentd >= self.dist_parachute:
                chute = False
                print('SOLTA')
            self.currentd += (self.player_vel/200.)
            

        else:
            currentz = z(self.currentd,k_parachute,self.player_vel)
            self.currentd += self.player_vel/100.

            

        if currentz*100 <0.0:
            self.crashed = True
            return None

        if self.currentd >= self.d:
            self.currentd = self.d

        self.pixels.append((round(300+(500*self.currentd//self.d)),round(600-(500*currentz//self.height))))
        
        #Draw axis
        pg.draw.line(self.gameDisplay,self.white,(300,50),(300,600),2)
        pg.draw.line(self.gameDisplay,self.white,(300,600),(850,600),2)

        #Draw z vs d curve
        pg.draw.lines(self.gameDisplay,self.pink,False, self.pixels,1)
        
        print(f'distance = {round(self.currentd*100)} PosZ = {round(currentz*100)}')



    def setup_jump(self,jump_point,vel):
        
        self.jump_pointx,self.jump_pointy = jump_point
        self.player_vel = vel
        self.d = math.sqrt((self.jump_pointx-self.targetx)**2+(self.jump_pointy-self.targety)**2)/100.
        self.theta = self.get_theta(self.k0,self.gamma,self.height,
                                    self.d,self.player_vel)
        self.pixels.append((300,600-self.height))
        self.get_dist_parachute()
        self.theta_parachute = self.get_theta(self.alfa*self.k0,self.alfa*self.gamma,self.height, 
                                              self.dist_parachute,self.player_vel/2)

            
class Player:

    def __init__(self,W,H,start,aircraft_vel,target):
        self.W = W
        self.H = H
        self.vel = 1
        self.startx,self.starty = start
        self.aircraft_velx, self.aircraft_vely = aircraft_vel
        self.targetx,self.targety = target
        self.startx /= 100
        self.starty /= 100
        self.targetx /= 100
        self.targety /= 100
        

    def get_jump_point(self):
        N = 100
        tol = 1e-7
        def f_total_time():
            return abs(self.jump_pointx - self.startx)/self.aircraft_velx + abs(self.targetx-self.jump_pointx)/Vjx()
        def f_prime():
            return ((((-1)**int(self.jump_pointx<self.startx))/self.aircraft_velx)+(((-1)**int(self.targetx>=self.jump_pointx))*Vjx()-abs(self.targetx-self.jump_pointx)*Vjx_prime())/(Vjx()**2))
        def Vjx():
            aux = np.linalg.norm([self.targetx-self.jump_pointx,self.targety-self.jump_pointy])
            res = self.vel*abs(self.targetx-self.jump_pointx)/aux
            if res == 0.0:
                res = 1e-10
            return res
        def Vjx_prime():
            aux = np.linalg.norm([self.targetx-self.jump_pointx,self.targety-self.jump_pointy])
            return self.vel*(((-1)**int(self.targetx>=self.jump_pointx))*aux-abs(self.targetx-self.jump_pointx)*(((self.jump_pointx-self.targetx)+(-y_prime())*(self.targety-self.jump_pointy))/aux))/(aux**2)
        def y():
            self.jump_pointy  = round(100*float(float(self.aircraft_vely/self.aircraft_velx)*(self.jump_pointx-self.startx)+self.starty))
        def y_inv():
            self.jump_pointx = round(float(float(self.aircraft_velx/self.aircraft_vely)*(self.jump_pointy-self.starty)+self.startx))
        def y_prime():
            return self.aircraft_vely/self.aircraft_velx
        def get_initial_guess():
            #the initial guess is a point wich the distance vector is perpendicular to the aircraft's trajectory
            vec_a = np.array([self.targetx-self.startx,self.targety-self.starty])
            vec_b = np.array([self.aircraft_velx,self.aircraft_vely])
            res = list((np.dot(vec_a,vec_b)/(np.linalg.norm(vec_b)**2))*vec_b)
            jump_pointx = res[0] + self.startx
            jump_pointy = res[1] + self.starty
            if round(self.aircraft_velx,2) == .00:
                jump_pointx = self.startx
                jump_pointy = self.targety
            if round(self.aircraft_vely,2) == .00:
                jump_pointy = self.starty
                jump_pointx = self.targetx

            return jump_pointx,jump_pointy

        self.jump_pointx,self.jump_pointy = get_initial_guess()
        count = 0
        p = 0.8
        der = f_prime()
        while count < N and abs(der)>tol:
            der = f_prime()
            self.jump_pointx  -= p * der
            count += 1
        
        print(self.jump_pointx,self.jump_pointy)

        if self.jump_pointx < 0:
            print('foo1')
            self.jump_pointx = 0
            y()
            print(self.jump_pointx,self.jump_pointy)

        elif self.jump_pointx > self.W:
            print('foo2')
            self.jump_pointx = self.W
            print(self.jump_pointx)
            y()
            print(self.jump_pointx,self.jump_pointy)

        if self.jump_pointy < 0:
            print('foo3')
            self.jump_pointy = 0
            print(self.jump_pointy)
            y_inv()
            print(self.jump_pointx,self.jump_pointy)


        elif self.jump_pointy > self.H:
            print('foo4')
            self.jump_pointy = self.H
            print(self.jump_pointy)
            y_inv()
            print(self.jump_pointx,self.jump_pointy)


        y()
        self.jump_pointx = round(100*self.jump_pointx)
        self.velx = Vjx()
        self.vely = math.sqrt(self.vel**2-self.velx**2) #velx² + vely² = vel²

             
if __name__ == "__main__":
    
    env = Environment(1366,768,'images/map.png','images/aircraft.png')
    env.setup_plane()
    player = Player(1366,768,(env.startx,env.starty),(env.aircraft_velx,env.aircraft_vely),(env.targetx,env.targety))
    
    #get jump_point and set it in Environment object
    player.get_jump_point()
    env.setup_jump((player.jump_pointx,player.jump_pointy),player.vel)

    while not env.crashed and ((env.aircraft_posy <= env.H -env.aircraft_h//2 and env.aircraft_posy >= -env.aircraft_h//2) or env.jumped):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                env.crashed = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                env.crashed = True
        
        env.gameDisplay.fill(env.black)
        if not env.jumped: env.render_plane()
        else: env.render_jump()

        pg.display.update()
        env.clock.tick(10)

    quit()