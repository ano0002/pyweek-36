from bullet import Bullet
from menu import MainMenu,EndScreen,SettingsMenu
from random import randint

from ursina import *
from ursina.shaders.screenspace_shaders.fxaa import fxaa_shader

import json,random

window.title = 'Hidden in the Shadows'
app = Ursina()

camera.shader = fxaa_shader

camera.orthographic = True

camera.fov = 100



class World(Entity):
    def __init__(self,file,gravity=15,background="space",start_texture="1start",end_texture="2start",end = lambda: print("end"), **kwargs):
        super().__init__(**kwargs)
        self.gravity = gravity
        self.asteroids = []
        self.on_end = end
        self.shoot = False
        self.hiding_zones = []
        self.bullets = []
        self.bounce_zones = []
        data = json.load(open(file))
        for asteroid in data["asteroids"]:
            self.add_planet(Asteroid(mass=asteroid["mass"],position=Vec3(asteroid["x"],asteroid["y"],-1),world=self))
        for hiding_zone in data["hiding_zones"]:
            self.add_hiding_zone(HidingZone(position=Vec2(hiding_zone["x"],hiding_zone["y"]),scale=Vec2(hiding_zone["scale_x"],hiding_zone["scale_y"])))
        for bounce_zone in data["bounce_zones"]:
            self.bounce_zones.append(BounceZone(position=Vec2(bounce_zone["x"],bounce_zone["y"]),scale=Vec2(bounce_zone["scale_x"],bounce_zone["scale_y"])))
        self.start = Entity(scale=10, position=Vec2(-40*camera.aspect_ratio,-35))
        self.start_display = Entity(model="quad",texture=start_texture, scale=self.start.scale, position=self.start.position)
        self.destination = Entity(model="quad",texture=end_texture, scale=10, position=(Vec2(40*camera.aspect_ratio,35)))
        self.arrow = Entity(parent= self.start, model="quad",texture="arrow",scale=0.3, scale_x=0.7,z=0.1,rotation_z=-90,origin=(-0.5,0))
        self.background = Entity(model="quad",texture=background,scale=Vec2(100*camera.aspect_ratio,100),z=10)
        
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
        destroy(self.background)
        
    def end(self):
        self.destroy()
        self.on_end()

    def toggle_menu(self):
        for bullet in self.bullets:
            bullet.pause()
        if hasattr(self,"settings") and self.settings != None:
            destroy(self.settings)
            self.settings = None
        else:
            self.settings = SettingsMenu(game_music,set_volume,lambda: print("leaving"))
        


    def input(self,key):
        if key == "left mouse down" and not self.shoot:
            self.shoot = True
            self.direction = (mouse.position*camera.fov-self.start.position).normalized()
            self.timer = 0
        elif key == "left mouse up" and self.shoot:
            self.shoot = False
            velocity = self.direction*self.timer
            velocity = Vec2(velocity.x,velocity.y)
            self.bullets.append(Bullet(position=self.start.position+self.direction*self.start.scale/2,velocity=velocity,world=self,music=game_music))
        elif key == "escape":
            self.toggle_menu()
class Asteroid(Entity):
    def __init__(self,mass,position,world=None, **kwargs):
        super().__init__(**kwargs)
        self.model = "quad"
        self.texture = "asteroid"+str(randint(0,2))
        self.scale = 3*mass**0.7
        self.position = position
        self.mass = mass
        self.world = world
        self.rotation_speed = randint(-45, 45)  # Random initial rotation speed in degrees per second

    def update(self):
        # Update the rotation of the asteroid based on its rotation speed
        self.rotation_z += self.rotation_speed * time.dt
        # Ensure that the rotation stays within 360 degrees
        self.rotation_z %= 360


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
        self.scale = scale
        self.position = Vec3(*position,0)
        self.origin= Vec2(-0.5,-0.5)
        self.collider = "box"
        



if __name__ == "__main__":
    game_music = Audio("loop",loop=True, autoplay=False,volume=0.5)

    click_sound = Audio("click",loop=False, autoplay=False,volume=0.5)

    total_time = 0
    
    def load_world(number):
        if number < 10:
            World(f"world{number}.json",end= lambda: load_world(number+1),start_texture=f"{number}start",end_texture=f"{number+1}start")
        else:
            EndScreen(total_time)    
        
    def start():
        global total_time
        click_sound.play()
        World("world1.json",end= lambda: load_world(2))
        game_music.play()
        total_time = 0

    def update():
        global total_time
        total_time += time.dt
        camera.set_shader_input("window_size", window.size)
    
    def set_volume(volume):
        game_music.volume = volume
        click_sound.volume = volume*1.5
    
    def settings():
        click_sound.play()
        SettingsMenu(game_music,set_volume,open_menu)

    def open_menu():
        click_sound.play()
        MainMenu(start,settings)

    open_menu()

    app.run()