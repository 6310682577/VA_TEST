import arcade
import random
import config as cf


def changeSizePxToPt(size):
    return size / 96 * 72

def draw_text_2side_center(text, screen_width, start_y, color, font_size, anchor_x = "center"):
    arcade.draw_text(text, screen_width*0.25, start_y, color, font_size = font_size, anchor_x =anchor_x)
    arcade.draw_text(text, screen_width*0.75, start_y, color, font_size = font_size, anchor_x =anchor_x)

class VRWelcomeView(arcade.View):
    def on_show(self):
        arcade.set_background_color(cf.BG_COLOR)
        self.window.set_mouse_visible(False)
 
    def on_draw(self):
        arcade.start_render()
        _, screen_width, _, screen_height = self.window.get_viewport()
        draw_text_2side_center("Welcome", SCREEN_VR.width, SCREEN_VR.height/2, cf.MAIN_TEXT_COLOR, cf.VR_TEXT_SIZE)

class VRShowTest(arcade.View):
    def __init__(self, window=None, bg_color=cf.BG_COLOR):
        super().__init__(window=window)

        self.totaltime = 0.0
        self.text = ""
        self.side = "Left"
        self.size = 25
        self.color = 0
        self.timeleft = 4.0
        self.appeartime = 0.0
        self.count_round = 0
        self.count_left = 0
        self.count_right = 0
        self.last = ""
        self.last2 = ""

        self.callback = None

    def on_show(self):
        arcade.set_background_color(cf.BG_COLOR)
        self.window.set_mouse_visible(False)

    def on_draw(self):
        arcade.start_render()
        _, screen_width, _, screen_height = self.window.get_viewport()

        # arcade.draw_text((f"{str(self.timeshow)}, {str(self.timeleft)}"), 100, 100, (self.color, self.color, self.color), 30)

        if self.timeleft > 0:
            arcade.draw_text(self.text,
                            screen_width * (0.25 if self.side=='L' else 0.75),
                            screen_height / 2,
                            (self.color, self.color, self.color),
                            changeSizePxToPt(self.size),
                            font_name = 'ETDRS',
                            anchor_x = "center",
                            anchor_y = "center")
        elif self.timeleft <= 0 and not self.callback is None:
            self.callback()
            self.callback = None

    def on_update(self, dt):
        if self.timeleft >= 0.0:
            self.timeleft -= dt

    def show_text(self, text, side="L", size=25, color=0, time=cf.DISAPPEAR_TIME, callback=None):
        self.text = text
        self.side = side
        self.timeleft = time + appeartime
        self.size = size
        self.color = color
        self.callback = callback

class VRFinishTest(arcade.View):
    def __init__(self, window=None, bg_color=cf.BG_COLOR):
        super().__init__(window=window)

    def on_show(self):
        arcade.set_background_color(cf.BG_COLOR)
        self.window.set_mouse_visible(False)
 
    def on_draw(self):
        arcade.start_render()
        _, screen_width, _, screen_height = self.window.get_viewport()
        draw_text_2side_center("Thank you", screen_width, screen_height/2, cf.MAIN_TEXT_COLOR, cf.VR_TEXT_SIZE)