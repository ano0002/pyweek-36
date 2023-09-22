from ursina import *

class Button(Button):

    def __init__(self, texture='', highlight_texture='', **kwargs):
        super().__init__(radius=0,**kwargs)
        
        self.default_texture = texture
        self.highlight_texture = highlight_texture
        self.texture = self.default_texture
        
    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.texture = self.highlight_texture


    def on_mouse_exit(self):
        super().on_mouse_exit()
        self.texture = self.default_texture

class Slider(ThinSlider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        def drop():
            self.knob.z = -.1
            if self.setattr:
                if isinstance(self.setattr[0], dict):   # set value of dict
                    self.setattr[0][self.setattr[1]] = self.value
                else:                                   # set value of Entity
                    setattr(self.setattr[0], self.setattr[1], self.value)

            if self.on_value_changed:
                self.on_value_changed(self.value)
        self.knob.drop = drop
        
    def slide(self):
        t = self.knob.x / .5

        if self.step > 0:
            if isinstance(self.step, int) or self.step.is_integer():
                self.knob.text_entity.text = str(self.value)

        if self.dynamic and self._prev_value != t:
            if self.on_value_changed:
                self.on_value_changed(t)

            if self.setattr:
                target_object, attr = self.setattr
                setattr(target_object, attr, self.value)

            self._prev_value = t

        invoke(self._update_text, delay=1/60)



class MainMenu(Entity):
    def __init__(self,play,open_settings, add_to_scene_entities=True, **kwargs):
        super().__init__(parent=camera.ui,add_to_scene_entities=add_to_scene_entities, **kwargs)
        self.play_button = Button(text="",text_origin=Vec2(-.3,0),model="quad",texture="BoutonStartOff",scale=Vec2(.1994,.0392)*3,position=(-.5,-0.15),color=color.white,on_click=self.play,parent=self,highlight_texture="BoutonStartOn")
        self.settings_button = Button(text="",text_origin=Vec2(-.3,0),model="quad",texture="BoutonSettingsOff",scale=Vec2(.1994,.0392)*3,position=(-.5,-.3),color=color.white,on_click=self.open_settings,parent=self,highlight_texture="BoutonSettingsOn")
        self.background = Entity(model="quad",texture="menu",scale=(1*camera.aspect_ratio,1),parent=self,z=1)
        self.play_func = play
        self.settings_func = open_settings
    
    def play(self):
        destroy(self)
        self.play_func()    
    
    def open_settings(self):
        destroy(self)
        self.settings_func()
    
class SettingsMenu(Entity):
    def __init__(self,music,volume_func,on_leave=lambda: print("leaving"), add_to_scene_entities=True, **kwargs):
        super().__init__(parent=camera.ui,add_to_scene_entities=add_to_scene_entities, **kwargs)
        self.background = Entity(model="quad",texture="menu",scale=(1*camera.aspect_ratio,1),parent=self,z=1)
        self.on_leave = on_leave
        self.volume_slider = Slider(min=0, max=1, step=0.01, default=music.volume, dynamic=True, position=(-0.7,-0.2),parent=self, text='Volume', text_origin=(-.3,0), text_scale=0.5, text_offset=(-.1,0), on_value_changed=volume_func,bar_color=color.white)
        self.close_button = Button(model="quad",texture="BoutonCloseOff",scale=Vec2(.1994,.0392)*3,position=(-.5,-.1),on_click=self.leave,parent=self,highlight_texture="BoutonCloseOn",color=color.white,highlight_color=color.gray)

    def input(self,key):
        if key == "escape":
            self.leave()

    def leave(self):
        destroy(self)
        self.on_leave()

class EndScreen(Entity):
    def __init__(self,total_time, add_to_scene_entities=True, **kwargs):
        super().__init__(parent=camera.ui,add_to_scene_entities=add_to_scene_entities, **kwargs)
        self.total_time = total_time
        self.background = Entity(model="quad",texture="end",scale=(1*camera.aspect_ratio,1),parent=self,z=1)
        self.time_text = Text(text=f"Time: {total_time:.2f}s",scale=2,origin=(2,6),parent=self)
        

if __name__ == "__main__":
    
    window.title = 'Hidden in the Shadows'
    app = Ursina()
    
    music = Audio("loop",loop=True, autoplay=True,volume = 0.5)
    
    def play():
        EndScreen(10)
    
    def set_volume(volume):
        music.volume = volume
    
    def open_menu():
        MainMenu(play,open_settings)
    
    def open_settings():
        SettingsMenu(music,set_volume,open_menu)
    
    open_menu()
    
    app.run()