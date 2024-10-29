from django.urls import path 
from core import views
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('team/',views.Team.as_view(),name='team'),
    path('error/',views.Error.as_view(),name='error'),
    path('staff/<int:id>/<str:subject>/',views.Profile.as_view(),name='prof'),
    path('class/<int:semester>/<str:section>/',views.ClassProfile.as_view(),name='class_prof'),
    path('login/',views.StudentLogin.as_view(),name='login'),
    path('feed/<int:sid>/<int:catid>/',views.FeedBackView.as_view(),name='feed'),
    path('search/',views.Search.as_view(),name='search'),
    path('msubject/<int:sid>/<int:count>/',views.Manitiory.as_view(),name='msubject'),
    path('mcfeed/<int:sid>/<int:csid>/<int:count>/',views.ManitioryForm.as_view(),name='mfeed'),
    #api urls 
    path('api/status/<int:sid>/<str:subject_code>/',views.StaffStatsView.as_view(),name='status'),
    path('api/class/status/<int:semester>/<str:section>/',views.ClassStatsView.as_view(),name='cstatus'),
    path('classstaff/subjects/<int:year>/', views.get_subjects, name='get_subjects'),
    # admin urls 
    path('cadmin/report/',views.ReportView.as_view(),name='report'),
    path('student/',views.StudentCheck.as_view(),name='student'),
]
