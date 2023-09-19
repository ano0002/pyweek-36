from ursina import *

class Particle(Entity):
    def __init__(self, pos, start, maxi, length, color=color.hsv(0, 0, 0.3), curve = curve.linear_boomerang,loop=False,velocity = (0,0), **kwargs):
        super().__init__(model="quad",texture="circle",color=color, position=pos, scale=start)
        self.maxi = maxi
        self.animate_scale(maxi, duration=length,
                           curve=curve, loop=loop)
        self.start = time.time()
        self.velocity = velocity
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
        super().__init__(add_to_scene_entities, **kwargs)
        self.particles = []
        self.rate = rate
        self.total_time = 0
    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.scale_x == particle.maxi:
                self.particles.remove(particle)
        self.total_time += time.dt
        if self.total_time >= self.rate:
            self.total_time = 0
            self.particles.append(Particle(pos=self.position, start=0.01, maxi=0.1, length=0.5, curve=curve.linear,loop=False,velocity = Vec2(0,0.1)))
        
        
        
if __name__ == "__main__":
    
    app = Ursina()
    
    emiter = Emiter(rate=0.1)
    
    def update():
        emiter.position = mouse.position * camera.fov
    
    
    app.run()
    