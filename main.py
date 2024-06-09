import time
import pyautogui
import random
import keyboard
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog

mouse = Controller()
time.sleep(0.5)


def click(xs, ys):
    mouse.position = (xs, ys + random.randint(1, 2))
    mouse.press(Button.left)
    mouse.release(Button.left)


def choose_window():
    root = tk.Tk()
    root.withdraw()

    windows = gw.getAllTitles()
    if not windows:
        return None

    choice = simpledialog.askstring("Выбор окна Telegram:", "Введите номер окна:\n" + "\n".join(f"{i}: {window}" for i, window in enumerate(windows)))

    if choice is None or not choice.isdigit():
        return None

    choice = int(choice)
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        return None


def find_start_button(screen, window_rect):
    width, height = screen.size # ~(380,690)
    for x in range(0, width, 20):
        y = height - height / 7
        r, g, b = screen.getpixel((x, y))
        if (r, g, b) == (255, 255, 255):
            screen_x = window_rect[0] + x
            screen_y = window_rect[1] + y
            click(screen_x, screen_y)
            print('Запускаю новую игру...')
            time.sleep(0.01)
            return True
    return False

window_name = "TelegramDesktop"
check = gw.getWindowsWithTitle(window_name)

if not check:
    print(f"\nОкно {window_name} не найдено! Попробйте выбрать другое окно.")
    window_name = choose_window()
else:
    print(f"\nОкно {window_name} найдено!\nНажмите 'S' для старта.")

t_window = gw.getWindowsWithTitle(window_name)[0]
paused = True
last_checking = time.time()

while True:
    if keyboard.is_pressed('S'):
        paused = not paused
        if paused:
            print('Пауза')
        else:
            print('Начинаю кликать!')
            print("Чтобы остновить кликер, нажмите 'S'")
        time.sleep(0.3)

    if paused:
        continue

    window = (t_window.left, t_window.top, t_window.width, t_window.height)

    if t_window != []:
        try:
            t_window.activate()
        except:
            t_window.minimize()
            t_window.restore()

    screen = pyautogui.screenshot(region=(window[0], window[1], window[2], window[3]))

    width, height = screen.size
    pixel_found = False

    for x in range(0, width, 20):
        for y in range(130, height, 20):
            r, g, b = screen.getpixel((x, y))
            if (r in range(105, 221)) and (g in range(200, 256)) and (b in range(0, 126)):
                screen_x = window[0] + x
                screen_y = window[1] + y
                click(screen_x, screen_y)
                time.sleep(0.003)
                pixel_found = True
                break

    current_time = time.time()
    if current_time - last_checking >= 33:
        if find_start_button(screen, window):
            last_checking = current_time