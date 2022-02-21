import arcade
import config as cf

from Officer_Screen import StartMenuView

# Screen
SCREEN = arcade.get_screens()

if __name__ == "__main__":
    if len(SCREEN) == 1:
        window_vr = arcade.Window(SCREEN[0].width//2, SCREEN[0].height//2, "Reaction time Test VR", fullscreen = True, resizable=True, screen=SCREEN[0])
        window_officer = arcade.Window(SCREEN[0].width//2, SCREEN[0].height//2, "Reaction time Test VR", fullscreen = True, resizable=True,screen=SCREEN[0])
    else:
        window_vr = arcade.Window(SCREEN[1].width, SCREEN[1].height, "VA Test Vr", fullscreen = True, update_rate=1/cf.FPS, screen=SCREEN[1])
        window_vr.set_location(SCREEN[1].x, 0)

        window_officer = arcade.Window(SCREEN[0].width, SCREEN[0].height, "VA Test Main", fullscreen = True, update_rate=1/cf.FPS, screen=SCREEN[0])
        window_officer.set_location(0, 0)

    
    main_view = StartMenuView(window=window_officer, window_vr=window_vr)
    window_officer.show_view(main_view)
    
    arcade.run()
