from django.urls import path 
from api import views
urlpatterns = [
    path('report/',views.Report.as_view(),name='api-report'),
    path('analysis/',views.Analysis.as_view(),name='an'),
    path('analysis/dept/',views.DepartmentAnalysis.as_view(),name='ana-dept'),
    path('student/',views.StudentReport.as_view(),name='s'),
    path("search/student/", views.StudentSearch.as_view(), name="student-search"),
    path('dept/',views.Department.as_view(),name='dept-report'),
    path('instru/',views.Instruction.as_view(),name='ins'),
    path('search/',views.UniversalSearchAPIView.as_view(),name='sss'),
    path('class/search/',views.ClassSerchApi.as_view(),name='class-search'),
    path('feed/search/<int:id>/<int:cid>/<str:subid>/',views.FeedSearch.as_view(),name='feed-search'),
    path("feed/", views.FeedBackApi.as_view(), name="feed-api"),
    path("comment/<int:sid>/", views.CommentApi.as_view(), name="comt-api"),

]