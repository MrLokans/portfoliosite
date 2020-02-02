from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from apps.spiders import services


class SpiderListView(generics.ListAPIView):

    service = services.SpiderManagementService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(
            data=self.service.list_known_spiders(), status=status.HTTP_200_OK
        )


class SpiderConfigView(generics.RetrieveAPIView):

    service = services.SpiderManagementService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        spider_name = self.kwargs["spider_name"]
        return Response(
            data=self.service.get_config_for_spider(spider_name),
            status=status.HTTP_200_OK,
        )
