import arcade
import string
import random
import config as cf
import numpy as np
import createData

from VR_Screen import VRWelcomeView, VRShowTest, VRFinishTest

def createTest():
    test_list = []
    length = len(cf.SIZE_LIST) * cf.SUB_ROUND
    half_length = length//2

    for size in cf.SIZE_LIST:
        side_list = np.random.permutation(['L']*half_length + ['R']*(length-half_length))
        char_list = np.random.choice(["E","W","F", "M"], size=(length,))
        size_list = (size,)*length

        test_list.extend(list(zip(char_list, side_list, size_list)))

    return test_list

def appeartime():
    return random.randint(2 , 4)

def calculate_score(score):
    snellen_va = " "
    if score > 23 and score <= 25:
        snellen_va = "20/40 or better"
    elif score > 18:
        snellen_va = "20/80"
    elif score > 13:
        snellen_va = "20/120"
    elif score > 8:
        snellen_va = "20/160"
    elif score > 3:
        snellen_va = "20/200"
    else:
        pass
    return snellen_va

def randomuser(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class StartMenuView(arcade.View):
    def __init__(self, window_vr, window=None):
        super().__init__(window=window)

        self.selected = 1
        self.user = randomuser()
        self.test_list = createTest()

        self.startColor = (0, 0, 0)
        self.settingColor = (125, 125, 125)
        self.quitColor = (125, 125, 125)

        self.window_vr = window_vr
        self.vr_welcome_view = VRWelcomeView(window=window_vr)

    def on_show(self):
        arcade.set_background_color(cf.BG_COLOR)
        self.window.set_mouse_visible(False)
        self.window_vr.show_view(self.vr_welcome_view)

    def on_draw(self):
        arcade.start_render()

        _, screen_width, _, screen_height = self.window.get_viewport()

        # menu text
        arcade.draw_text("Start", screen_width / 2, screen_height / 2 + 100, self.startColor,
                         cf.TEXT_SIZE , anchor_x = "center", anchor_y = "center")

        arcade.draw_text("Setting", screen_width / 2, screen_height / 2, self.settingColor,
                         cf.TEXT_SIZE , anchor_x = "center", anchor_y = "center")

        arcade.draw_text("Quit", screen_width / 2, screen_height / 2 - 100, self.quitColor,
                         cf.TEXT_SIZE , anchor_x = "center", anchor_y = "center")     

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

        if symbol == arcade.key.DOWN or symbol == arcade.key.S or symbol == cf.KEY_DOWN:
            if self.selected < 3:
                self.selected += 1
        elif symbol == arcade.key.UP or symbol == arcade.key.W or symbol == cf.KEY_UP:
            if self.selected > 1:
                self.selected -= 1
        else:
            pass

        self.startColor = ((0, 0, 0) if self.selected == 1 else (125, 125, 125))
        self.settingColor = ((0, 0, 0) if self.selected == 2 else (125, 125, 125))
        self.quitColor = ((0, 0, 0) if self.selected == 3 else (125, 125, 125))

        if symbol == arcade.key.ENTER or symbol == cf.KEY_ENTER:
            if self.selected == 1:
                test_view = OnTestView(self.window_vr)

                test_view.user = self.user
                test_view.test = self.test_list

                self.window.show_view(test_view)
            elif self.selected == 2:
                pass
                setting_view = SettingView(self.window_vr)
                self.window.show_view(setting_view)
            elif self.selected == 3:
                arcade.exit()

class SettingView(arcade.View):
    def __init__(self, window_vr, window=None):
        super().__init__(window=window)

        self.selected = 1
        self.fs_mode = "ON" if self.window.fullscreen else "OFF"

        self.window_vr = window_vr
        self.vr_welcome_view = VRWelcomeView(window=window_vr)

        self.fsColor = (0, 0, 0)
        self.backColor = (125, 125, 125)

    def on_show(self):
        arcade.set_background_color(cf.BG_COLOR)

    def on_draw(self):
        arcade.start_render()

        left, screen_width, bottom, screen_height = self.window.get_viewport()

        # menu text
        arcade.draw_text(f"Full screen mode : {self.fs_mode}", screen_width / 2, screen_height / 2 + 100, self.fsColor,
                         cf.TEXT_SIZE , anchor_x = "center", anchor_y = "center")

        arcade.draw_text("Back", screen_width / 2, screen_height / 10, self.backColor, cf.TEXT_SIZE, anchor_x = "center", anchor_y = "center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

        if symbol == arcade.key.DOWN or symbol == arcade.key.S:
            if self.selected < 2:
                self.selected += 1
        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            if self.selected > 1:
                self.selected -= 1
        
        self.fsColor = (0, 0, 0) if self.selected == 1 else (125, 125, 125)
        self.backColor = (0, 0, 0) if self.selected == 2 else (125, 125, 125)

        if symbol == arcade.key.ENTER:
            if self.selected == 1:
                SCREEN = arcade.get_screens()

                self.window.set_fullscreen(not self.window.fullscreen)
                self.vr_welcome_view.window.set_fullscreen(self.window.fullscreen)
                self.vr_welcome_view.window.set_location(SCREEN[1].x, 0)
                self.window.set_location(0, 0)

                self.fs_mode = "ON" if self.window.fullscreen == True else "OFF"

            elif self.selected == 2:
                StartMenu = StartMenuView(self.window_vr)
                self.window.show_view(StartMenu)

class OnTestView(arcade.View):
    def __init__(self, window_vr, window=None):
        super().__init__(window=window)

        self.user = ""
        self.test = []
        self.window_vr = window_vr
        self.vr_show_welcome = VRWelcomeView(window=window_vr)
        self.vr_show_test = VRShowTest(window=window_vr)
        self.vr_finish_test = VRFinishTest(window=window_vr)
        self.side = " "

        self.round = 0
        self.appeartime = 0
        self.total_test_time = -1
        self.score = 0

    def on_show(self):
        arcade.set_background_color(cf.BG_COLOR)
        self.window_vr.show_view(self.vr_show_welcome)

    def on_draw(self):
        arcade.start_render()

        _, screen_width, _, screen_height = self.window.get_viewport()

        arcade.draw_text(f"Overall Progress {self.round}/{len(self.test)}",
                         screen_width//2,
                         screen_height//2,
                         cf.MAIN_TEXT_COLOR,
                         cf.TEXT_SIZE,
                         anchor_x = "center",
                         anchor_y = "center")

    def on_update(self, dt):
        pass
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

        if symbol == arcade.key.ENTER or symbol == cf.KEY_ENTER:
            self.window_vr.show_view(self.vr_show_test)
            if self.total_test_time < 0:
                self.total_test_time = 0

        if symbol == arcade.key.W or symbol == arcade.key.UP or symbol == cf.KEY_UP:
            click = 'W'
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT or symbol == cf.KEY_LEFT:
            click = 'F'
        elif symbol == arcade.key.S or symbol == arcade.key.DOWN or symbol == cf.KEY_DOWN:
            click = 'M'
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT or symbol == cf.KEY_RIGHT:
            click = 'E'
        else:
            click = 'XXX'
        
        self.vr_show_test.show_text(self.test[self.round - 1][0], self.test[self.round - 1][1], self.test[self.round - 1][2], time=6)
        self.round += 1

        if self.round >= len(self.test):

            self.window_vr.show_view(self.vr_finish_test)
            finish_view = FinishTestView(self.window_vr)

            finish_view.test = self.test
            finish_view.total_test_time = self.total_test_time

            finish_view.window.show_view(finish_view)

class FinishTestView(arcade.View):
    def __init__(self, window_vr, window=None):
        super().__init__(window=window)

        self.save_text = "Press S to save data"
        self.save = False
        self.user = ""
        self.test = []

        self.total_test_time = 0
        self.score = 0

    def on_show(self):
        arcade.set_background_color(cf.BG_COLOR)
 
    def on_draw(self):
        arcade.start_render()
        _, screen_width, _, screen_height = self.window.get_viewport()

        arcade.draw_text("Results", screen_width / 2, screen_height * 7 / 10, MAIN_TEXT_COLOR, font_size = 30, anchor_x = "center")

        arcade.draw_text(f"VA Left eye = {calculate_score(self.left_score)}",
                             screen_width / 2,
                             screen_height / 2 + 60,
                             cf.MAIN_TEXT_COLOR,
                             cf.TEXT_SIZE,
                             anchor_x = "center")

        arcade.draw_text(f"(answered correctly {self.left_score} out of {(len(cf.SIZE_LIST) * cf.SUB_ROUND) // 2})",
                             screen_width / 2,
                             screen_height / 2 + 20,
                             cf.MAIN_TEXT_COLOR,
                             cf.TEXT_SIZE,
                             anchor_x = "center")
        
        arcade.draw_text(f"VA Right eye = {calculate_score(self.right_score)}",
                             screen_width / 2,
                             screen_height / 2 - 40,
                             cf.MAIN_TEXT_COLOR,
                             cf.TEXT_SIZE,
                             anchor_x = "center")

        arcade.draw_text(f"(answered correctly {self.right_score} out of {(len(cf.SIZE_LIST) * cf.SUB_ROUND) // 2})",
                             screen_width / 2,
                             screen_height / 2 - 80,
                             cf.MAIN_TEXT_COLOR,
                             cf.TEXT_SIZE,
                             anchor_x = "center")

        arcade.draw_text(self.save_text,
                             screen_width * 0.1,
                             screen_height * 0.1,
                             cf.MAIN_TEXT_COLOR,
                             cf.TEXT_SIZE,)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

        if symbol == arcade.key.S and self.save == False:
            createData.appendData(Name = self.user, E_List = self.E_letter_list, E_correct_List = self.E_correction_list,
                                 VA_left = calculate_score(self.left_score), VA_right = calculate_score(self.right_score),
                                 E_Lt_List = self.E_letter_left_list, E_correct_Lt_List = self.E_correction_left_list,
                                 E_Rt_List = self.E_letter_right_list, E_correct_Rt_List = self.E_correction_right_list,
                                 Response_time_left = self.response_time_left, Response_time_right = self.response_time_right,
                                 total_time = self.total_test_time)
            self.save_text = "Data is saved"
            self.save == True