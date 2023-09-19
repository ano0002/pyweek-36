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


def input(key):
    if key == "space":
        asteroid = Asteroid(mass=1,position=mouse.position*camera.fov,world=world)
        world.add_planet(asteroid)
    elif key == "left mouse down":
        bullet = Bullet(world=world,position=mouse.position*camera.fov)

world = World()

app.run()