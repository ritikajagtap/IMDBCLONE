from django.urls import path, include
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformAV, StreamDetailAV, ReviewList, ReviewDetail, ReviewCreate, StreamPlatformVS
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='watch-detail'),
    path('', include(router.urls)),
#     path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
#     path('stream/<int:pk>/', StreamDetailAV.as_view(), name='stream-detail'),
    path('<int:pk>/review', ReviewList.as_view(), name='review-detail'),
    path('<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),

    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),


]
