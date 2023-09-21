from ursina import *


class MainMenu(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        
        self.play_button = Button(text="Play",text_origin=Vec2(-.3,0),model="quad",texture="button",scale=(.3,.1),position=(0,0.1),color=color.white)
        self.settings_button = Button(text="Settings",scale=0.1,position=(0,-0.1))
        
class SettingsMenu(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)

if __name__ == "__main__":
    
    window.title = 'Hidden in the Shadows'
    app = Ursina()
    
    menu = MainMenu()
    
    app.run()