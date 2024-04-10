# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User
# from apps.auth1.serializer import UserSerializer # type: ignore

# class UserRegistrationAPIView(APIView):
#     """
#     API endpoint for user registration.
#     """
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             # Save the user
#             user = serializer.save()
#             return Response({"message": "User registered successfully", "user_id": user.user_id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#=========================================

from rest_framework import viewsets
from .models import User
from .serializer import UserSerializer  


class SignUpViews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer