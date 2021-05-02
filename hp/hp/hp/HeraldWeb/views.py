from chatterbot.trainers import ListTrainer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.shortcuts import render,redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .forms import TranscriptForm
from HeraldWeb.models import Transcript
from .models import Contact
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer



# Create your views here.

def homePageBef(request):
    return render(request,'WelcomePage/index.html')

def homePageAft(request):
    return render(request,'WelcomePage/UserDash.htm')

def AboutPage(request):
    return render(request,'WelcomePage/about.html')


def GalleryPage(request):
    return render(request,'WelcomePage/gallery.html')

def HomeBlog(request):
    return render(request,'WelcomePage/blogHome.html')

chatbot = ChatBot(
    'HeruBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)

training_data_quesans = open('training_data/database.txt').read().splitlines()

training_data = training_data_quesans

trainer = ListTrainer(chatbot)
trainer.train(training_data)


def chathome(request):
    return render(request,'WelcomePage/home.html')

#contact
def ContactView(request):
    if request.method == 'POST':
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact.name = name 
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()
        return render(request,'WelcomePage/contactsuccess.html', {'san': name})
    return render(request,'WelcomePage/contact.html')



# Main View Started

def GetStarted(request):
    return render(request,'student_teacher_cards.html')    

def Welcome(request):
    return render(request,'student_teacher_cards.html')     
   
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'WelcomePage/index.html')

#for showing signup/login button for Teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

#for showing signup/login button for Students
def studentsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentsclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


# for teacher signup 
def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            username = userForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)


# for student signup 
def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST': 
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            username = userForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)


#for checking user teacher, student or admin(by sumit)
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()



# render after login for teacher and teacher.
def afterlogin_view(request):
    if is_teacher(request.user):
        return redirect('teacher-dashboard')
    elif is_student(request.user):
        accountapproval=models.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'student/student_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start
#============================================================================================

# for admin dashboard view 
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    teacher_feedback = models.FeedBackTeacher.objects.all().count()
    dict={
    'total_teacher':models.Teacher.objects.all().count(),
    'total_student':models.Student.objects.all().count(),
    'teacher_feedback': models.FeedBackTeacher.objects.all().count(),
    'student_feedback': models.FeedBackStudent.objects.all().count(),
    'total_feedback':models.FeedBackTeacher.objects.all().count() + models.FeedBackStudent.objects.all().count(),
    }
    print(teacher_feedback)
    return render(request,'admin/admin_dashboard.html', context=dict)

        

# for admin view for teacher
@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    return render(request,'admin/admin_teacher.html')

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers=models.Teacher.objects.all()
    return render(request,'admin/admin_view_teacher.html',{'teachers':teachers})


# admin delete - teacher
@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')

# admin update - teacher 
@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    userForm=forms.TeacherUserForm(instance=user)
    teacherForm=forms.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST,instance=user)
        teacherForm=forms.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            messages.success(request, f'Account is Updated Successfully!')
            return redirect('admin-view-teacher')
    return render(request,'admin/update_teacher.html',context=mydict)


# admin add - teacher
@login_required(login_url='adminlogin')
def admin_add_teacher_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='CLIENT')
            my_teacher_group[0].user_set.add(user)
            messages.success(request, f'New Teacher is Added Successfully!')
        return HttpResponseRedirect('/admin-view-teacher')
    return render(request,'admin/admin_add_teacher.html',context=mydict)



# for admin view for teacher 
@login_required(login_url='adminlogin')
def admin_student_view(request):
    return render(request,'admin/admin_student.html')

@login_required(login_url='adminlogin')
def admin_approve_student_view(request):
    students=models.Student.objects.all().filter(status=False)
    return render(request,'admin/admin_approve_student.html',{'students':students})

@login_required(login_url='adminlogin')
def approve_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    student.status=True
    student.save()
    messages.success(request, f'Student is Approved Successfully!')
    return render(request,'admin/admin_approve_student_details.html')

# admin delete - student
@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')

# admin add - student
@login_required(login_url='adminlogin')
def admin_add_student_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.status=True
            student.save()
            my_student_group = Group.objects.get_or_create(name='GUEST')
            my_student_group[0].user_set.add(user)
            messages.success(request, f'New Student is Added Successfully!')
            return HttpResponseRedirect('admin-view-student')
        else:
            print('problem in form')
    return render(request,'admin/admin_add_student.html',context=mydict)



# for admin view for teacher 
@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students=models.Student.objects.all()
    return render(request,'admin/admin_view_student.html',{'students':students})


# admin update - student
@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    userForm=forms.StudentUserForm(instance=user)
    studentForm=forms.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST,instance=user)
        studentForm=forms.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            messages.success(request, f'Account is Updated Successfully!')
            return redirect('admin-view-student')
    return render(request,'admin/update_student.html',context=mydict)


#============================================================================================
# ADMIN RELATED views END
#============================================================================================


#============================================================================================
# Teacher RELATED views start
#============================================================================================
from django.db.models import Q

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacher_obj = models.Teacher.objects.get(user=request.user.id)
    feedback_data_count = models.FeedBackTeacher.objects.filter(teacher_id=teacher_obj).count()
    context = {
        "feedback_data_count":feedback_data_count ,
        "teacher_obj": teacher_obj
    }
    return render(request,'teacher/teacher_dashboard.html', context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_request_view(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/teacher_request.html',{'teacher':teacher})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_profile_view(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/teacher_profile.html',{'teacher':teacher})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def edit_teacher_profile_view(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=teacher.user_id)
    userForm=forms.TeacherUserForm(instance=user)
    teacherForm=forms.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm,'teacher':teacher}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST,instance=user)
        teacherForm=forms.TeacherForm(request.POST,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return HttpResponseRedirect('teacher-profile')
    return render(request,'teacher/edit_teacher_profile.html',context=mydict)


#============================================================================================
# Teacher RELATED views END
#============================================================================================






#============================================================================================
# Student RELATED views start
#============================================================================================

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    student_obj = models.Student.objects.get(user=request.user.id)
    feedback_data_count = models.FeedBackStudent.objects.filter(student_id=student_obj).count()
    context = {
        "feedback_data_count":feedback_data_count, 
        "student_obj": student_obj
    }
    student=models.Student.objects.get(user_id=request.user.id)
    return render(request,'student/student_dashboard.html', context)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_profile_view(request):
    student=models.Student.objects.get(user_id=request.user.id)
    return render(request,'student/student_profile.html',{'student':student})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def edit_student_profile_view(request):
    student=models.Student.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=student.user_id)
    userForm=forms.StudentUserForm(instance=user)
    studentForm=forms.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm,'student':student}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST,instance=user)
        studentForm=forms.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('student-profile')
    return render(request,'student/edit_student_profile.html',context=mydict)


#============================================================================================
# Student RELATED views end
#============================================================================================



# for aboutus and contact
def aboutus_view(request):
    return render(request,'aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})





#============================================================================================
# With Respect to Admin
#============================================================================================
def student_feedback_message(request):
    feedbacks = models.FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = models.FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def teacher_feedback_message(request):
    feedbacks = models.FeedBackTeacher.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin/teacher_feedback_template.html', context)


@csrf_exempt
def teacher_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')
    try:
        feedback = models.FeedBackTeacher.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")




#============================================================================================
# Admin, Teacher, GUEST RELATED views for Feedback  
#============================================================================================

# For Teacher 

def teacher_feedback(request):
    teacher_obj = models.Teacher.objects.get(user=request.user.id)
    feedback_data = models.FeedBackTeacher.objects.filter(teacher_id=teacher_obj)
    feedback_data_count = models.FeedBackTeacher.objects.filter(teacher_id=teacher_obj).count()
    print("The data is:", feedback_data_count) 
    context = {
        "feedback_data": feedback_data,
        "feedback_data_count": feedback_data_count,
        "teacher_obj": teacher_obj
    }
    return render(request, 'teacher/teacher_feedback.html', context)


def teacher_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('teacher_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        teacher_obj = models.Teacher.objects.get(user_id=request.user.id)

        try:
            add_feedback = models.FeedBackTeacher(teacher_id=teacher_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('teacher_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('teacher_feedback')



# For Student

def student_feedback(request):
    student_obj = models.Student.objects.get(user=request.user.id)
    feedback_data = models.FeedBackStudent.objects.filter(student_id=student_obj)
    print(feedback_data)
    context = {
        "feedback_data": feedback_data,
        "student_obj": student_obj
    }
    return render(request, 'student/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = models.Student.objects.get(user_id=request.user.id)

        try:
            add_feedback = models.FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')




@login_required(login_url='adminlogin')

# Upload/Create    
def upload(request):
    upload = TranscriptForm()
    # check = models.Transcript().objects()
    if request.method == 'POST':
        upload = TranscriptForm(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('admin-dashboard')
        else:
            # print(check.title)
            # print(check.picture)
            # print(check.description)
            return HttpResponse("Invalid!!")    
    else:
        return render(request, 'admin/admin_add_transcript.html', {'upload_transcript':upload})



def show_transcript(request):
    show = Transcript.objects.all()
    return render(request, 'student/transcript.html', {'show':show})
