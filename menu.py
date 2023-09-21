from ursina import *

class Button(Entity):

    default_color = color.black90
    default_model = None # will default to rounded Quad

    def __init__(self, text='', text_origin=(0,0), **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.disabled = False

        for key, value in kwargs.items():   # set the scale before model for correct corners
            if key in ('scale', 'scale_x', 'scale_y', 'scale_z',
            'world_scale', 'world_scale_x', 'world_scale_y', 'world_scale_z'):

                setattr(self, key, value)

        if Button.default_model is None:
            if not 'model' in kwargs and self.scale[0] != 0 and self.scale[1] != 0:
                self.model = Quad(aspect=self.scale[0] / self.scale[1])
        else:
            self.model = Button.default_model

        if 'color' in kwargs:
            self.color = kwargs['color']
        else:
            self.color = Button.default_color

        self.highlight_color = self.color.tint(.2)
        self.pressed_color = self.color.tint(-.2)
        self.highlight_scale = 1    # multiplier
        self.pressed_scale = 1     # multiplier
        self.collider = 'box'

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.text_entity = None
        if text:
            self.text = text

        self.text_origin = text_origin
        self.original_scale = self.scale


    def input(self, key):
        if self.disabled or not self.model:
            return

        if key == 'left mouse down':
            if self.hovered:
                self.model.setColorScale(self.pressed_color)
                self.model.setScale(Vec3(self.pressed_scale, self.pressed_scale, 1))

        if key == 'left mouse up':
            if self.hovered:
                self.model.setColorScale(self.highlight_color)
                self.model.setScale(Vec3(self.highlight_scale, self.highlight_scale, 1))
            else:
                self.model.setColorScale(self.color)
                self.model.setScale(Vec3(1,1,1))


    def on_mouse_enter(self):
        if not self.disabled and self.model:
            self.model.setColorScale(self.highlight_color)

            if self.highlight_scale != 1:
                self.model.setScale(Vec3(self.highlight_scale, self.highlight_scale, 1))

        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.enabled = True


    def on_mouse_exit(self):
        if not self.disabled and self.model:
            self.model.setColorScale(self.color)

            if not mouse.left and self.highlight_scale != 1:
                self.model.setScale(Vec3(1,1,1))

        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.enabled = False



class MainMenu(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        
        self.play_button = Button(text="Play",scale=0.1,position=(0,0.1))
        self.settings_button = Button(text="Settings",scale=0.1,position=(0,-0.1))
        
class SettingsMenu(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)

if __name__ == "__main__":
    
    window.title = 'Hidden in the Shadows'
    app = Ursina()
    
    menu = MainMenu()
    
    app.run()