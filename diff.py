import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import json
import os
import tempfile
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep

def extract_zip(zip_path):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    followers_path = os.path.join(temp_dir, 'connections', 'followers_and_following', 'followers_1.json')
    following_path = os.path.join(temp_dir, 'connections', 'followers_and_following', 'following.json')
    return followers_path, following_path

def load_follow_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    usernames = set()
    if isinstance(data, dict) and 'relationships_following' in data:
        data = data['relationships_following']
    for item in data:
        if 'string_list_data' in item and item['string_list_data']:
            usernames.add(item['string_list_data'][0]['value'])
    return usernames

def process_zip(zip_path):
    try:
        followers_path, following_path = extract_zip(zip_path)
        followers = load_follow_data(followers_path)
        following = load_follow_data(following_path)
        mutual_followers = followers.intersection(following)
        followers_not_following_back = followers - following
        following_not_followed_back = following - followers
        return mutual_followers, followers_not_following_back, following_not_followed_back
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return set(), set(), set()

def display_results(tree, data, sort_by='alphabetical', is_unfollow_tab=False):
    for widget in tree.winfo_children():
        widget.destroy()
    
    sorted_data = sorted(data) if sort_by == 'alphabetical' else list(data)
    
    if is_unfollow_tab:
        global unfollow_vars
        unfollow_vars = {user: tk.BooleanVar() for user in sorted_data}
        
        for user, var in unfollow_vars.items():
            check = ttk.Checkbutton(tree, text=user, variable=var)
            check.pack(anchor='w')
    else:
        for item in sorted_data:
            tree.insert("", tk.END, values=(item,))

def toggle_sort(tree, data, current_sort, is_unfollow_tab=False):
    new_sort = 'date' if current_sort == 'alphabetical' else 'alphabetical'
    display_results(tree, data, new_sort, is_unfollow_tab=is_unfollow_tab)
    return new_sort

def random_delay(min_seconds, max_seconds):
    sleep(random.uniform(min_seconds, max_seconds))

def verify_instagram_structure(driver):
    """Verify Instagram page structure to confirm the 'Following' button is in the expected location."""
    retries = 3
    for attempt in range(retries):
        try:
            # Wait a bit to allow the page to load completely
            random_delay(2, 4)
            if attempt == 0:
                driver.get("https://www.instagram.com/instagram/")
            
            try:
                # Attempt to find the "Following" button using the provided XPath
                following_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[2]/div/div[1]/button/div/div")
                if following_button:
                    print("Page structure verified: 'Following' button is in the expected location.")
                    return True
            except NoSuchElementException:
                pass

            print(f"Attempt {attempt + 1}/{retries}: Profile structure not verified, retrying...")

        except Exception as e:
            print(f"Error during structure verification: {e}")
        
    print("Page structure verification failed after multiple attempts.")
    return False

def login_if_needed(driver, username, password):
    try:
        login_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_field.send_keys(username)
        password_field.send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Logged in successfully.")
        random_delay(4, 7)
    except NoSuchElementException:
        print("Already logged in, skipping login step.")

def unfollow_selected():
    selected_users = [user for user, var in unfollow_vars.items() if var.get()]
    if not selected_users:
        messagebox.showwarning("No Selection", "Please select users to unfollow.")
        return
    run_selenium_unfollow(selected_users)

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def run_selenium_unfollow(usernames):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("user-data-dir=C:\\SeleniumProfile")  # Reuse session

    service = webdriver.chrome.service.Service('C:\\SeleniumDrivers\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.instagram.com/accounts/login/")
    random_delay(3, 5)

    username = "ENTER_USERNAME_HERE"
    password = "ENTER_PASSWORD_HERE"

    try:
        login_if_needed(driver, username, password)
        if not verify_instagram_structure(driver):
            print("Instagram structure verification failed. Aborting unfollow process.")
            return

        for user in usernames:
            driver.get(f"https://www.instagram.com/{user}/")
            random_delay(2, 4)

            try:
                # Locate and click the "Following" button
                following_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[2]/div/div[1]/button")
                following_button.click()
                random_delay(1, 2)

                # Wait for and click the "Unfollow" button in the confirmation popup
                unfollow_confirm_button = driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[8]/div[1]")
                unfollow_confirm_button.click()
                print(f"Unfollowed {user}")
                random_delay(5, 10)
            except NoSuchElementException:
                print(f"Failed to unfollow {user}: Button not found.")
                continue

    except Exception as e:
        print("Error occurred during unfollowing:", e)
    finally:
        driver.quit()

    print("Unfollowing process completed.")
    messagebox.showinfo("Unfollow Complete", "Selected users have been unfollowed.")

def upload_and_process():
    zip_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    if zip_path:
        global mutual, not_following_back, not_followed_back
        mutual, not_following_back, not_followed_back = process_zip(zip_path)
        
        global mutual_sort, not_following_back_sort, not_followed_back_sort
        mutual_sort = 'alphabetical'
        not_following_back_sort = 'alphabetical'
        not_followed_back_sort = 'alphabetical'

        display_results(tree_mutual, mutual, mutual_sort)
        display_results(tree_not_following_back, not_following_back, not_following_back_sort)
        display_results(frame_not_followed_back, not_followed_back, not_followed_back_sort, is_unfollow_tab=True)
        
        unfollow_button = ttk.Button(frame_not_followed_back, text="Unfollow Selected", command=unfollow_selected)
        unfollow_button.pack(pady=10)

# GUI Setupf
root = tk.Tk()
root.title("Instagram Follower Analyzer")

btn_upload = tk.Button(root, text="Upload ZIP File", command=upload_and_process)
btn_upload.pack(pady=10)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

frame_mutual = ttk.Frame(notebook)
frame_not_following_back = ttk.Frame(notebook)
frame_not_followed_back = ttk.Frame(notebook)
notebook.add(frame_mutual, text="Mutual Followers")
notebook.add(frame_not_following_back, text="Followers Not Following Back")
notebook.add(frame_not_followed_back, text="Following Not Followed Back")

tree_mutual = ttk.Treeview(frame_mutual, columns=("Mutual Followers",), show="headings")
tree_not_following_back = ttk.Treeview(frame_not_following_back, columns=("Not Following Back",), show="headings")

for tree, column_name in [(tree_mutual, "Mutual Followers"), 
                          (tree_not_following_back, "Not Following Back")]:
    tree.heading(column_name, text=column_name)
    tree.pack(expand=True, fill="both")

mutual_sort_btn = ttk.Button(frame_mutual, text="Toggle Sort", command=lambda: toggle_sort(tree_mutual, mutual, mutual_sort))
mutual_sort_btn.pack(pady=5)
not_following_back_sort_btn = ttk.Button(frame_not_following_back, text="Toggle Sort", command=lambda: toggle_sort(tree_not_following_back, not_following_back, not_following_back_sort))
not_following_back_sort_btn.pack(pady=5)
not_followed_back_sort_btn = ttk.Button(frame_not_followed_back, text="Toggle Sort", command=lambda: toggle_sort(frame_not_followed_back, not_followed_back, not_followed_back_sort, is_unfollow_tab=True))
not_followed_back_sort_btn.pack(pady=5)

root.geometry("600x600")
root.mainloop()