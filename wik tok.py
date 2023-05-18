import wikipediaapi
import keyboard

def get_random_page():
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_name = wiki_wiki.random(pages=1)
    page = wiki_wiki.page(page_name)
    while not page.exists():
        page_name = wiki_wiki.random(pages=1)
        page = wiki_wiki.page(page_name)
    return page_name

def get_page_in_same_vein(page_name):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(page_name)
    if page.exists():
        for link in page.links:
            return link
    return page_name

def main():
    current_page = get_random_page()
    previous_page = None
    
    print(f"Current Page: {current_page}")
    
    while True:
        if keyboard.is_pressed('space'):
            current_page = get_random_page()
            print(f"Current Page: {current_page}")
            
        elif keyboard.is_pressed('right'):
            previous_page = current_page
            current_page = get_page_in_same_vein(current_page)
            print(f"Current Page: {current_page}")
            
        elif keyboard.is_pressed('left') and previous_page is not None:
            current_page, previous_page = previous_page, None
            print(f"Current Page: {current_page}")
