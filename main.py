import pyautogui
from pynput.keyboard import Controller, Key, Listener
import time
import logging
import threading
import configparser
import os
from ui import create_ui

# Configure logging to output to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

keyboard = Controller()

# Flags to control the script's running state
running = False
stop_script = False

# Default settings
config_file = 'settings.ini'
config = configparser.ConfigParser()

def load_settings():
    global middle_range, sensitivity, sensitivity_multiplier, full_press_sensitivity, hold_down_range, start_key, stop_key
    if os.path.exists(config_file):
        config.read(config_file)
        middle_range = config.getfloat('Settings', 'middle_range', fallback=pyautogui.size()[0] / 5)
        sensitivity = config.getfloat('Settings', 'sensitivity', fallback=0.05)
        sensitivity_multiplier = config.getfloat('Settings', 'sensitivity_multiplier', fallback=1.0)
        full_press_sensitivity = config.getfloat('Settings', 'full_press_sensitivity', fallback=0.01)
        hold_down_range = config.getfloat('Settings', 'hold_down_range', fallback=pyautogui.size()[0] / 10)
        start_key = config.get('Keybinds', 'start_key', fallback='t')
        stop_key = config.get('Keybinds', 'stop_key', fallback='q')
    else:
        middle_range = pyautogui.size()[0] / 5  # Default value
        sensitivity = 0.05  # Default value
        sensitivity_multiplier = 1.0  # Default value
        full_press_sensitivity = 0.01  # Default value
        hold_down_range = pyautogui.size()[0] / 10  # Default value
        start_key = 't'
        stop_key = 'q'

def save_settings():
    config['Settings'] = {
        'middle_range': str(middle_range),
        'sensitivity': str(sensitivity),
        'sensitivity_multiplier': str(sensitivity_multiplier),
        'full_press_sensitivity': str(full_press_sensitivity),
        'hold_down_range': str(hold_down_range)
    }
    config['Keybinds'] = {
        'start_key': start_key,
        'stop_key': stop_key
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    logging.info('Settings saved.')

def update_settings(entry_middle_range, entry_sensitivity, entry_sensitivity_multiplier, entry_full_press_sensitivity, entry_hold_down_range, entry_start_key, entry_stop_key):
    global middle_range, sensitivity, sensitivity_multiplier, full_press_sensitivity, hold_down_range, start_key, stop_key
    try:
        middle_range = float(entry_middle_range.get())
        logging.info('Middle range updated to: %.2f', middle_range)
    except ValueError:
        logging.error('Invalid input for middle range.')

    try:
        sensitivity = float(entry_sensitivity.get())
        logging.info('Sensitivity updated to: %.2f', sensitivity)
    except ValueError:
        logging.error('Invalid input for sensitivity.')

    try:
        sensitivity_multiplier = float(entry_sensitivity_multiplier.get())
        logging.info('Sensitivity multiplier updated to: %.2f', sensitivity_multiplier)
    except ValueError:
        logging.error('Invalid input for sensitivity multiplier.')

    try:
        full_press_sensitivity = float(entry_full_press_sensitivity.get())
        logging.info('Full press sensitivity updated to: %.2f', full_press_sensitivity)
    except ValueError:
        logging.error('Invalid input for full press sensitivity.')

    try:
        hold_down_range = float(entry_hold_down_range.get())
        logging.info('Hold down range updated to: %.2f', hold_down_range)
    except ValueError:
        logging.error('Invalid input for hold down range.')

    start_key = entry_start_key.get()
    stop_key = entry_stop_key.get()
    logging.info('Start keybind updated to: %s', start_key)
    logging.info('Stop keybind updated to: %s', stop_key)

    save_settings()

def toggle_script():
    global running, stop_script
    if not running:
        running = True
        stop_script = False
        logging.info('Script started.')
        start_button.config(text="Pause Script")
        # Start the script in a separate thread
        threading.Thread(target=run_script, daemon=True).start()
    elif running:
        running = False
        logging.info('Script paused.')
        start_button.config(text="Resume Script")

def stop_script_function():
    global running, stop_script
    running = False
    stop_script = True
    start_button.config(text="Start Script")
    logging.info('Script stopped.')

def on_press(key):
    global running, stop_script
    if key == Key.esc:
        logging.info('Esc key pressed. Exiting.')
        stop_script = True
        return False  # Stop listener

    try:
        if key.char == start_key:
            toggle_script()
        elif key.char == stop_key:
            stop_script_function()
    except AttributeError:
        pass

# Get the screen dimensions and center
screen_width, screen_height = pyautogui.size()
center_x = screen_width / 2

def run_script():
    global running, stop_script, middle_range, center_x, sensitivity, sensitivity_multiplier, full_press_sensitivity, hold_down_range
    try:
        while not stop_script:
            if running:
                mouse_x, _ = pyautogui.position()

                # Calculate distance from center and adjust sensitivity
                distance_from_center = abs(mouse_x - center_x)
                if distance_from_center <= middle_range:
                    logging.info('Mouse in middle range, no key pressed.')
                else:
                    # Normalize the distance within the screen width and apply sensitivity scaling
                    normalized_distance = (distance_from_center - middle_range) / (screen_width / 2 - middle_range)
                    adjusted_sensitivity = sensitivity + (normalized_distance * sensitivity * sensitivity_multiplier)
                    
                    if mouse_x < center_x:
                        keyboard.press('a')
                        time.sleep(adjusted_sensitivity)
                        keyboard.release('a')
                        logging.info(f'Key "a" pressed with adjusted sensitivity: {adjusted_sensitivity:.3f}')
                    elif mouse_x > center_x:
                        keyboard.press('d')
                        time.sleep(adjusted_sensitivity)
                        keyboard.release('d')
                        logging.info(f'Key "d" pressed with adjusted sensitivity: {adjusted_sensitivity:.3f}')
                    
                    # Full press sensitivity
                    if normalized_distance > 0.75:
                        if mouse_x < center_x:
                            keyboard.press('a')
                            time.sleep(full_press_sensitivity)
                            keyboard.release('a')
                            logging.info('Holding key: a')
                        else:
                            keyboard.press('d')
                            time.sleep(full_press_sensitivity)
                            keyboard.release('d')
                            logging.info('Holding key: d')

                time.sleep(0.01)  # Constant small delay for processing
    finally:
        # Release keys and stop listener on exit
        keyboard.release('a')
        keyboard.release('d')
        logging.info('Script exited cleanly.')

# Initialize settings and UI
load_settings()
root, start_button = create_ui(
    update_settings,
    toggle_script,
    stop_script_function,
    middle_range,
    sensitivity,
    sensitivity_multiplier,
    full_press_sensitivity,
    hold_down_range,
    start_key,
    stop_key
)

# Start the keyboard listener in a separate thread
listener = Listener(on_press=on_press)
listener_thread = threading.Thread(target=listener.start, daemon=True)
listener_thread.start()

# Start the GUI event loop
root.mainloop()
