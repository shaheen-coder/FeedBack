from django.urls import path 
from core import views
urlpatterns = [
    path('staff/<int:id>/',views.Profile.as_view(),name='prof'),
    path('',views.StudentLogin.as_view(),name='login'),
    path('feed/',views.FeedBackView.as_view(),name='feed'),
]
