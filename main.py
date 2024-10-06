import sha
from sha.points import *
from time import sleep
from threading import Thread

from pynput import keyboard

SUPER_CLICK = False


def enable_super_click():
    global SUPER_CLICK
    sha.FAILSAFE = True
    sha.mouse_up()
    SUPER_CLICK = True
    print('Super click: {0}'.format(
        SUPER_CLICK))


def disable_super_click():
    global SUPER_CLICK
    SUPER_CLICK = False
    sha.FAILSAFE = False
    print('Super click: {0}'.format(
        SUPER_CLICK))


def on_press(key):
    try:
        if key.char == 'p':
            sha.print_mouse()

        elif key.char == 'a':
            sha.click(POS_BOSS, 2)
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'q':
            sha.click(POS_DISH_1, 3)
            print('Dish 1 clicked')
            sha.click(POS_DISH_2, 3)
            print('Dish 2 clicked')
            sha.click(POS_DISH_3, 3)
            print('Dish 3 clicked')
            sha.click(POS_DISH_4, 3)
            print('Dish 4 clicked')
            sleep(.4)
            sha.swipe(POS_CAKE_BOTTOM, POS_CAKE_TOP, 0.2)
            print('Cake swiped')
            sleep(.05)
            sha.click(POS_WRAPPING_MACHINE, 3, 0.08)
            print('Wrapping machine clicked')
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'w':
            sha.click(POS_POTATO_FRY, 4)
            print('Potato fry clicked')
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'e':
            sha.click_hold(POS_POTATO, 3)
            print('Potato clicked')
            sha.click(POS_POTATO_FRY, 1)
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'c':
            sha.swipe(POS_TABLE_LEFT, POS_TABLE_RIGHT, .3)
            print('Table swiped')
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'd':
            enable_super_click()

        elif key.char == 'z':
            sha.move_to(POS_DRINK)
        elif key.char == 'x':
            sha.move_to(POS_DIGUA)

    except AttributeError:
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        # tab
        elif key == keyboard.Key.tab:
            enable_super_click()


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    # tab
    elif key == keyboard.Key.tab:
        disable_super_click()
    # d
    try:
        if key.char == 'd':
            disable_super_click()
    except AttributeError:
        pass


def super_click_thread():
    print('Super click thread started')
    while True:
        if SUPER_CLICK:
            sha.click_no_pos()
            sleep(0.05)
        else:
            sleep(0.05)


if __name__ == '__main__':
    # Start super click thread
    Thread(target=super_click_thread, daemon=True).start()

    print('Press "p" to print mouse position')
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
