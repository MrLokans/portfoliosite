from typing import List

from apps.spiders import models


class SpiderManagementService:
    def list_known_spiders(self) -> List[str]:
        return models.Spider.objects.values_list("name", flat=True)

    def get_config_for_spider(self, spider_name: str) -> dict:
        bot = models.Spider.objects.get(name=spider_name)
        return {
            "name": bot.name,
            "search_criteria": [
                {config.website_part: config.search_words}
                for config in bot.spiderconfiguration_set.all()
            ],
        }

    def register_event(self, spider_name: str, event_data: dict):
        bot = models.Spider.objects.get(name=spider_name)
        event_kind = event_data.pop("kind")
        models.SpiderEvent.objects.create(
            associated_spider=bot, event_data=event_data, event_kind=event_kind
        )
