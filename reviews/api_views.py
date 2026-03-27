from django.contrib.auth import authenticate
from .models import Book, Review
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from .serializers import BookSerializer, ReviewSerializer

class BookViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Book.objects.all()
     serializer_class = BookSerializer
     authentication_classes = []
     authentication_classes = []
     # permission_classes = [IsAuthenticated]
     # permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
     queryset = Review.objects.order_by('-date_created')
     serializer_class = ReviewSerializer
     pagination_class = LimitOffsetPagination
     authentication_classes = []
