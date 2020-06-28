from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_song(song_info, profile, driver):
    search_URL = "https://www.youtube.com/results?search_query="
    song_info = song_info.replace(" ", "+")
    lyrics = "+lyrics"
    search_URL = search_URL + song_info + lyrics

    driver.get(search_URL)

    print("Go to search query")

    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    links = []
    video_title = ""
    for i in user_data:
        if not (str(i.get_attribute('class')).__contains__("playlist")):
            links.append(i)

    video = links[0]
    video_URL = links[0].get_attribute('href')
    video_title = links[0].get_attribute('title')
    link_num = 1
    while video_URL is None:
        video_URL = links[link_num].get_attribute('href')
        video_title = links[link_num].get_attribute('title')
        link_num += 1

    print("Using [" + video_title + "]")
    driver.get("https://ytmp3.cc")
    user_data = driver.find_elements_by_xpath('//*[@id="input"]')

    # Select the video url input box
    id_box = driver.find_element_by_name('video')
    id_box.send_keys(video_URL)

    # click convert button
    convert_button = driver.find_elements_by_id('submit')[0]
    convert_button.click()
    print("Pressed convert video")

    link = ""
    while link == "":
        download_button = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div[1]/div[3]/a[1]')
        link = download_button.get_attribute('href')

    driver.get(link)
    time.sleep(5)


def main():
    songs = list()
    file = open("C:\\Users\\b1n4ry\\Desktop\\songs.txt", "r+")

    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": r"C:\Users\b1n4ry\Desktop\Music",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    profile = ""
    for line in file:
        print("Search: " + line)
        get_song(line, profile, driver)
        print("Downloaded...")


main()
