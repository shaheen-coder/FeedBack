from django.urls import path 
from core import views
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('team/',views.Team.as_view(),name='team'),
    path('error/',views.Error.as_view(),name='error'),
    path('staff/<int:id>/',views.Profile.as_view(),name='prof'),
    path('login/',views.StudentLogin.as_view(),name='login'),
    path('feed/<int:sid>/<int:catid>/',views.FeedBackView.as_view(),name='feed'),
    path('search/',views.Search.as_view(),name='search'),
    #api urls 
    path('api/status/<int:sid>/<str:subject_code>/',views.StaffStatsView.as_view(),name='status'),
]
