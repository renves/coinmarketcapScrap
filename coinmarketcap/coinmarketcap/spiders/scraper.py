import scrapy
from scrapy.http import Request
import datetime
import ipdb
import re


class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    start_urls = ['https://coinmarketcap.com/historical/']
                  # 'https://coinmarketcap.com/historical/'
                

    def parse(self, response):
        links = response.css(
            ".bPfpOJ:nth-child(5) .cmc-link::attr(href)").extract()
        for link in links:
            new_link = response.urljoin(link)
            # ipdb.set_trace()
            yield Request(new_link, callback=self.parse_annual)

    def parse_annual(self, response):

        date = response.url.split('/')[-2]
        date = datetime.datetime.strptime(date, '%Y%m%d').date()

        number_week = date.isocalendar()[1]

        ranks = response.css(
            '.cmc-table__cell--sort-by__rank > div::text').extract()

        names = response.css(
            '.cmc-table__cell--sort-by__name > div > a::text').extract()

        symbols = response.css(
            '.cmc-table__cell--sort-by__symbol > div::text').extract()

        marketcaps = response.css(
            '.cmc-table__cell--sort-by__market-cap > p::text').extract()

        prices = response.css(
            '.cmc-table__cell--sort-by__price > div > a::text').extract()

        circulatingsupplies = response.css(
            '.cmc-table__cell--sort-by__circulating-supply > div::text').extract()
        r = re.compile(r"^(\d+,?)+")
        circulatingsupplies = list(filter(r.match, circulatingsupplies))

        volumes = response.css(
            '.cmc-table__cell--sort-by__volume-24-h > a::text').extract()

        p1hrs = response.css(
            '.cmc-table__cell--sort-by__percent-change-1-h > div::text').extract()
        r = re.compile(r"^(-?\d+\.?)+")
        p1hrs = list(filter(r.match, p1hrs))


        p24hrs = response.css(
            '.cmc-table__cell--sort-by__percent-change-24-h > div::text').extract()
        p24hrs = list(filter(r.match, p24hrs))

        p7days = response.css(
            '.cmc-table__cell--sort-by__percent-change-7-d > div::text').extract()
        p7days = list(filter(r.match, p7days))


        for rank, name, symbol, marketcap, price, circulatingsupply, volume, p1hr, p24hr, p7day in zip(ranks, names, symbols, marketcaps, prices, circulatingsupplies, volumes, p1hrs, p24hrs, p7days):

            yield {'date': date, 'number_week': number_week, 'rank': rank, 'name': name, 'symbol': symbol, 'market_cap': marketcap, 'price': price, 'circulating_supply': circulatingsupply, 'volume': volume, "%_1h": p1hr, '%_24h': p24hr, '%_7d': p7day}
