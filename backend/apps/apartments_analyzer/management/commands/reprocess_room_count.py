import json
from collections import defaultdict

from agent_spider import settings
from agent_spider.apartment_spider import OnlinerApartmentSpider
from scrapy.crawler import CrawlerProcess

from apps.apartments_analyzer.enums import BulletinStatusEnum
from apps.apartments_analyzer.management.commands import _base
from apps.apartments_analyzer.models import SoldApartments


class InterruptedSpider(OnlinerApartmentSpider):

    def __init__(self, start_urls, *args, **kwargs):
        self.start_urls = start_urls
        super().__init__(*args, **kwargs)

    def _get_start_urls(self, *args, **kwargs):
        return self.start_urls


class Command(_base.BaseParserCommand):

    OUTPUT_FILE = "to_update_room_count.json"

    def handle(self, *args, **kwargs):
        urls = (
            SoldApartments
                .objects
                .filter(total_rooms=None)
                .filter(status=BulletinStatusEnum.ACTIVE.value)
                .values('id', 'bullettin_url')
        )
        url_to_id_map = {
            item["bullettin_url"]: item["id"] for item in urls
        }
        if not url_to_id_map:
            self.stdout.write("No apartment to sync, quitting.")
            return
        self.stdout.write(f"There are {urls.count()} items to fetch data about.")
        overridden_settings = {
            'FEED_FORMAT': "json",
            'FEED_URI': self.OUTPUT_FILE,
            'SPIDER_LOADER_WARN_ONLY': True,
            'LOG_LEVEL': 'INFO',
        }
        global_settings = {s: getattr(settings, s)
            for s in dir(settings)
            if s.isupper()
        }
        process = CrawlerProcess({**global_settings, **overridden_settings})
        process.crawl(InterruptedSpider, start_urls=list(url_to_id_map.keys()))
        process.start()
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        room_data = defaultdict(list)
        for apartment in data:
            url, rooms = apartment["origin_url"], apartment["room_count"]
            if rooms is not None:
                pk_to_update = url_to_id_map[url]
                room_data[rooms].append(pk_to_update)
        for room_count, ids_to_update in room_data.items():
            SoldApartments.objects.filter(id__in=ids_to_update).update(total_rooms=room_count)
