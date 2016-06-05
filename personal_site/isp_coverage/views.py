import os
import csv

from django.shortcuts import render
from django.views.generic import TemplateView


BYFLY_CSV_FILE = os.path.abspath(os.path.join('isp_coverage', "byfly.csv"))
MTS_CSV_FILE = os.path.abspath(os.path.join('isp_coverage', "mts.csv"))
UNET_CSV_FILE = os.path.abspath(os.path.join('isp_coverage', "unet.csv"))


class MapView(TemplateView):

    def get(self, request):
        byfly_dots = []
        mts_dots = []
        with open(BYFLY_CSV_FILE, 'r') as csv_file:
            reader = csv.reader(csv_file)
            byfly_dots = [row for row in reader if row[0] != "longitude"]
        with open(MTS_CSV_FILE, 'r') as csv_file:
            reader = csv.reader(csv_file)
            mts_dots = [row for row in reader if row[0] != "longitude"]
        with open(UNET_CSV_FILE, 'r') as csv_file:
            reader = csv.reader(csv_file)
            unet_dots = [row for row in reader if row[0] != "longitude"]
        # coords = [()]
        return render(request, "isp_map.html", {"byfly_coords": byfly_dots,
                                                "mts_coords": mts_dots,
                                                "unet_coords": unet_dots})
