from time import sleep
from pyperclip import copy

import win32con
import win32api
from pynput.mouse import Controller

import asyncio


mouse = Controller()
FAILSAFE = False


def mouse_up():
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def move_to(pos: tuple):
    win32api.SetCursorPos(pos)


def click_no_pos():
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.03)
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


async def click(pos: tuple, cnt=1, sleep_time=0.04):
    for _ in range(cnt):
        move_to(pos)
        win32api.mouse_event(
            win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # sleep(0.03)
        await asyncio.sleep(0.03)
        win32api.mouse_event(
            win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        if FAILSAFE:
            break
        if cnt > 1:
            await asyncio.sleep(sleep_time)


async def swipe(pos1: tuple, pos2: tuple, duration=0.2):
    move_to(pos1)
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    steps = 20
    x1 = pos1[0]
    x2 = pos2[0]
    y1 = pos1[1]
    y2 = pos2[1]
    for i in range(steps):
        if FAILSAFE:
            break
        p = (int(x1 + (x2 - x1) * i / steps),
             int(y1 + (y2 - y1) * i / steps))
        move_to(p)
        await asyncio.sleep(duration / steps)
        if FAILSAFE:
            break
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


async def click_hold(pos, seconds):
    move_to(pos)
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    for i in range(seconds * 10):
        await asyncio.sleep(0.1)
        if FAILSAFE:
            break

    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def print_mouse():
    print('Mouse position: {0}'.format(
        mouse.position))
    copy(str(mouse.position))
