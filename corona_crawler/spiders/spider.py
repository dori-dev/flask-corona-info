"""Spider for crawl corona information
"""
import pickle
from os import rename
import scrapy
import matplotlib.pyplot as plt
from dictionary import english_to_persian, formated_persian


class MySpider(scrapy.Spider):
    """corona spider to extract information of corona virus
    """
    name = "corona_crawler"

    def start_requests(self):
        page_url = [
            "https://www.worldometers.info/coronavirus/",
        ]
        for url in page_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        table_xpath = "//div[@class='tab-pane active']/div[@class='main_table_countries_div']/table"
        number_of_country = len(response.xpath(
            table_xpath+"/tbody[1]/tr/td[3]/text()").extract())

        cases, deaths, recovered = self.parse_header(response)
        country = self.parse_country(response, number_of_country)
        country = list(map(lambda c: english_to_persian.get(
            c, c) if isinstance(c, str) else "نا مشخص", country))
        new_cases, new_deaths, new_recovered = self.parse_new_columns(
            response, number_of_country)
        total_cases, total_deaths, total_recovered, active_cases, population = self.parse_columns(
            response)

        table_info = {}
        country = country[8:]
        country.insert(0, "جهان")
        population.insert(0, "7,925,351,688")
        table_info["country"] = country
        table_info["total_cases"] = total_cases[7:]
        table_info["new_cases"] = new_cases[7:]
        table_info["total_deaths"] = total_deaths[7:]
        table_info["new_deaths"] = new_deaths[7:]
        table_info["total_recovered"] = total_recovered[7:]
        table_info["new_recovered"] = new_recovered[7:]
        table_info["active_cases"] = active_cases[7]
        table_info["population"] = population

        self.save_info(cases, deaths, recovered, table_info)

    def parse_country(self, response, number_of_country):
        """parse country name(with order) from table
        """
        table_xpath = "//div[@class='tab-pane active']/div[@class='main_table_countries_div']/table"
        country = []
        for i in range(1, number_of_country):
            this_country = response.xpath(
                table_xpath+f"/tbody[1]/tr[{i}]/td[2]/a/text()").extract()
            if self.check_empty(this_country):
                this_country = response.xpath(
                    table_xpath+f"/tbody[1]/tr[{i}]/td[2]/span/text()").extract()

            country.append(this_country[0] if this_country else this_country)
        return country

    @staticmethod
    def parse_new_columns(response, number_of_country):
        """parse new cases, new deaths, new recovered from table
        """
        new_cases = []
        new_deaths = []
        new_recovered = []
        table_xpath = "//div[@class='tab-pane active']/div[@class='main_table_countries_div']/table"

        for i in range(1, number_of_country):
            this_new_cases = response.xpath(
                table_xpath+f"/tbody[1]/tr[{i}]/td[4]/text()").extract()
            if not any(this_new_cases):
                this_new_cases = [""]

            this_new_deaths = response.xpath(
                table_xpath+f"/tbody[1]/tr[{i}]/td[6]/text()").extract()
            if not any(this_new_deaths):
                this_new_deaths = [""]

            this_new_recovered = response.xpath(
                table_xpath+f"/tbody[1]/tr[{i}]/td[8]/text()").extract()
            if not any(this_new_recovered):
                this_new_recovered = [""]

            new_cases.append(this_new_cases[0])
            new_deaths.append(this_new_deaths[0])
            new_recovered.append(this_new_recovered[0])

        return (
            list(map(lambda x: "" if x == "N/A" else x, new_cases)),
            list(map(lambda x: "" if x == "N/A" else x, new_deaths)),
            list(map(lambda x: "" if x == "N/A" else x, new_recovered))
        )

    @staticmethod
    def parse_columns(response):
        """parse columns info from table
        """
        table_xpath = "//div[@class='tab-pane active']/div[@class='main_table_countries_div']/table"
        total_cases = response.xpath(
            table_xpath+"/tbody[1]/tr/td[3]/text()").extract()

        total_deaths = response.xpath(
            table_xpath+"/tbody[1]/tr/td[5]/text()").extract()

        total_recovered = response.xpath(
            table_xpath+"/tbody[1]/tr/td[7]/text()").extract()
        total_recovered = list(
            map(lambda x: "نا مشخص" if x == "N/A" else x, total_recovered))

        active_cases = response.xpath(
            table_xpath+"/tbody[1]/tr/td[9]/text()").extract()

        population = response.xpath(
            table_xpath+"/tbody[1]/tr/td[15]/a/text()").extract()

        return (
            total_cases, total_deaths, total_recovered,
            active_cases, population)

    @staticmethod
    def parse_header(response):
        """parse header information like
        cases
        deaths
        recovered
        """
        data_xpath = "//div[@class='maincounter-number']/span/text()"
        data = response.xpath(data_xpath).extract()
        return data[:3]

    def save_info(self, cases, deaths, recovered, table_info):
        """save information with pickle to info_db binary file
        """
        with open("static/DB/info_db.dat", "rb") as old_info_data:
            with open("static/DB/old_info_db.dat", "wb") as old_info_file:
                old_info_file.write(old_info_data.read())

        with open("static/DB/info_db.dat", "wb") as info:
            pickle.dump(cases, info)
            pickle.dump(deaths, info)
            pickle.dump(recovered, info)
            pickle.dump(table_info, info)

        self.draw_plot(table_info["country"][1:],
                       table_info["total_cases"][1:])

    @ staticmethod
    def check_empty(my_list: list) -> bool:
        """check list for empty or not
        examples:
            [] -> True
            [""] -> True
            [a, b, ""] -> False
            ["", "", "  "] -> True
            [x, y] -> False
        """
        new_list = list(map(str.strip, my_list))
        return not any(new_list)

    @staticmethod
    def draw_plot(country: list, total_cases: list):
        """draw plot and save it

        Args:
            country (list): country names
            total_cases (list): total cases info
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_facecolor('#f5f5f5')
        fig.set_facecolor('#f5f5f5')
        plt.setp(ax.spines.values(), color="#000000")
        number_of_top_country = 12
        total_cases = [int(case.replace(",", ""))/1000000
                       for case in total_cases[:number_of_top_country]]
        country = country[:number_of_top_country]
        country = list(map(lambda c: formated_persian.get(
            c, c) if isinstance(c, str) else "نا مشخص", country))
        reg = range(number_of_top_country)
        colors = [
            "#9E0000",
            "#B60000",
            "#CF0000",
            "#E70000",
            "#EC1400",
            "#F12900",
            "#F53D00",
            "#FA5200",
            "#FF6600",
            "#F98C06",
            "#F79E09",
            "#F4B10C",
        ]
        chart = plt.bar(reg, total_cases, color=colors, width=0.6)
        plt.ticklabel_format(style="plain", useLocale=True, useMathText=True)
        plt.xticks(reg, country, fontsize=12)
        plt.yticks(fontsize=14)
        plt.title('ﺎﻧﻭﺮﮐ ﺎﺑ ﺮﯿﮔﺭﺩ ﯼﺎﻫﺭﻮﺸﮐ ﻥﺎﯾﻼﺘﺒﻣ ﻉﻮﻤﺠﻣ ﺭﺎﻣﺁ\n',
                  fontsize=25)
        plt.ylabel("ﻥﻮﯿﻠﯿﻣ\n", fontsize=18)
        plt.legend(chart, country, fontsize=12)
        plt.savefig("static/DB/saving_plot.png")
        rename("static/DB/saving_plot.png", "static/DB/plot.png")
