from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from rest_framework import generics
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

# importação serializers
from core.serializers import (GuardPostSerializer, AccessRegisterSerializer, 
                              VisitorSerializer, EmployeeSerializer)

# importação dos modelos
from core.models import (GuardPost, AccessRegister, 
                         Visitor, Employee, PersonType)

from django.contrib.auth import get_user_model, authenticate
GuardPost = get_user_model()

import logging

logger = logging.getLogger(__name__)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user  
        user_data = {
            'id': user.id,
            'email': user.email,
            'nome': user.username,  
        }
        return Response(user_data)
    
class RegisterView(APIView):
    """
    View para registrar um novo usuário.
    """

    queryset = GuardPost.objects.all()
    serializer_class = GuardPostSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GuardPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuário cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    """
    View para autenticar um usuário.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Email recebido: {email}") #adicionei esta linha
        print(f"Senha recebida: {password}") #adicionei esta linha

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh_token.access_token),
                "refresh": str(refresh_token),
                "usuario": {  
                    "id": user.id
                }
            }, status=200)
        return Response({"error": "Credenciais inválidas."}, status=401)
    

class AccessRegisterViewSet(viewsets.ModelViewSet):

    queryset = AccessRegister.objects.all()
    serializer_class = AccessRegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)  # Permitir acesso apenas para usuários autenticados


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = (permissions.IsAuthenticated,)  


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        logger.info(f"Requisição para EmployeeViewSet.list: {request.headers}")
        return super().list(request, *args, **kwargs)