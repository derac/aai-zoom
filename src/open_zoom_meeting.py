import os
from time import sleep
from urllib import parse

import pyautogui


def open_zoom_meeting(meeting_url):
    os.system("pkill zoom")
    os.system("zoom &")

    S_WAIT = 2
    parsed_url = parse.urlsplit(meeting_url)
    params = parse.parse_qs(parsed_url.query)
    meeting_number = parsed_url.path.split("/")[-1]
    password = params["pwd"][0]

    sleep(S_WAIT)
    pyautogui.click(878, 532)
    sleep(S_WAIT)
    pyautogui.click(862, 455)
    pyautogui.write(meeting_number)
    pyautogui.click(939, 675)
    sleep(S_WAIT)
    pyautogui.click(862, 455)
    pyautogui.write(password)
    pyautogui.click(939, 675)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-meeting_url", "-m", type=str, required=True)
    args = parser.parse_args()

    open_zoom_meeting(args.meeting_url)
