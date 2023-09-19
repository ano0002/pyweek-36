from ursina import *

class Bullet(Entity):
    def __init__(self,world=None, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        
        self.model = 'quad'
        self.color = color.white
        self.scale = 1
        self.world = world
        self.velocity = Vec2(0,0)
    
    def update(self):
        if self.world :
            for asteroid in self.world.asteroids:
                strength = self.world.gravity * asteroid.mass / distance(asteroid,self)**2
                print(Vec2(asteroid.x - self.x,asteroid.y-self.y))
                self.velocity += Vec2(asteroid.x - self.x,asteroid.y-self.y).normalized() * strength * time.dt
                if asteroid != self and distance(self, asteroid) < (self.scale + asteroid.scale) / 2:
                    destroy(self)
                    return
                
        self.position += self.velocity
        

if __name__ == "__main__":
    app = Ursina()
    window.title = 'Hidden in the Shadows'
    camera.orthographic = True
    camera.fov = 100
    
    def input(key):
        if key == "left mouse down":
            bullet = Bullet(position = mouse.position * camera.fov)

    app.run()