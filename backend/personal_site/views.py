from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='MrLokans blog API')


class HealthCheckView(generics.GenericAPIView):

    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        """
        Request site status (whether the django application
        is working)
        """
        return Response({}, status=status.HTTP_200_OK)
