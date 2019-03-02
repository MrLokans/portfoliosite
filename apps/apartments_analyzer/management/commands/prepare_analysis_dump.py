import csv
import logging
from typing import List

from django.core.management.base import BaseCommand, CommandError

from apps.apartments_analyzer.models import RentApartment

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    SUPPORTED_FIELDS = {f.name for f in RentApartment._meta.fields}
    EXPORTED_FIELDS = (
        "bullettin_url",
        "address",
        "apartment_type",
        "price_BYN",
        "price_BYN",
        "description",
        "longitude",
        "latitude",
        "author_url",
        "status",
        "user_phones",
        "user_name",
        "last_updated",
        "image_links",
        "has_balcony",
        "has_conditioner",
        "has_balcony",
        "has_conditioner",
        "has_fridge",
        "has_furniture",
        "has_kitchen_furniture",
        "has_oven",
        "has_tv",
        "has_washing_machine",
    )

    help = """Outputs the apartment data in a format suitable for future analysis."""

    def csv_row_from_instance(self, instance) -> List:
        return [getattr(instance, field) for field in self.EXPORTED_FIELDS]

    def add_arguments(self, parser):
        parser.add_argument("-f", "--output-file", required=True, type=str)

    def handle(self, *args, **kwargs):
        output_file = kwargs["output_file"]
        if not output_file.endswith(".csv"):
            raise CommandError("Non CSV output files are not supported.")
        for field in self.EXPORTED_FIELDS:
            if field not in self.SUPPORTED_FIELDS:
                raise CommandError("{} is not declared in your model".format(field))
        with open(output_file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(self.EXPORTED_FIELDS)

            for (
                apartment
            ) in RentApartment.objects.iterator():  # pylint: disable=not-an-iterable
                writer.writerow(self.csv_row_from_instance(apartment))
