from ursina import *

class Particle(Entity):
    def __init__(self, pos, start, maxi, length, color=color.hsv(0, 0, 0.3), curve = curve.linear_boomerang,loop=False,velocity = (0,0), **kwargs):
        if callable(color):
            color = color()
        if callable(start):
            start = start()
        if callable(maxi):
            maxi = maxi()
        if callable(length):
            length = length()
        if callable(velocity):
            velocity = velocity()
            
        super().__init__(model="quad",texture="circle",color=color, position=pos, scale=start)
        self.maxi = maxi
        self.animate_scale(maxi, duration=length,
                           curve=curve, loop=loop)
        self.start = time.time()
        self.velocity = Vec2(velocity)
        self.length = length
        for key, value in kwargs.items():
            try :
                setattr(self, key, value)
            except :
                print(key,value)
        
        destroy(self, delay=length)

    def update(self):
        self.position += self.velocity*time.dt
        
class Emiter(Entity):
    def __init__(self,rate, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities)
        self.particles = []
        self.rate = rate
        self.total_time = 0
        self.particle_args = kwargs
        
    def update(self):
        self.total_time += time.dt
        if self.total_time >= self.rate:
            self.total_time = 0
            self.particles.append(Particle(pos=self.world_position, **self.particle_args))
        
    
        
if __name__ == "__main__":
    
    app = Ursina()
    
    def velocity_setter():
        return Vec2(random.random()*2-1,abs(random.random()))
    
    emiter = Emiter(rate=0.1, start=0.5, maxi=1 , length=1, color=color.hsv(0, 0, 0.3),velocity = velocity_setter)
    
    
    camera.orthographic = True
    camera.fov = 100
    
    def update():
        emiter.position = mouse.position * camera.fov
    
    
    app.run()
    