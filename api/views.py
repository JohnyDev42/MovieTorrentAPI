import pyodbc
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# server = 'DESKTOP-LACGG2H'
# database = 'Students'
# username = 'sa'
# password = '123456'
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
#                       server+';DATABASE='+database+';UID='+username+';PWD=' + password)
# cursor = cnxn.cursor()
# out = cursor.execute('''SELECT TOP (1000) [id]
#       ,[title]
#       ,[description]
#       ,[no_of_ratings]
#       ,[avg_rating]
#   FROM [Students].[dbo].[Movie]''')

# print(out)
# columns = [column[0] for column in out.description]
# print(columns)
# results = []
# for row in out.fetchall():
#     results.append(dict(zip(columns, row)))
# print(results)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    # print(queryset)
    #queryset = results

    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print('user ', user)
            #user = User.objects.get(id=1)
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'rating updated',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(
                    user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'rating created',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'status': 'provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
