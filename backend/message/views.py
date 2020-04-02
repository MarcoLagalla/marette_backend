from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from .models import Message
from .serializers import MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageAPIView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.all()
        print(messages)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


