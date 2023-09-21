from ursina import *

class MainMenu(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(parent=camera.ui,add_to_scene_entities=add_to_scene_entities, **kwargs)
        
        self.play_button = Button(text="Play",text_origin=Vec2(-.3,0),model="quad",texture="button",scale=(.3,.1),position=(-.5,-0.15),color=color.white)
        self.settings_button = Button(text="Settings",text_origin=Vec2(-.3,0),model="quad",texture="button",scale=(.3,.1),position=(-.5,-.3),color=color.white)
        
class SettingsMenu(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)

if __name__ == "__main__":
    
    window.title = 'Hidden in the Shadows'
    app = Ursina()
    
    menu = MainMenu()
    
    app.run()