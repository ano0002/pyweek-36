from bullet import Bullet

from ursina import *

app = Ursina()

window.title = 'Hidden in the Shadows'

camera.orthographic = True

camera.fov = 100

class World(Entity):
    def __init__(self,gravity=15,asteroids = [], **kwargs):
        super().__init__(**kwargs)
        self.gravity = gravity
        self.asteroids = asteroids
        self.start = Entity(scale=10, position=Vec2(-40*camera.aspect_ratio,-35))
        self.start_display = Entity(model="quad",texture="1start", scale=self.start.scale, position=self.start.position)
        self.destination = Entity(model="quad",texture="circle",color=color.red, scale=10, position=(Vec2(40*camera.aspect_ratio,35)))
        self.arrow = Entity(parent= self.start, model="quad",texture="arrow",scale=0.3, scale_x=0.7,z=1,rotation_z=-90,origin=(-0.5,0))
        
    def add_planet(self, asteroid):
        self.asteroids.append(asteroid)

    def update(self):
        if held_keys["left mouse"]:
            self.arrow.scale_x = timer + 0.7
        else:
            self.arrow.scale_x = 0.7
            self.start.look_at_2d(mouse.position*camera.fov)

class Asteroid(Entity):
    def __init__(self,mass,position,world=None, **kwargs):
        super().__init__(**kwargs)
        self.model = "quad"
        self.texture = "circle"
        self.color = color.rgb(74, 27, 0)
        self.scale = 3*mass**0.7
        self.position = position
        self.mass = mass
        self.world = world




timer = 0


def input(key):
    global direction, timer
    if key == "1":
        asteroid = Asteroid(mass=1,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "2":
        asteroid = Asteroid(mass=2,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "3":
        asteroid = Asteroid(mass=3,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "4":
        asteroid = Asteroid(mass=4,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "5":
        asteroid = Asteroid(mass=5,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "6":
        asteroid = Asteroid(mass=5,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "7":
        asteroid = Asteroid(mass=7,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "8":
        asteroid = Asteroid(mass=8,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "9":
        asteroid = Asteroid(mass=9,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "0":
        asteroid = Asteroid(mass=10,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "left mouse down":
        direction = (mouse.position*camera.fov-world.start.position).normalized()
        timer = 0
    elif key == "left mouse up":
        velocity = direction*timer
        velocity = Vec2(velocity.x,velocity.y)
        Bullet(position=world.start.position+direction*world.start.scale/2,velocity=velocity,world=world)

def update():
    global timer
    if held_keys["left mouse"]:
        timer += time.dt
        timer = min(timer,1)

world = World()

app.run()