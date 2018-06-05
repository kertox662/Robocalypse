from pynput import keyboard
from threading import Thread

x = {1:2, 3:4, 5:6}
print(len(x))
print(x.index(3))

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        print(type(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        print(type(key))
    
def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
