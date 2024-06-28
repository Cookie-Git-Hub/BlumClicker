import time
import pyautogui
import random
import keyboard
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog

# Constants:
WINDOW_NAME = "TelegramDesktop"
CLICK_DELAY = 0.003
CHECK_INTERVAL = 33
START_BUTTON_COLOR = (255, 255, 255)
CLICKABLE_COLOR_RANGE = {
    'r': (105, 221),
    'g': (200, 256),
    'b': (0, 126)
}

mouse = Controller()


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
    return windows[choice] if 0 <= choice < len(windows) else None


def is_clickable_color(color):
    r, g, b = color
    return (CLICKABLE_COLOR_RANGE['r'][0] <= r <= CLICKABLE_COLOR_RANGE['r'][1] and
            CLICKABLE_COLOR_RANGE['g'][0] <= g <= CLICKABLE_COLOR_RANGE['g'][1] and
            CLICKABLE_COLOR_RANGE['b'][0] <= b <= CLICKABLE_COLOR_RANGE['b'][1])


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
            time.sleep(0.02)
            return True
    return False


def game_loop(t_window):
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

        try:
            t_window.activate()
        except:
            t_window.minimize()
            t_window.restore()

        screen = pyautogui.screenshot(region=window)

        width, height = screen.size

        for x in range(0, width, 20):
            for y in range(130, height, 20):
                color = screen.getpixel((x, y))
                if is_clickable_color(color):
                    screen_x = window[0] + x
                    screen_y = window[1] + y
                    click(screen_x, screen_y)
                    time.sleep(0.04)
                    break

        current_time = time.time()
        if current_time - last_checking >= CHECK_INTERVAL:
            if find_start_button(screen, window):
                last_checking = current_time

def main():            
    check = gw.getWindowsWithTitle(WINDOW_NAME)

    if not check:
        print(f"\nОкно {WINDOW_NAME} не найдено! Попробуйте выбрать другое окно.")
        window_name = choose_window()
    else:
        print(f"\nОкно {WINDOW_NAME} найдено!\nНажмите 'S' для старта.")
        window_name = WINDOW_NAME
        
    if window_name:
        t_window = gw.getWindowsWithTitle(window_name)[0]
        game_loop(t_window)
    else:
        print("Нужное окно не найдено. Выход.")


if __name__ == "__main__":
    main()