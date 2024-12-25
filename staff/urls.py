from django.urls import path
from staff import views
urlpatterns = [
    path('dash/',views.StaffDash.as_view(),name='staff-dash'),
    path("search/<str:mode>/<int:ana>/", views.Search.as_view(), name="staff-search"),
    path("class/search/<str:mode>/<int:ana>/", views.ClassSearch.as_view(), name="staff-csearch"),
    path('report/',views.ReportMode.as_view(),name='staff-reportmode'),
    path('analysis/',views.AnalysisMode.as_view(),name='staff-anamode'),
    path("feedscheduler/", views.FeedScheduler.as_view(), name="feed-time"),
    path('studentcheck/',views.StudentCheck.as_view(),name='stu-check'),
    path('staffcheck/',views.StaffCheck.as_view(),name='staff-check'),
]
