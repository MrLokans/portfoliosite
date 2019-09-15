import os
import subprocess

from django.conf import settings
from django.core.management import CommandError
from django.db import connection

from apps.apartments_analyzer.management.commands import _base
from apps.apartments_analyzer.models import CityRegion


CITY_REGION_SQL = """
SELECT tags -> 'name:ru' as region_name, ST_AsEWKT(ST_Multi(ST_Transform(way, 4326))) as polygon
FROM planet_osm_polygon
WHERE boundary = 'administrative' AND admin_level = '9'
ORDER BY way_area DESC;
"""


class Command(_base.BaseParserCommand):

    expected_binaries = (
        'wget',
        'osmupdate',
        'osm2pgsql',
    )

    BELARUS_MAP_FILE = f'belarus-latest.osm.pbf'
    MINSK_MAP_FILE = f'minsk.osm.pbf'
    BELARUS_MAP_PATH = f'http://download.geofabrik.de/europe/{BELARUS_MAP_FILE}'
    MINSK_COORDINATES = '27.3552344,53.7841053,28.1260829,53.9745307'

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        self.stdout.write("Checking binary availability.")
        self._check_binaries()
        if not os.path.isfile(self.BELARUS_MAP_FILE):
            self._run_shell_command(f"wget {self.BELARUS_MAP_PATH}")
        self.stdout.write("Updating latest city OSM data.")
        self._run_shell_command(
            f"osmupdate --verbose "
            f"-b={self.MINSK_COORDINATES} "
            f"--drop-version --drop-author "
            f"{self.BELARUS_MAP_FILE} {self.MINSK_MAP_FILE}"
        )
        os.environ.setdefault('PGPASSWORD', db_settings['PASSWORD'])
        self.stdout.write("Exporting data to the database.")
        self._run_shell_command(
            f"osm2pgsql {self.MINSK_MAP_FILE} "
            f"--username {db_settings['USER']} "
            f"--database {db_settings['NAME']} "
            f"--host {db_settings['HOST']} "
            f"--port {db_settings['PORT']} "
            f"--slim --hstore --multi-geometry"
        )
        self._sync_regions()


    def _run_shell_command(self, command):
        return subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL)

    def _check_binaries(self):
        for binary in self.expected_binaries:
            installed = self._make_sure_binary_is_installed(binary)
            if not installed:
                raise CommandError(f"{binary} is not installed, can not proceed.")

    def _make_sure_binary_is_installed(self, binary: str) -> bool:
        try:
            self._run_shell_command(f"which {binary}")
            return True
        except subprocess.CalledProcessError:
            return False

    def _sync_regions(self):
        self.stdout.write("Syncing regions.")
        with connection.cursor() as cursor:
            cursor.execute(CITY_REGION_SQL)
            for row in cursor.fetchall():
                name, polygon = row
                print(f"Update -> '{name}'.")
                CityRegion.objects.get_or_create(region_name=name, defaults={'polygon': polygon})
