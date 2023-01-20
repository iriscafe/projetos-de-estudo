import scrapy
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "pt_BR")


class CortexSpider(scrapy.Spider):
    name = "cortex_spider"
    page_number = 2

    start_urls = ['https://cortex-intelligence.com/blog/']

    def parse(self, response):
        posts = response.xpath(
            '//div[@class="post-desc"]//h2/a[re:test(@href, "blog/")]/@href'
        ).getall()
        for post in posts:
            yield scrapy.Request(
                post,
                callback=self.parse_post
            )
        next_page = 'https://cortex-intelligence.com/blog/page/' + str(CortexSpider.page_number) + '/'
        if CortexSpider.page_number < 6:
            CortexSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)


    def parse_post(self, response):
        title = response.css('h1::text').get()
        subtitle = response.css('div.resumo p::text').get()
        author = response.css('span.fn a::text').get()
        date = response.css('span.post-date.updated ::text').get()
        try:
            date_object = datetime.strptime(date[:-1], "%d %b, %Y").date()
            date_br = date_object.strftime("%d/%m/%Y")
        except:
            date_object = datetime.strptime(date[:-1], "%d %B, %Y").date()
            date_br = date_object.strftime("%d/%m/%Y")
        images = response.css('img::attr(src)').getall()
        videos = response.css('video source::attr(src)').getall()

        yield {
            'titulo': title,
            'sub-titulo': subtitle,
            'autor': author,
            'data': date_br,
            'links-imagens': images,
            'links-videos': videos
        }
