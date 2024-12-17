import pyautogui
import time
import json
import random

# Open and read the JSON file
with open('test.json', 'r') as file:
    data = json.load(file)
    unfollow_list = [item['string_list_data'][0]['href'] for item in data['relationships_follow_requests_sent']]

# Random time function
def random_sleep(min_time, max_time):
    time.sleep(random.uniform(min_time, max_time))

random_sleep(4, 6)  # Wait for the user to focus on the application

for href in unfollow_list:
    random_sleep(0.5, 1.5)
    pyautogui.hotkey('ctrl', 't')  # Open a new tab
    random_sleep(0.5, 1.5)
    pyautogui.write(href)  # Write the href string (Instagram profile link)
    random_sleep(0.5, 1.5)
    pyautogui.press('enter')  # Press enter
    random_sleep(1.5, 3)  # Give time for the page to load
    
    # Navigate to the unfollow button using tab
    for _ in range(3):  # Press 'tab' 3 times to navigate
        pyautogui.press('tab')
        random_sleep(0.1, 0.3)  # Slight delay to ensure the action is registered
    random_sleep(0.4, 0.6)
    pyautogui.press('enter')  # Press enter to open the user's profile
    random_sleep(1, 2)  # Wait for profile to load
    pyautogui.press('enter')  # Press enter to unfollow
    random_sleep(0.5, 1)
    pyautogui.hotkey('ctrl', 'w')  # Close tab
    random_sleep(0.5, 1)