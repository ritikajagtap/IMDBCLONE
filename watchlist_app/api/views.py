from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer,
                                            StreamPlatformSerializer,
                                            ReviewSerializer)
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if(review_queryset.exists()):
            raise ValidationError("you have reviwed this content!")

        if watchlist.number_rating==0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating+serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating+1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)
class ReviewList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [ReviewUserOrReadOnly]
    serializer_class = ReviewSerializer

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class ReviewDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         streamplatform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(streamplatform)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     def update(self, request, pk=None):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     def destroy(self, request, pk=None):
#         stream = StreamPlatform.objects.get(pk=pk)
#         stream.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#streamplatform api views
class StreamPlatformAV(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        streamPlatform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamPlatform, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamDetailAV(APIView):
    def get(self, request, pk):
        try:
            stream =  StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(stream)
        return Response(serializer.data)


    def put(self, request, pk):
        stream = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stream = StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class WatchListAV(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie =  WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)


    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# function based view
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#          serializer = WatchListSerializer(data=request.data)
#          if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#          else:
#             return Response(serializer.errors)
#
# # difference between PUT and PATCH
# # PUT :-> changing or rewriting all the fields
# # PATCH :-> updating only one field which is required
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({'Error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method=='GET':
#         movie = Movie.objects.get(pk=pk)
#         serializer  = WatchListSerializer(movie)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
