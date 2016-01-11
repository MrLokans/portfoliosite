import os
import csv

from django.shortcuts import render

CSV_FILE = os.path.abspath(os.path.join('isp_coverage', "byfly.csv"))


def providers_map(request):
    dots = []
    with open(CSV_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        dots = [row for row in reader if row[0] != "longitude"]
    # coords = [()]
    print(dots)
    return render(request, "isp_map.html", {"coords": dots})
