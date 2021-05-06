from django.contrib import admin
from django.urls import path
from HeraldWeb import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [

    path('', views.homePageBef, name='startPG'),
    path('gallery/', views.GalleryPage, name='gallery'),
    path('homeBlog/', views.HomeBlog, name='homeBlog'),
    path('contact/', views.ContactView, name='contact'),

    # path('bot/', bot, name='bot'),
    path('chatbotHome/',views.chathome, name='chltu'),
    path('get-response/', views.get_response),
   
    # actual urls start 
    path('start/', views.GetStarted, name='start'),
    path('', views.home_view,name=''),

    # For after click
    path('adminclick', views.adminclick_view, name = 'adminclick'), 
    path('teacherclick', views.teacherclick_view,name = 'teacherclick' ),
    path('studentclick', views.studentsclick_view, name = 'studentclick'),

    # For Signup
    path('teachersignup', views.teacher_signup_view,name='teachersignup'),
    path('studentsignup', views.student_signup_view,name='studentsignup'),

    # For Login
    path('login/', LoginView.as_view(template_name='student/studentlogin.html'),name='login'),
    path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
    path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
    path('adminlogin', LoginView.as_view(template_name='admin/adminlogin.html'),name='adminlogin'),
    path('accounts/profile/', views.Welcome, name='adminlogin'),

    # Admin Power for Teacher and Student 
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-view-teacher',views.admin_view_teacher_view,name='admin-view-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('admin-add-teacher', views.admin_add_teacher_view,name='admin-add-teacher'),
    path('teacher-request', views.teacher_request_view,name='teacher-request'),
    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-profile', views.teacher_profile_view,name='teacher-profile'),
    path('edit-teacher-profile', views.edit_teacher_profile_view,name='edit-teacher-profile'),

    # Admin Power for Guest
    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student',views.admin_view_student_view,name='admin-view-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('admin-add-student',views.admin_add_student_view,name='admin-add-student'),
    path('admin-approve-student',views.admin_approve_student_view,name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('student-profile', views.student_profile_view,name='student-profile'),
    path('edit-student-profile', views.edit_student_profile_view,name='edit-student-profile'),
    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),



    # For After login and logout 
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),

    # For Contact us and About us
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),


   # For Feedback  
   path('student_feedback_message/', views.student_feedback_message, name="student_feedback_message"),
   path('student_feedback_message_reply/', views.student_feedback_message_reply, name="student_feedback_message_reply"),
   path('teacher_feedback_message/', views.teacher_feedback_message, name="teacher_feedback_message"),
   path('teacher_feedback_message_reply/',views.teacher_feedback_message_reply, name="teacher_feedback_message_reply"),

   path('teacher_feedback/', views.teacher_feedback, name="teacher_feedback"),
   path('teacher_feedback_save/',views.teacher_feedback_save, name="teacher_feedback_save"),

   path('student_feedback/', views.student_feedback, name="student_feedback"),
   path('student_feedback_save/',views.student_feedback_save, name="student_feedback_save"),


    path('admin-add-transcript',views.upload,name='admin-add-transcript'),
    path('show', views.show_transcript, name = 'show'),

  
  
]
