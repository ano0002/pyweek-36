from ursina import *

class MainMenu(Entity):
    def __init__(self,play,open_settings, add_to_scene_entities=True, **kwargs):
        super().__init__(parent=camera.ui,add_to_scene_entities=add_to_scene_entities, **kwargs)
        self.play_button = Button(text="Play",text_origin=Vec2(-.3,0),model="quad",texture="button",scale=(.3,.1),position=(-.5,-0.15),color=color.white,highlight_scale=1.05,on_click=self.play,parent=self)
        self.settings_button = Button(text="Settings",text_origin=Vec2(-.3,0),model="quad",texture="button",scale=(.3,.1),position=(-.5,-.3),color=color.white,highlight_scale=1.05,on_click=self.open_settings,parent=self)
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
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)

if __name__ == "__main__":
    
    window.title = 'Hidden in the Shadows'
    app = Ursina()
    def play():
        print("play")
    
    def open_settings():
        print("settings")
    
    menu = MainMenu(play,open_settings)
    
    app.run()