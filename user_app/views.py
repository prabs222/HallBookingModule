from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser ,AllowAny
from .models import LeftPanel
from django.db.models import Q
# Create your views here.
class logout_view(APIView):
    def post(self,request):  
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()
        return Response("Successfully logged out", status=status.HTTP_200_OK)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]    
    def get(self, request):
        if request.user.rolename == "AO":
            res = {
            "routes" : list(LeftPanel.objects.filter(Q(allow = 1) | Q(allow = 0)).values()),
            "data" : { " name": request.user.username , "role": "AO"}
            }
            return Response(res)

        elif request.user.rolename == "HOD":
            res = {
            "routes" : LeftPanel.objects.filter(Q(allow = 2) | Q(allow = 0)).values(),
            "data" : { " name": request.user.username , "role": "Hod"}
            }
            return Response(res)

        elif (request.user.rolename == "Employee"):
            res = {
            "routes" : list(LeftPanel.objects.filter(Q(allow = 3) | Q(allow = 0)).values()),
            "data" : { " name": request.user.username , "role": "Employee"}
            }
            return Response(res)

