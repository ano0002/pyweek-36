from ursina import *

from bullet import Bullet

from ursina import *

import json

app = Ursina()

window.title = 'Hidden in the Shadows'

camera.orthographic = True

camera.fov = 100

class World(Entity):
    def __init__(self,gravity=15,asteroids = [], **kwargs):
        super().__init__(**kwargs)
        self.gravity = gravity
        self.asteroids = asteroids
        self.hiding_zones = []
        self.bounce_zones = []
        self.start = Entity(scale=10, position=Vec2(-40*camera.aspect_ratio,-35))
        self.start_display = Entity(model="quad",texture="1start", scale=self.start.scale, position=self.start.position)
        self.destination = Entity(model="quad",texture="circle",color=color.red, scale=10, position=(Vec2(40*camera.aspect_ratio,35)))
        self.arrow = Entity(parent= self.start, model="quad",texture="arrow",scale=0.3, scale_x=0.7,z=1,rotation_z=-90,origin=(-0.5,0))
        
    def add_planet(self, asteroid):
        self.asteroids.append(asteroid)

    def add_hiding_zone(self, hiding_zone):
        self.hiding_zones.append(hiding_zone)

    def add_bounce_zone(self, bounce_zone):
        self.bounce_zones.append(bounce_zone)

    def update(self):
        if held_keys["left mouse"]:
            self.arrow.scale_x = timer + 0.7
        else:
            self.arrow.scale_x = 0.7
            self.start.look_at_2d(mouse.position*camera.fov)

    def end(self):
        print("end")

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
        self.color = color.rgba(74, 27, 0,120)
        self.scale = scale
        position.z = -2
        self.position = position
        self.origin = (-0.5,-0.5)
    
class BounceZone(Entity):
    def __init__(self,position,scale, **kwargs):
        super().__init__(**kwargs)
        self.model = "quad"
        self.texture = "zone"
        self.color = color.rgba(0, 27, 120,120)
        self.scale = scale
        position.z = 0
        self.position = position
        self.origin = (-0.5,-0.5)
        self.collider = 'box'

def save_world(world):
    data = {}
    data["asteroids"] = []
    data["hiding_zones"] = []
    data["bounce_zones"] = []
    for asteroid in world.asteroids:
        data["asteroids"].append({"mass":asteroid.mass,"x":asteroid.x,"y":asteroid.y})
    for hiding_zone in world.hiding_zones:
        if hiding_zone.scale_x == 0 or hiding_zone.scale_y == 0:
            continue
        data["hiding_zones"].append({"x":hiding_zone.x,"y":hiding_zone.y,"scale_x":hiding_zone.scale_x,"scale_y":hiding_zone.scale_y})
    for bounce_zone in world.bounce_zones:
        if bounce_zone.scale_x == 0 or bounce_zone.scale_y == 0:
            continue
        if not((bounce_zone.scale_x < 0 and bounce_zone.scale_y < 0) or (bounce_zone.scale_x > 0 and bounce_zone.scale_y > 0)):
            continue
        data["bounce_zones"].append({"x":bounce_zone.x,"y":bounce_zone.y,"scale_x":bounce_zone.scale_x,"scale_y":bounce_zone.scale_y})
    with open("world.json","w") as file:
        json.dump(data,file)


timer = 0


def input(key):
    global direction, timer,mouse_origin
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
    elif key == "right mouse down":
        for asteroid in world.asteroids:
            if distance_2d(asteroid, mouse.position*camera.fov) < asteroid.scale/2:
                destroy(asteroid)
                world.asteroids.remove(asteroid)
                return   
    elif key == "middle mouse down":
        world.add_hiding_zone(HidingZone(position=mouse.position*camera.fov,scale=Vec2(0,0)))
        mouse_origin = mouse.position*camera.fov
    elif key == "b":
        world.add_bounce_zone(BounceZone(position=mouse.position*camera.fov,scale=Vec2(0,0)))
        mouse_origin = mouse.position*camera.fov
    elif held_keys["control"] and key == "s":
        save_world(world)



def update():
    global timer,mouse_origin
    if held_keys["left mouse"]:
        timer += time.dt / 3
        timer = min(timer,1)
    if held_keys["middle mouse"]:
        world.hiding_zones[-1].scale = mouse.position*camera.fov - mouse_origin
    if held_keys["b"]:
        world.bounce_zones[-1].scale = mouse.position*camera.fov - mouse_origin

world = World()

app.run()