from django.urls import path
from core import views
urlpatterns = [
    #student urls 
    path('',views.Home.as_view(),name='home'),
    path('team/',views.Team.as_view(),name='team'),
    path('error/',views.Error.as_view(),name='error'),
    path('analysis/staffsub/<int:id>/<str:subject>/',views.Profile.as_view(),name='ana-staffsub'),
    path('analysis/class/<int:semester>/<str:section>/<str:dept>/',views.ClassProfile.as_view(),name='ana-class'),
    path("analysis/staff/<int:id>/<str:dept>/", views.StaffProfile.as_view(), name="ana-staff"),
    path("analysis/dept/<str:dept>/", views.DeptProfile.as_view(), name="ana-dept"),
    path('login/',views.StudentLogin.as_view(),name='login'),
    path('feed/<int:sid>/<int:fid>/',views.FeedBackView.as_view(),name='feed'),
    path('cadmin/search/<str:mode>/<int:ana>/',views.Search.as_view(),name='search'),
    path('cadmin/csearch/<str:mode>/<int:ana>/',views.ClassSearch.as_view(),name='csearch'),
    path('msubject/<int:sid>/<int:cid>/<int:fid>/',views.Manitiory.as_view(),name='msubject'),
    path('mcfeed/<int:sid>/<int:cid>/<int:fid>/<str:subid>/',views.ManitioryForm.as_view(),name='mfeed'),
    path('course/<int:sid>/<int:fid>/',views.Course.as_view(),name='course'),

    #prinicipal urls 
    path('prinicipal/',views.PrinicpalDash.as_view(),name='prinicpal'),
    path('add/hod/',views.AddHodUser.as_view(),name='addhod'),
    path('prinicipal/report/<str:mode>/<str:key>/<str:dept>/',views.PReport.as_view(),name='preport'),
    path('prinicipal/creport/<str:mode>/<str:sec>/<int:sem>/<str:dept>/',views.ClassReport.as_view(),name='classreport'),
    path('prinicipal/dreport/<str:dept>/',views.DeptReport.as_view(),name='d-report'),
    path('prinicipal/reportmode/',views.ReportMode.as_view(),name='reportmode'),
    path("prinicipal/searchmode/",views.AnalysisMode.as_view(), name="anamode"),
    path('prinicipal/promote/',views.StudentPromote.as_view(),name='stu-pro'),
    path("prinicipal/comment/search/", views.CommentSearch.as_view(), name="comt-search"),
    path("cadmin/comment/<int:sid>/", views.CommentView.as_view(), name="comt-view"),
    #auth view 
    path('auth/logout/',views.CustomLogoutView.as_view(),name='logout'),
]
