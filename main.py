from bullet import Bullet
from menu import MainMenu,EndScreen,SettingsMenu

from ursina import *
from ursina.shaders.screenspace_shaders.fxaa import fxaa_shader

import json

window.title = 'Hidden in the Shadows'
app = Ursina()

camera.shader = fxaa_shader

camera.orthographic = True

camera.fov = 100



class World(Entity):
    def __init__(self,file,gravity=15,asteroids = [],start_texture="1start",end_texture="2start",end = lambda: print("end"), **kwargs):
        super().__init__(**kwargs)
        self.gravity = gravity
        self.asteroids = asteroids
        self.on_end = end
        self.shoot = False
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
        self.start_display = Entity(model="quad",texture=start_texture, scale=self.start.scale, position=self.start.position)
        self.destination = Entity(model="quad",texture=end_texture, scale=10, position=(Vec2(40*camera.aspect_ratio,35)))
        self.arrow = Entity(parent= self.start, model="quad",texture="arrow",scale=0.3, scale_x=0.7,z=0.1,rotation_z=-90,origin=(-0.5,0))
        
    def add_planet(self, asteroid):
        self.asteroids.append(asteroid)

    def add_hiding_zone(self, hiding_zone):
        self.hiding_zones.append(hiding_zone)

    def update(self):
        if held_keys["left mouse"] and self.shoot:
            self.timer += time.dt / 3
            self.timer = min(self.timer,1)
            self.arrow.scale_x = self.timer + 0.7
        else:
            self.arrow.scale_x = 0.7
            self.start.look_at_2d(mouse.position*camera.fov)
        
    def destroy(self):
        for asteroid in self.asteroids:
            destroy(asteroid)
        for hiding_zone in self.hiding_zones:
            destroy(hiding_zone)
        for bounce_zone in self.bounce_zones:
            destroy(bounce_zone)
        for bullet in self.bullets:
            bullet.destroy()
        destroy(self.start)
        destroy(self.destination)
        destroy(self.arrow)
        destroy(self.start_display)
        destroy(self)
        
    def end(self):
        self.destroy()
        self.on_end()

    def input(self,key):
        if key == "left mouse down" and not self.shoot:
            self.shoot = True
            self.direction = (mouse.position*camera.fov-self.start.position).normalized()
            self.timer = 0
        elif key == "left mouse up" and self.shoot:
            self.shoot = False
            velocity = self.direction*self.timer
            velocity = Vec2(velocity.x,velocity.y)
            self.bullets.append(Bullet(position=self.start.position+self.direction*self.start.scale/2,velocity=velocity,world=self))

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
        



if __name__ == "__main__":
    music = Audio("loop",loop=True, autoplay=False)


    background = Entity(model="quad",texture="space",scale=Vec2(100*camera.aspect_ratio,100),z=10)

    total_time = 0
    
    def load_world(number):
        if number < 10:
            World(f"world{number}.json",end= lambda: load_world(number+1),start_texture=f"{number}start",end_texture=f"{number+1}start")
        else:
            EndScreen(total_time)    
        
    def start():
        global total_time
        World("world1.json",end= lambda: load_world(2))
        music.play()
        total_time = 0

    def update():
        global total_time
        total_time += time.dt
    
    def set_volume(volume):
        music.volume = volume
    
    def settings():
        SettingsMenu(set_volume)

    MainMenu(start,settings)


    app.run()