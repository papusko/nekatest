from rest_framework import generics
from .models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .permissions import IsSelf
from core.permissions import IsScrumMaster
from .filters import UserFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
import logging
from sentry_sdk import capture_exception

logger = logging.getLogger('django')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"[REGISTER] Tentative de création: {request.data}")
            response = super().create(request, *args, **kwargs)
            logger.info(f"[REGISTER SUCCESS] Utilisateur créé: {response.data}")
            return response
        except Exception as e:
            logger.error(f"[REGISTER ERROR] Erreur: {str(e)}", exc_info=True)
            capture_exception(e)
            return Response(
                {"detail": "Une erreur est survenue aussi lors de l'inscription."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Empêche de modifier un autre utilisateur
    permission_classes = [IsSelf]


class UsersListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    # Seul le Scrum Master peut voir tous les users
    permission_classes = [IsScrumMaster]  