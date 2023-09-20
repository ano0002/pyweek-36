from ursina import *
from particle import Emiter, Particle
import random

def is_in_rect(rect, point,radius=0):
    print(point.x,rect.left - radius,point.x,rect.right + radius,point.y,rect.bottom - radius,point.y,rect.top + radius)
    if point.x > rect.left - radius and point.x < rect.right + radius and point.y > rect.bottom - radius and point.y < rect.top + radius:
        return True
    return False

def get_closest_rect_side(rect, point):
    closest_side = 0
    closest_distance = abs(rect.left - point.x)
    if abs(rect.right - point.x) < closest_distance:
        closest_side = 1
        closest_distance = abs(rect.right - point.x)
    if abs(rect.top - point.y) < closest_distance:
        closest_side = 2
        closest_distance = abs(rect.top - point.y)
    if abs(rect.bottom - point.y) < closest_distance:
        closest_side = 3
        closest_distance = abs(rect.bottom - point.y)
    return closest_side

class Rect:
    def __init__(self,pos,scale) -> None:
        self.left = pos.x 
        self.right = pos.x + scale.x
        self.top = pos.y 
        self.bottom = pos.y - scale.y

class Bullet(Entity):
    def __init__(self,velocity=Vec2(0),world=None, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        
        self.model = 'quad'
        self.color = color.white
        self.scale = 1
        self.world = world
        self.velocity = velocity
        self.emiter = Emiter(rate=0.01,start=lambda : random.random()*2,maxi=lambda : random.random()*1,length=0.1,color=lambda : random.choice((color.yellow,color.red,color.orange)),curve=curve.linear,velocity=-self.velocity)
    
    def update(self):
        if self.world :
            for asteroid in self.world.asteroids:
                strength = self.world.gravity * asteroid.mass / distance_2d(asteroid,self)**2
                self.velocity += Vec2(asteroid.x - self.x,asteroid.y-self.y).normalized() * strength * time.dt
                if distance_2d(self, asteroid) < (self.scale + asteroid.scale) / 2:
                    self.destroy()
                    return

            if distance_2d(self, self.world.destination) < (self.scale + self.world.destination.scale) / 2:
                self.destroy()
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
        
    def destroy(self):
        destroy(self.emiter)
        destroy(self)

if __name__ == "__main__":
    app = Ursina()
    window.title = 'Hidden in the Shadows'
    camera.orthographic = True
    camera.fov = 100
    
    def input(key):
        if key == "left mouse down":
            Bullet(position = mouse.position * camera.fov,velocity=Vec2(random.random()*2-1,random.random()*2-1))

    app.run()