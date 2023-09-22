from ursina import *
from particle import Emiter, Particle
import random

class Bullet(Entity):
    def __init__(self,velocity=Vec2(0),world=None,music=0, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        
        self.texture = 'Vaiseau1.2'
        self.model = 'quad'
        self.color = color.white
        self.scale = 1
        self.world = world
        self.velocity = velocity
        self.emiter = Emiter(rate=0.01,start=lambda : random.random()*2,maxi=lambda : random.random()*1,length=0.1,color=lambda : random.choice((color.yellow,color.red,color.orange)),curve=curve.linear,velocity=-self.velocity)
        self.sound = Audio("rocket",loop=True, autoplay=True,volume=music.volume*0.5)
        self.explosion_sound = Audio("explosion.mp3",loop=False, autoplay=False,volume=music.volume*0.5)
        self.playing = True
        self.music = music
    def update(self):
        if self.playing:
            if self.world :
                for asteroid in self.world.asteroids:
                    strength = self.world.gravity * asteroid.mass / distance_2d(asteroid,self)**2
                    self.velocity += Vec2(asteroid.x - self.x,asteroid.y-self.y).normalized() * strength * time.dt
                    if distance_2d(self, asteroid) < (self.scale + asteroid.scale) / 2:
                        self.destroy()
                        return

                if distance_2d(self, self.world.destination) < (self.scale + self.world.destination.scale) / 2:
                    self.destroy(explosion= False)
                    self.world.end()
                    return
            
            if self.x < -camera.fov*camera.aspect_ratio/2 or self.x > camera.fov*camera.aspect_ratio/2 or self.y < -camera.fov/2 or self.y > camera.fov/2:
                self.destroy()
                return
            
            ray = raycast(self.world_position, Vec3(1,0,0), distance=self.velocity.x+self.scale_x, ignore=(self,))
            if ray.hit:
                self.velocity.x *= -1
            
            ray = raycast(self.world_position, Vec3(-1,0,0), distance=-self.velocity.x+self.scale_x, ignore=(self,))
            if ray.hit:
                self.velocity.x *= -1
            
            ray = raycast(self.world_position, Vec3(0,1,0), distance=self.velocity.y+self.scale_y, ignore=(self,))
            if ray.hit:
                self.velocity.y *= -1
            
            ray = raycast(self.world_position, Vec3(0,-1,0), distance=-self.velocity.y+self.scale_y, ignore=(self,))
            if ray.hit:
                self.velocity.y *= -1
            
            self.position += self.velocity
            self.emiter.position = self.world_position
            self.look_at_2d(self.position+self.velocity)
            self.sound.pitch = 0.5 + self.velocity.length()
            self.sound.volume = self.music.volume*0.5
            self.explosion_sound.volume = self.music.volume*0.5    
    def destroy(self,explosion=True):
        self.world.bullets.remove(self)
        destroy(self.emiter)
        destroy(self.sound)
        if explosion:
            self.explosion_sound.play()
            destroy(self.explosion_sound, delay=self.explosion_sound.length)
            emiter = Emiter(rate=0.1,start=lambda : random.random()*2,maxi=lambda : random.random()*1,length=0.1,color=lambda : random.choice((color.yellow,color.red,color.orange)),curve=curve.linear,velocity=lambda : Vec2(random.random()*2-1,random.random()*2-1))
            emiter.position = self.world_position-Vec3(0,0,1)
            destroy(emiter, delay=self.explosion_sound.length*0.75)
        else:
            destroy(self.explosion_sound)
        destroy(self)
    def pause(self):
        self.playing = not self.playing
        self.emiter.pause()
        if self.sound.playing:
            self.sound.pause()
        else:
            self.sound.play()
if __name__ == "__main__":
    app = Ursina()
    window.title = 'Hidden in the Shadows'
    camera.orthographic = True
    camera.fov = 100
    
    def input(key):
        if key == "left mouse down":
            Bullet(position = mouse.position * camera.fov,velocity=Vec2(random.random()*2-1,random.random()*2-1))

    app.run()
