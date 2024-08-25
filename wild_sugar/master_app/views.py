from django.shortcuts import render
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.http import HttpRequest
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


import logging

logger = logging.getLogger('debug_file')


class TestApiView(APIView):
    """
    id -- A first parameter
    first_name -- A second parameter
    """
    def post(self, request):
        logger.warning("Platform is running at risk")
        logger.critical("Payment system is not responding")
        logger.debug("Attempting to connect to API")
        logger.info("Attempting to connect to API")
        id = request.data.get('id', None)
        first_name = request.data.get('first_name', None)
        
        return JsonResponse({'message':'Swagger Test', 'status':False, 'status_code':200}, status=400)

