from django.db import connection

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class StatisticsRepository(object):
    # FIXME: this can be easily rewritten
    # with django ORM

    @classmethod
    def get_hour_aggregated_stats(self) -> dict:
        SQL_query = """
        SELECT CAST(coalesce(DATE_PART('hour', time_finished), '0') AS integer) AS hour,
               SUM(total_saved)
        FROM apartments_analyzer_apartmentscrapingresults
        WHERE total_saved < 1000
        GROUP BY hour
        ORDER BY hour;
        """
        with connection.cursor() as cursor:
            cursor.execute(SQL_query)
            data = cursor.fetchall()
            return {'hours': data}

    @classmethod
    def get_weekday_aggregated_stats(self) -> dict:
        SQL_query = """
        SELECT CAST(coalesce(DATE_PART('dow', time_finished), '0') AS integer) AS day,
               SUM(total_saved)
        FROM apartments_analyzer_apartmentscrapingresults
        WHERE total_saved < 1000
        GROUP BY day
        ORDER BY day;
        """
        with connection.cursor() as cursor:
            cursor.execute(SQL_query)
            data = cursor.fetchall()
            return {'days': data}


class GetStatsPerHoursView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        repo = StatisticsRepository()
        stats = repo.get_weekday_aggregated_stats()
        return Response({'stats': stats})
