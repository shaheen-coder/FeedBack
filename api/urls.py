from django.urls import path 
from api import views
urlpatterns = [
    path('report/',views.Report.as_view(),name='api-report'),
    path('analysis/',views.Analysis.as_view(),name='an'),
    path('student/',views.Student.as_view(),name='s'),
    path('dept/',views.Department.as_view(),name='dpet'),
]