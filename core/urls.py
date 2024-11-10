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
    path('classstaff/subjects/<int:year>/', views.get_subjects, name='get_subjects'),
    path('api/staff/<int:sid>/<str:subject_code>/',views.StaffData.as_view(),name='staff'),
    path('api/classdata/<int:semester>/<str:section>/',views.ClassData.as_view(),name='class'),
    # admin urls 
    path('cadmin/report/<int:staff_id>/<str:subject_code>/',views.ReportView.as_view(),name='report'),
    path('student/',views.StudentCheck.as_view(),name='student'),
    
    # test views 
    path('sub/',views.SubjectViews.as_view(),name='sub'),
]
