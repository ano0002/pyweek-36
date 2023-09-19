from bullet import Bullet

from ursina import *

app = Ursina()

window.title = 'Hidden in the Shadows'

camera.orthographic = True

camera.fov = 100

class World(Entity):
    def __init__(self,gravity=9.81,asteroids = [], **kwargs):
        super().__init__(**kwargs)
        self.gravity = gravity
        self.asteroids = asteroids
        self.start = Entity(model="quad",texture="circle", scale=10, position=(Vec2(-40*camera.aspect_ratio,-35)))
        self.destination = Entity(model="quad",texture="circle",color=color.red, scale=10, position=(Vec2(40*camera.aspect_ratio,35)))

    def add_planet(self, asteroid):
        self.asteroids.append(asteroid)

    def update(self):
        pass

class Asteroid(Entity):
    def __init__(self,mass,position,world=None, **kwargs):
        super().__init__(**kwargs)
        self.model = "quad"
        self.texture = "circle"
        self.color = color.rgb(74, 27, 0)
        self.scale = 3*mass
        self.position = position
        self.mass = mass
        self.world = world

timer = 0

def input(key):
    global direction, timer
    if key == "1":
        asteroid = Asteroid(mass=1,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    if key == "2":
        asteroid = Asteroid(mass=2,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    if key == "3":
        asteroid = Asteroid(mass=3,position=mouse.position*camera.fov,world=world)
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
    timer += time.dt

world = World()

app.run()