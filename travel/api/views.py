from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins
from . import serializers


class FlagGameView(APIView):

    def get(self, request):
        return Response(serializers.flag_data())


class UserLogListView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.TravelUserLogSerializer
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
