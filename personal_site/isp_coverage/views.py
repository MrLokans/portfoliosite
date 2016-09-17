import os
import csv
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from isp_coverage.models import ProviderCoordinate


BYFLY_CSV_FILE = os.path.abspath(os.path.join('isp_coverage', "byfly.csv"))
MTS_CSV_FILE = os.path.abspath(os.path.join('isp_coverage', "mts.csv"))
UNET_CSV_FILE = os.path.abspath(os.path.join('isp_coverage', "unet.csv"))


class MapView(TemplateView):

    def get(self, request):
        # with open(UNET_CSV_FILE, 'r') as csv_file:
        #     reader = csv.reader(csv_file)
        #     unet_dots = [row for row in reader if row[0] != "longitude"]
        return render(request, "isp_map.html", {"unet_coords": []})


def get_provider_dots(request):
    provider_name = request.GET.get("provider", "byfly")
    provider_name = provider_name.lower()
    provider_dots = ProviderCoordinate.objects.filter(provider__name__icontains=provider_name)

    dots = {"dots": []}

    for dot in provider_dots:
        dots["dots"].append({"longitude": dot.longitude,
                             "latitude": dot.latitude})
    return HttpResponse(json.dumps(dots), content_type="application/json")
