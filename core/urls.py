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
    path('msubject/<int:sid>/<int:cid>/',views.Manitiory.as_view(),name='msubject'),
    path('mcfeed/<int:sid>/<int:csid>/<int:cid>/',views.ManitioryForm.as_view(),name='mfeed'),
    path('course/<int:sid>/',views.Course.as_view(),name='course'),
    # admin urls 
    path('cadmin/report/<int:staff_id>/<str:subject_code>/',views.ReportView.as_view(),name='report'),
    path('student/',views.StudentCheck.as_view(),name='student'),
    
    #auth view 
    path('auth/logout/',views.CustomLogoutView.as_view(),name='logout'),
    path('add/hod/',views.AddHodUser.as_view(),name='addhod'),
    # test view
    path('feed/',views.Feed.as_view(),name='ff'),
    #path('testlogin/',views.SLogin.as_view(),name='slogin'),

]
