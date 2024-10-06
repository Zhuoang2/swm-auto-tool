import asyncio

import sha
from sha.points import *
from time import sleep
from threading import Thread

from pynput import keyboard
from concurrent.futures import ThreadPoolExecutor

SUPER_CLICK = False
EXECUTOR = ThreadPoolExecutor(max_workers=1)

__doc__ = """
沙威玛传奇辅助工具

按下 ESC 退出
按下 p 打印鼠标位置

按下 TAB 或者 d 开启/关闭连点。无论在进行哪一项操作，只要激活连点，就会中断当前的脚本操作，立即切换鼠标连点

按下 q 一键添加四个菜，卷饼，点机器打包。（需要解锁：自动刮肉，自动飞饼，一键打包）
按下 w 点击炸薯条，一键把炸好的薯条放到桌子上
按下 e 一键炸薯条，此操作会同时收钱+点薯条，防止小偷+防止锅内已有薯条无法炸
按下 a 点击老板，备货（需要解锁：员工培训）

按下 c 滑动桌子，自动收钱
按下 z 移动到饮料，方便拿
按下 x 移动到地瓜，方便拿

"""


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


def handle_4_dishes():
    for p in [POS_DISH_1, POS_DISH_2, POS_DISH_3, POS_DISH_4]:
        if SUPER_CLICK:
            return
        sha.click(p, 3)
        print(f'Dish {p} clicked')
    sleep(.4)
    if SUPER_CLICK:
        return
    sha.swipe(POS_CAKE_BOTTOM, POS_CAKE_TOP, 0.2)
    if SUPER_CLICK:
        return
    print('Cake swiped')
    sleep(.05)
    sha.click(POS_WRAPPING_MACHINE, 3, 0.08)
    if SUPER_CLICK:
        return
    print('Wrapping machine clicked')
    sha.move_to(POS_TABLE_CENTER)


def handle_fry_potato():
    sha.swipe(POS_TABLE_LEFT, POS_TABLE_RIGHT, .2)
    sha.click(POS_POTATO_FRY, 2)
    sha.click_hold(POS_POTATO, 3)
    print('Potato clicked')
    sha.move_to(POS_TABLE_CENTER)


def handle_swipte_table():
    sha.swipe(POS_TABLE_LEFT, POS_TABLE_RIGHT, .2)
    print('Table swiped')
    sha.move_to(POS_TABLE_CENTER)


async def handle_key_press(key):
    try:
        if key.char == 'p':
            sha.print_mouse()

        elif key.char == 'a':
            await sha.click(POS_BOSS, 2)
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'q':
            EXECUTOR.submit(handle_4_dishes)

        elif key.char == 'w':
            await sha.click_async(POS_POTATO_FRY, 4)
            print('Potato fry clicked')
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'e':
            EXECUTOR.submit(handle_fry_potato)

        elif key.char == 'c':
            EXECUTOR.submit(handle_swipte_table)

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


async def handle_key_release(key):
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


def on_press(key):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(handle_key_press(key))
    return asyncio.run(handle_key_press(key))


def on_release(key):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(handle_key_release(key))
    return asyncio.run(handle_key_release(key))


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
    print(__doc__)
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
