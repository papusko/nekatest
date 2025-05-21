import logging
from sentry_sdk import capture_exception
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def handle_create_view(view_instance, request, *args, **kwargs):
    try:
        logger.info(f"[REGISTER] Tentative de création: {request.data}")
        response = view_instance.create(request, *args, **kwargs)
        logger.info(f"[REGISTER SUCCESS] Utilisateur créé: {response.data}")
        return response
    except Exception as e:
        logger.error(f"[REGISTER ERROR] Erreur: {str(e)}", exc_info=True)
        capture_exception(e)
        return Response(
            {"detail": "Une erreur est survenue lors de l'inscription."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
