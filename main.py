from bullet import Bullet

from ursina import *

import json

app = Ursina()

window.title = 'Hidden in the Shadows'

camera.orthographic = True

camera.fov = 100

class World(Entity):
    def __init__(self,file,gravity=15,asteroids = [], **kwargs):
        super().__init__(**kwargs)
        self.gravity = gravity
        self.asteroids = asteroids
        self.hiding_zones = []
        self.bullets = []
        self.bounce_zones = []
        data = json.load(open(file))
        for asteroid in data["asteroids"]:
            self.add_planet(Asteroid(mass=asteroid["mass"],position=Vec2(asteroid["x"],asteroid["y"]),world=self))
        for hiding_zone in data["hiding_zones"]:
            self.add_hiding_zone(HidingZone(position=Vec2(hiding_zone["x"],hiding_zone["y"]),scale=Vec2(hiding_zone["scale_x"],hiding_zone["scale_y"])))
        for bounce_zone in data["bounce_zones"]:
            self.bounce_zones.append(BounceZone(position=Vec2(bounce_zone["x"],bounce_zone["y"]),scale=Vec2(bounce_zone["scale_x"],bounce_zone["scale_y"])))
        self.start = Entity(scale=10, position=Vec2(-40*camera.aspect_ratio,-35))
        self.start_display = Entity(model="quad",texture="1start", scale=self.start.scale, position=self.start.position)
        self.destination = Entity(model="quad",texture="circle",color=color.red, scale=10, position=(Vec2(40*camera.aspect_ratio,35)))
        self.arrow = Entity(parent= self.start, model="quad",texture="arrow",scale=0.3, scale_x=0.7,z=1,rotation_z=-90,origin=(-0.5,0))
        
    def add_planet(self, asteroid):
        self.asteroids.append(asteroid)

    def add_hiding_zone(self, hiding_zone):
        self.hiding_zones.append(hiding_zone)

    def update(self):
        if held_keys["left mouse"]:
            self.timer += time.dt / 3
            self.timer = min(self.timer,1)
            self.arrow.scale_x = self.timer + 0.7
        else:
            self.arrow.scale_x = 0.7
            self.start.look_at_2d(mouse.position*camera.fov)

    def destroy(self):
        for asteroid in self.asteroids:
            destroy(asteroid)
        for bullet in self.bullets:
            destroy(bullet)
        destroy(self.start)
        destroy(self.destination)
        destroy(self.arrow)

    def end(self):
        print("end")
        self.destroy()

    def input(self,key):
        if key == "left mouse down":
            self.direction = (mouse.position*camera.fov-world.start.position).normalized()
            self.timer = 0
        elif key == "left mouse up":
            velocity = self.direction*self.timer
            velocity = Vec2(velocity.x,velocity.y)
            print(world.start.position+self.direction*world.start.scale/2)
            self.bullets.append(Bullet(position=world.start.position+self.direction*world.start.scale/2,velocity=velocity,world=self))

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


class HidingZone(Entity):
    def __init__(self,position,scale, **kwargs):
        super().__init__(**kwargs)
        self.model = "quad"
        self.texture = "zone"
        self.color = color.rgb(74, 27, 0)
        self.scale = scale
        self.position = Vec3(*position,-2)
        self.origin= Vec2(-0.5,-0.5)
        

class BounceZone(Entity):
    def __init__(self,position,scale, **kwargs):
        super().__init__(**kwargs)
        self.model = "quad"
        self.texture = "zone"
        self.color = color.rgb(0, 27, 120)
        self.scale = scale
        self.position = Vec3(*position,0)
        self.origin= Vec2(-0.5,-0.5)
        self.collider = "box"
        



Audio("loop",loop=True, autoplay=True)


world = World("world.json")

app.run()