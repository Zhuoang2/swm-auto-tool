import asyncio
import time
from typing import Tuple

import sha
from sha.points import *
from config import *
from time import sleep
from threading import Thread

from pynput import keyboard
from concurrent.futures import ThreadPoolExecutor

SUPER_CLICK = False
EXECUTOR = ThreadPoolExecutor(max_workers=1)

__doc__ = """
沙威玛传奇辅助工具

按下 ESC，Alt，Windows 中的任何键即退出，防止在其他程序内启用脚本。

按下 p 打印鼠标位置

按下 TAB 或者 d 开启连点，松开关闭。
无论在进行哪一项操作，只要激活连点，就会中断当前的脚本操作，立即切换鼠标连点（方便点小偷）

按下 q 一键添加四个菜，卷饼，加酱料，点机器打包。（需要解锁：自动刮肉，自动飞饼，一键打包）
按下 w 点击炸薯条，一键把炸好的薯条放到桌子上
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
    print('打开连点: {0}'.format(
        SUPER_CLICK))


def disable_super_click():
    global SUPER_CLICK
    SUPER_CLICK = False
    sha.FAILSAFE = False
    print('关闭连点: {0}'.format(
        SUPER_CLICK))


def action_add_4_dish():
    """
    一键添加四个菜
    :return:
    """
    # add dish
    print('[1] 一键添加四种酱料开始')
    for p in [POS_DISH_1, POS_DISH_2, POS_DISH_3, POS_DISH_4]:
        if SUPER_CLICK:
            return
        sha.click(p, DISH_CLICK_COUNT)
        print(f'[1] 酱料位置 {p} 完成')
    if SUPER_CLICK:
        return


def action_add_sauce(is_swipe=False):
    """
    添加石榴汁
    :return:
    """
    # just click first
    print('[2] 左下角酱汁开始')
    sha.move_to(POS_SHILIU)
    if is_swipe:
        if SUPER_CLICK:
            return
        sha.click(POS_SHILIU, 1)
        sleep(.1)
        sha.swipe(POS_SHILIU, POS_CACE_CENTER, 0.4)
        print('[2] 左下角酱汁滑动完成')
        if SUPER_CLICK:
            return
        # sleep(1)
    else:
        sleep(.05)
        sha.click(POS_SHILIU, 2)
        # sleep(1)
        print('[2] 左下角酱汁点击完成')


def action_roll_pancake():
    """
    卷饼
    :return:
    """
    sha.swipe(POS_CAKE_BOTTOM, POS_CAKE_TOP, 0.2)
    print('[-] 卷饼操作完成')


def action_wrap_pancake():
    """
    打包
    :return:
    """
    sha.click(POS_WRAPPING_MACHINE, 3, 0.08)
    print('[-] 打包操作完成')


def action_fry_potato():
    """
    炸薯条
    :return:
    """
    sha.swipe(POS_TABLE_LEFT, POS_TABLE_RIGHT, .2)
    print('[5] 炸土豆前战术性收钱已完成')
    action_click_potato_pot(2)
    sleep(.2)
    sha.click(POS_POTATO)
    sleep(.2)
    print(f'[5] 开始切土豆，需要切：{int(POTATO_CUT_TIME * 10) * 0.1} 秒')
    sha.click_hold(POS_POTATO, POTATO_CUT_TIME)
    sha.move_to(POS_TABLE_CENTER)
    print('[5] 土豆切割+炸土豆完成')


def action_click_potato_pot(cnt=1):
    sha.click(POS_POTATO_FRY, cnt)
    print(f'[-] 点击炸好的土豆 {cnt} 次')


def action_boss_add_atock():
    sha.click(POS_BOSS, 1)
    print('[-] 老板备货完成')


def action_click_coca_machine():
    sha.click(POS_COCA_1, 1)
    sha.click(POS_COCA_2, 1)
    print('[-] 可乐机点击完成')


def super_add_dish_sauce_pack():
    """
    一键添加四个菜，卷饼，点机器打包
    :return:
    """
    print('=' * 20)
    print('一键添加四个菜，卷饼，加酱料，点机器打包')
    t1 = time.time()
    # add sauce
    action_add_sauce()
    if SUPER_CLICK:
        return
    # add stock
    action_boss_add_atock()
    # add 4 dish
    action_add_4_dish()
    if SUPER_CLICK:
        return
    #sleep(.2)
    # click potato
    action_click_potato_pot()
    # click coca machine
    action_click_coca_machine()
    # roll the pancake
    action_roll_pancake()
    if SUPER_CLICK:
        return
    # while waiting for pancake, we clean the table
    # handle_swipte_table()
    # wrap
    # action_wrap_pancake()
    if SUPER_CLICK:
        return
    sha.move_to(POS_TABLE_CENTER)
    print('-' * 20)
    print(f'耗时 {time.time() - t1:.2f} 秒')


def super_fry_potato():
    """
    一键炸薯条，升级了自动切薯条的话，此函数不需要
    :return:
    """
    action_fry_potato()


def handle_swipte_table():
    print('[6] 开始滑动桌子收钱')
    sha.swipe(POS_TABLE_LEFT, POS_TABLE_RIGHT, .4)
    print('[6] 滑动桌子收钱完成')
    sha.move_to(POS_TABLE_CENTER)


def __feed_guest(guest_pos: Tuple[int, int]) -> None:
    print(f'[7] 喂食客人 {guest_pos}')
    sha.swipe(POS_DRINK, guest_pos, .15)
    sleep(.1)
    sha.swipe(POS_DRINK, guest_pos, .15)
    print(f'[7] 盒装饮料 {guest_pos}')
    if SUPER_CLICK:
        return
    sha.swipe(POS_DIGUA, guest_pos, .12)
    sha.swipe(POS_DIGUA, guest_pos, .12)
    print(f'[7] 地瓜 {guest_pos}')
    if SUPER_CLICK:
        return
    sha.swipe(POS_TABLE_CENTER, guest_pos, .1)
    sha.swipe(POS_TABLE_CENTER, guest_pos, .1)
    print(f'[7] 卷饼 {guest_pos}')
    if SUPER_CLICK:
        return
    sha.swipe(POS_COCA_CUP_1, guest_pos, .14)
    sleep(0.2)
    sha.swipe(POS_COCA_CUP_2, guest_pos, .14)
    print(f'[7] 可乐 {guest_pos}')
    action_click_coca_machine()
    for i in (POS_FRY_1,POS_FRY_2,):
        sha.swipe(i, guest_pos, .15)
    print(f'[7] 薯条 {guest_pos}')
    print(f'[7] 客人 {guest_pos} 喂食完成')


def feed_guest(guest_pos: Tuple[int, int]) -> None:
    Thread(target=__feed_guest, args=(guest_pos,), daemon=True).start()


async def handle_key_press(key):
    if key in {keyboard.Key.esc, keyboard.Key.alt, keyboard.Key.cmd}:
        # Stop listener
        return False
    try:
        if key.char == 'p':
            sha.print_mouse()

        elif key.char == 'a':
            sha.click(POS_BOSS, 2)
            sha.move_to(POS_TABLE_CENTER)

        elif key.char == 'q':
            EXECUTOR.submit(super_add_dish_sauce_pack)

        elif key.char == 'w':
            # waiting for package fly to table
            # do other stuff
            action_click_coca_machine()
            action_click_potato_pot(2)
            sha.move_to(POS_TABLE_CENTER)

        # elif key.char == 'e':
        #     EXECUTOR.submit(super_fry_potato)

        elif key.char == 'c':
            EXECUTOR.submit(handle_swipte_table)

        elif key.char == 'd':
            enable_super_click()

        elif key.char == 'z':
            sha.move_to(POS_DRINK)
        elif key.char == 'x':
            sha.move_to(POS_DIGUA)
        elif key.char == '1':
            feed_guest(POS_GUEST_1)
        elif key.char == '2':
            feed_guest(POS_GUEST_2)
        elif key.char == '3':
            feed_guest(POS_GUEST_3)
        elif key.char == '4':
            feed_guest(POS_GUEST_4)

    except AttributeError:
        if key == keyboard.Key.tab:
            enable_super_click()


async def handle_key_release(key):
    if key in {keyboard.Key.esc, keyboard.Key.alt, keyboard.Key.cmd}:
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
    return asyncio.run(handle_key_press(key))


def on_release(key):
    return asyncio.run(handle_key_release(key))


def super_click_thread():
    print('鼠标连点线程已启动')
    while True:
        if SUPER_CLICK:
            sha.click_no_pos()
            sleep(0.05)
        else:
            sleep(0.05)


if __name__ == '__main__':
    # Start super click thread
    Thread(target=super_click_thread, daemon=True).start()

    print('按下 ESC 退出')
    print(__doc__)
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
