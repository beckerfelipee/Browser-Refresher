#  You need to install playwright to works fine
#  In your terminal: pip install playwright

from playwright.sync_api import sync_playwright
import threading as th
import os
import time

# defining variables #
url = "www.google.com.br"
press_next = "continue.."  

# defining colors #
color_blue = "\033[34m"
color_yellow = "\033[33m"
color_reset = "\033[0m"


##########################################################
#              defining useful functions                 #
##########################################################

def press_to_next():
    global press_next
    press_next = input(color_blue + "Press [Enter] to continue" + color_reset)


def skip(sec):
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    time.sleep(sec)
    return os.system(command)


def put_https():
    global url
    if "https://" in url:
        pass
    else:
        url = "https://" + url


def url_name():
    global url
    if "www." in url:
        url_start = url.find("www.") + 4
    else:
        if "https://" in url:
            url_start = url.find("https://") + 8
        else:
            url_start = 0
    if ".com" in url:
        url_end = url.find(".com")
    elif ".dev" in url:
        url_end = url.find(".dev")
    elif ".gov" in url:
        url_end = url.find(".gov")
    elif ".org" in url:
        url_end = url.find(".org")
    elif ".net" in url:
        url_end = url.find(".net")
    else:
        return url[url_start:]
    return url[url_start:url_end]


##########################################################
# def scenes (just for aesthetics and info for the user) #
##########################################################

title = ("__________                                           ____"
         "______        _____                      .__                  \n"
         "\______   \_______  ______  _  ________ ___________  \______   \ ___"
         "__/ ____\______   ____   _____|  |__   ___________ \n"
         " |    |  _/\_  __ \/  _ \ \/ \/ /  ___// __ \_  __ \  |       _// __"
         " \   __ \_  __ \_/ __ \ /  ___/  |  \_/ __ \_  __ \ \n"
         " |    |   \ |  | \(  <_> )     /\___  \  ___/|  | \/  |    |   \  ___/"
         "|  |   |  | \/\  ___/ \___ \|   Y  \  ___/|  | \/\n"
         " |______  / |__|   \____/ \/\_//____  >\___  >__|     |____|_  /\___  >"
         "__|   |__|    \___  >____  >___|  /\___  >__|   \n"
         "        \/                          \/     \/                "
         "\/     \/                   \/     \/     \/     \/     \n")

# the title means "Browser Refresher" in ASCII style


loading_bar = ("[      ]", "[⬛     ]", "[⬛⬛    ]",
               "[⬛⬛⬛   ]", "[⬛⬛⬛⬛  ]", "[⬛⬛⬛⬛⬛ ]",
               "[⬛⬛⬛⬛⬛⬛]",
               )


def title_scene(colour):
    if colour:
        print(color_blue + "by Kikope \n\n")
        print(color_yellow + title)
        print(color_reset)
        print()
    else:
        print("by Kikope \n\n")
        print(title)
        print()


def loading_scene():
    time.sleep(0.5)
    bar = loading_bar
    x = 0
    while x != 6:
        skip(0)
        title_scene(colour=True)
        print(color_yellow + "\n\n                        " +
              "Loading '" + url_name() + "' website...  " + bar[x] + color_reset)
        time.sleep(0.5)
        x += 1
    skip(0)
    title_scene(colour=True)
    print(color_yellow + "\n\n                        " +
          "Loading '" + url_name() + "' website...  " + bar[x] + color_reset)
    skip(1)
    title_scene(colour=True)
    print(color_yellow + "\n\n                        " +
          "                  Loaded! " + bar[x] + color_reset)
    skip(2)


def info_scene():
    print(color_blue + "by Kikope \n\n" + color_reset)
    print(color_yellow)
    print("Some information about the program:")
    print("\n\n- When you want to exit, do not close the created browser, " +
          "\n  it will continue to be processed on your computer. " +
          "\n  The correct way is to close this console.")
    print("\n\n- You can search for 'chromium' in the windows task manager" +
          "\n  after closing the program to make sure this didn't happen.")
    print("\n\n- To start or pause the script you need to access this console.")
    print("\n\n- You can manipulate the browser while the script is paused." +
          "\n  (change URL, Login, and other actions...)")
    print(color_blue)
    time.sleep(2)
    print("\n\n")
    press_to_next()
    skip(0)


def launching_script():
    print(color_blue + "by Kikope \n\n")
    print(color_reset)
    print(color_yellow + "Successfully opened!")
    print("\nYou can pause the script when you need,")
    print("just go back to this console and hit [Enter] :)")
    print(color_reset)


##########################################################
#           defining reload script functions             #
##########################################################

between_sec = 3
keep_going = False
pause = "pause"
x = 0


def key_capture_thread():  # capture the key for pause the action
    global pause
    global keep_going
    pause = input()
    print("Paused")
    keep_going = False


def pause_thread():  # run the key_capture_thread in background
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()


def reload_page():
    global between_sec
    global keep_going
    global url
    pause_thread()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        skip(0.5)
        launching_script()

        while True:
            while keep_going:
                time.sleep(between_sec)
                if not keep_going:
                    break
                print("refreshing...")
                page.reload()
                print("done! ")
                pass
            if not keep_going:
                exit_or_cont = input("Write 'return' to continue or 'exit' to close: ")
                if exit_or_cont == "return":
                    keep_going = True
                    pause_thread()
                    pass
                elif exit_or_cont == "exit":
                    browser.close()
                    exit()
                else:
                    pass


def start_loop():
    global between_sec
    global keep_going

    while True:
        between_sec = input(color_yellow +
                            "Enter (in seconds) the time between each update: " +
                            color_reset)
        try:
            between_sec = int(between_sec)
            break
        except ValueError:
            print(color_yellow + "please put only integral numbers!" + color_reset)
            pass
    print(color_yellow + "\nThe page will refresh every " + str(between_sec) +
          " seconds... \n" + color_reset)

    while True:
        start_rl_loop = input(color_yellow + "Press [Enter] to start the script: " + color_reset)
        if start_rl_loop == "":
            keep_going = True
            break
        else:
            pass
    reload_page()


##########################################################
#                   Run the script                       #
##########################################################

def run_script():
    global url

    # Title #
    title_scene(colour=False)  # Only for first screen
    
    # Select Url #
    url = input("\n\n                   Copy and paste a URL to get started: ")
    put_https()

    # scenes (just for aesthetics) #
    loading_scene()
    info_scene()

    # start the script #
    start_loop()


run_script()
