from django.urls import path 
from core import views
urlpatterns = [
    path('staff/<int:id>/',views.Profile.as_view(),name='prof'),
    path('',views.StudentLogin.as_view(),name='login'),
    path('feed/<int:sid>/<int:catid>/',views.FeedBackView.as_view(),name='feed'),
    path('search/',views.Search.as_view(),name='search'),
]
