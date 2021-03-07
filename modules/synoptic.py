""" A plugin that gets weather info about set city. """
import requests

from sys import exit
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from modules.errors import Warning
from modules.config_reader import ConfigReader
from modules.paths import get_path
from modules.logger import logger


class ScreenWrapper:
    """
        A class of screen wrap to display some information.

        Attributes
        ----------
        weather_info: dict
            A dict of information.

        Methods
        -------
        render(): void
            render wrapped information to a user.
    """

    def __init__(self, weather_info: dict):
        self.weather_info = weather_info

    def _prepare_output(self):
        info = self.weather_info
        output = "" \
                 "|##################################################################################|\n" \
                 "|-------------------------------Doondler synoptic module---------------------------|\n" \
                 "|##################################################################################|\n" \
                 "\n" \
                 f"\t{info['title']}\n" \
                 f"\t{info['subtitle']}\n" \
                 f"\tTemperature: {info['temperature']} deg | Now: {info['weather_type']}\n" \
                 f"\t{info['feels_like']} | Wind speed: {info['wind_speed']}\n" \
                 f"\tHumidity: {info['humidity']} | pressure: {info['pressure']}\n" \
                 "\n" \
                 "|##################################################################################|\n" \
                 "|-------------------------------Wish you a great day!------------------------------|\n" \
                 "|##################################################################################|\n"

        return output

    def render(self):
        print(self._prepare_output())


class Synoptic:
    """
        A class of a synoptic.

        Attributes
        ----------
        city: str
            A city which user has set.
        api_url: str
            A url address of the YandexPogoda service.

        Methods
        -------
        get_weather(): str
            Parse api url and take current weather prognosis.

    """

    def __init__(self):
        self.city = ConfigReader(get_path("config")).read()["city"]
        self.api_url = f"https://yandex.com/pogoda/{self.city}"
        self.headers = {'User-Agent': UserAgent().chrome}

    def _parse_content(self):
        try:
            html = requests.get(self.api_url, headers=self.headers)
            assert html.status_code == 200, f"A city {self.city} does not exists in YandexPogoda service!"

            return html.text

        except AssertionError as error:
            logger.log(error)
            exit()

    def _take_info(self):
        try:
            soup = BeautifulSoup(self._parse_content(), "lxml")
            gotten_message = soup.find("p", class_=["text-wrapper", "text-wrapper_info"]).get_text()
            title = soup.select("div.header-title.header-title_in-fact")[0]
            subtitle = soup.select("div.fact__time-yesterday-wrap")[0]

            main_weather_block = soup.find("div", class_="fact__temp-wrap")
            sub_weather_block = soup.find("div", class_="fact__props")

            return {
                "title": title.find("h1", id="main_title").get_text(),
                "subtitle": subtitle.get_text(),
                "temperature": main_weather_block.find("span", class_="temp__value_with-unit").get_text(),
                "weather_type": main_weather_block.select("div.link__condition.day-anchor.i-bem")[0].get_text(),
                "feels_like": main_weather_block.select("div.term.term_orient_h.fact__feels-like")[0].get_text(),
                "wind_speed": sub_weather_block.find("div", class_="fact__wind-speed").get_text(),
                "humidity": sub_weather_block.find("div", class_="fact__humidity").get_text(),
                "pressure": sub_weather_block.find("div", class_="fact__pressure").get_text(),
            }

        except IndexError as error:
            logger.set_traceback_showing_mode(False)
            logger.log(error)
            logger.log(Warning(
                "It seems to be a problem. I guess there is something wrong with a "
                "server. Please, wait and try again a little bit later.\n"
                "Also, you probably were banned by YandexPogoda service.\n"
                "Server said: %s" % gotten_message))
            exit()

    def get_weather(self):
        """ Get current weather in set in the configuration file city. """
        screen_wrapper = ScreenWrapper(self._take_info())
        screen_wrapper.render()


if __name__ == "__main__":
    print(Synoptic().get_weather())
