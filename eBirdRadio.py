import sys 
import time

from selenium import webdriver as wd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import yaml


class EBirdRadio:

    def __init__(self):
        '''Get initialised browser and set default parameters.'''
        self._browser = self._init_browser()
        self._browser.maximize_window()
        self._browser.implicitly_wait(3)
        self.number_of_birds = 5
        self.bird_duration = 10
        self.pre_post_pause = 2

    def _init_browser(self):
        '''Return intialised browser according to eBirdRadio_config.yml.'''
        with open("eBirdRadio_config.yml") as hdl:
            config = yaml.load(hdl, Loader=yaml.Loader)["browser"]
        browser_type = config["type"]
        binary_location = config["binary_location"]
        driver_location = config["driver_location"]

        browser_handler = {
        'Chrome': {'browser': wd.Chrome, 'options': wd.ChromeOptions, 'service': wd.ChromeService},
        'Edge': {'browser': wd.Edge, 'options': wd.EdgeOptions, 'service': wd.EdgeService},
        'Firefox': {'browser': wd.Firefox, 'options': wd.FirefoxOptions, 'service': wd.FirefoxService},
        'Ie': {'browser': wd.Ie, 'options': wd.IeOptions, 'service': wd.IeService},
        'Safari': {'browser': wd.Safari, 'options': wd.SafariOptions, 'service': wd.SafariService}
        }

        option = browser_handler[browser_type]['options']()
        if binary_location is not None:
            option.binary_location = binary_location
        if driver_location is not None:
            service = browser_handler[browser_type]['service'](executable_path=driver_location)
        else:
            service = browser_handler[browser_type]['service']()

        return browser_handler[browser_type]['browser'](options=option, service=service)

    def run_session(self):
        '''Run listening session while browser is already open.'''
        self._browser.get("https://ebird.org/home")
        self._open_explore_page()
        self._select_initial_bird()
        i = 1
        while i <= self.number_of_birds:
            if i != 1: self._change_species()
            self._print_species_info()
            time.sleep(self.pre_post_pause)
            try:
                self._open_audio_player()
            except NoSuchElementException:
                print("No audio available, selecting different bird!")
                continue
            self._print_recording_info()
            time.sleep(self.bird_duration)
            self._close_audio_player()
            time.sleep(self.pre_post_pause)
            i += 1

    def close_radio(self):
        self._browser.quit()

    def _print_species_info(self):
        eng, lat = self._get_species_names()
        print("*** Listening to: {} ({})...".format(eng, lat))

    def _print_recording_info(self):
        info = self._get_recording_info()
        print(info)

    #---------------web page interaction--------------------------------

    def _open_explore_page(self):
        self._set_language_to_english()
        self._click_explore_button()

    def _set_language_to_english(self):
        language_menu = self._browser.find_element(By.ID, "language-menu-heading")
        language_menu.click()
        language_list = self._browser.find_element(By.CLASS_NAME, "u-textLanguageList")
        languages = language_list.find_elements(By.CLASS_NAME, "Header-link")
        for language in languages:
            if language.text == "English":
                language.click()
                break

    def _click_explore_button(self):
        header_menu = self._browser.find_element(By.CLASS_NAME, "Header-group")
        for item in header_menu.find_elements(By.TAG_NAME, "a"):
            if item.text == "Explore":
                item.click()
                break

    def _select_initial_bird(self):
        surprise_button = self._browser.find_element(By.ID, "random-species-btn")
        surprise_button.click()

    def _change_species(self):
        toolbar = self._browser.find_element(By.CLASS_NAME, "Toolbar")
        for item in toolbar.find_elements(By.TAG_NAME, "a"):
            if "Change Species" in item.text:
                item.click()
                break
        change_dialogue = self._browser.find_element(By.ID, "changeSpecies")
        for item in change_dialogue.find_elements(By.TAG_NAME, "a"):
            if "Surprise me!" in item.text:
                item.click()
                break

    def _get_species_names(self):
        eng_spec = self._browser.find_element(By.CLASS_NAME, "Heading-main").text
        lat_spec = self._browser.find_element(By.CLASS_NAME, "Heading-sub").text
        return eng_spec, lat_spec

    def _get_recording_info(self):
        info = self._browser.find_element(By.CLASS_NAME, "MediaControls-meta").text
        return info

    def _open_audio_player(self):
        playlist_area = self._browser.find_element(By.CLASS_NAME, "Species-identification-audio")
        listen_button = playlist_area.find_element(By.CLASS_NAME, "Button--huge")
        listen_button.click()

    def _close_audio_player(self):
        playlist_footer = self._browser.find_element(By.CLASS_NAME, "Playlist-footer")
        playlist_close = playlist_footer.find_element(By.CLASS_NAME, "Button")
        playlist_close.click()


if __name__ == "__main__":

    radio = EBirdRadio()

    args = sys.argv
    l = len(args)
    try:
        if l >= 2: radio.number_of_birds = int(args[1])
        if l >= 3: radio.bird_duration = int(args[2])
        if l >= 4: radio.pre_post_pause = int(args[3])
    except ValueError:
        print("Wrong parameters!")
        print("Usage: Pass integers positionally and non-mandatory for number of birds, song duration, and pause before/after song in seconds.")
        print("e.g. (with defaults): python eBirdRadio.py 5 10 2")

    radio.run_session()
    radio.close_radio()
