from rest_framework.response import Response
from rest_framework import status

# \\___________________________________________________//


class CustomResponse:
    @staticmethod
    def success(data=None, message="Opération réussie.", 
                status_code=status.HTTP_200_OK):
        return Response({
            "status": "success",
            "data": data,
            "message": message
        }, status=status_code)

    @staticmethod
    def error(errors=None, message="Erreur rencontrée.", 
              status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "status": "error",
            "errors": errors,
            "message": message
        }, status=status_code)

