import time
import random
import wikipedia
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput import keyboard

driver = webdriver.Chrome()  # Change this to the appropriate webdriver for your browser

def get_random_page():
    return wikipedia.random(pages=1)

def navigate_to_page(page):
    url = wikipedia.page(page).url
    driver.get(url)
    time.sleep(1)  # Wait for the page to load

def get_related_page(page):
    related_pages = wikipedia.page(page).links
    if len(related_pages) > 0:
        return random.choice(related_pages)
    return page

def search_wikipedia(keyword):
    return wikipedia.search(keyword, results=1)[0]

def on_press(key):
    global current_page, previous_page, last_searched_page
    
    try:
        if key == keyboard.Key.space:
            current_page = get_random_page()
            print(f"Current Page: {current_page}")
            navigate_to_page(current_page)
            
        elif key == keyboard.Key.right:
            if current_page is None:
                current_page = get_random_page()
            elif last_searched_page is not None:
                current_page = get_related_page(last_searched_page)
            else:
                current_page = get_related_page(current_page)
            print(f"Current Page: {current_page}")
            navigate_to_page(current_page)
            
        elif key == keyboard.Key.left and previous_page is not None:
            current_page, previous_page = previous_page, None
            print(f"Current Page: {current_page}")
            navigate_to_page(current_page)
            
        elif key == keyboard.Key.enter:
            print("Enter keyword:")
            keyword = input()
            last_searched_page = search_wikipedia(keyword)
            print(f"Last Searched Page: {last_searched_page}")
            
    except AttributeError:
        pass

def main():
    global current_page, previous_page, last_searched_page
    current_page = None
    previous_page = None
    last_searched_page = None
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
