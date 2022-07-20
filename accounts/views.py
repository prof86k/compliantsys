from http.client import HTTPResponse
from datetime import date, datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse,HttpRequest
from django.contrib import messages
from . import forms as fms
from . import models as mdl
from complaintsApi import models as cmdl


# Create your views here.
def users_login(request: HttpRequest) -> HTTPResponse:
    if request.method == 'POST':
        form = fms.UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user=user)
                logged_in_user = get_object_or_404(mdl.User,username=request.user)
                if logged_in_user.is_it_support:
                    pass
                elif logged_in_user.is_student:
                    return redirect('accounts:student_dashboard')
                elif logged_in_user.is_hod:
                    pass
                elif logged_in_user.is_dean:
                    pass
                elif logged_in_user.is_registry:
                    pass
            else:
                messages.error(request,'User or password is invalid!.')
    else:
        form = fms.UserLoginForm()
    context = {'form':form}
    return render(request, 'accounts/login.html',context)

def log_out_user(request: HttpRequest) -> HTTPResponse:
    logout(request)
    messages.info(request,'You have logged out successfully. Login again to access your dashboard.')
    return redirect('accounts:login')   

# ======================== administrators IT support =============================================
def dashboard(request: HttpRequest) -> HTTPResponse:
    users = mdl.User.objects.count()
    complaints = cmdl.Complaint.objects.count()
    new_complaints = cmdl.Complaint.current_model_count()
    resolved_complaints = cmdl.Complaint.objects.filter(
        hod_solve=True,
        dean_solve=True,
        registry_solve=True,
        support_repond=True
    ).count()
    context = {
        'users':users,'complaints':complaints,
        'resolved_complaints':resolved_complaints,
        'new_complaints':new_complaints
        }
    return render(request,'accounts/admins/dashboard.html',context)

def profile(request: HttpRequest) -> HTTPResponse:
    context = {}
    return render(request,'accounts/admins/profile.html',context)

def create_faculty(request: HttpRequest) -> HTTPResponse:
    faculties = database_models_query(mdl.Faculty,request.user)
    if request.method == 'POST':
        form = fms.FacultyForm(request.POST)
        if form.is_valid():
            new_faculty = form.save(commit=False)
            try:
                new_faculty.user = request.user
                new_faculty.save()
                messages.success(request,'Save Operation successful.')
                return redirect('accounts:create_faculty')
            except Exception as e:
                messages.error(request,'Save operation failed!')
                return redirect('accounts:create_faculty')
        messages.warning(request,'Warning: Some Inputs are incorrect.')
        return redirect('accounts:create_faculty')
    else:
        form = fms.FacultyForm()
    context = {'form':form,'faculties':faculties}
    return render(request,'accounts/admins/create_faculty.html',context)

def ajax_upload_faculties(request:HttpRequest) -> JsonResponse:
    if request.is_ajax():
        pass
    context={}
    return JsonResponse()

def create_department(request: HttpRequest) -> HTTPResponse:
    departments = database_models_query(mdl.Department,request.user)
    if request.method == 'POST':
        form = fms.DepartmentForm(request.POST)
        if form.is_valid():
            new_department = form.save(commit=False)
            try:
                new_department.user = request.user
                new_department.save()
                messages.success(request,'Save Operation successful.')
                return redirect('accounts:create_department')
            except Exception as e:
                messages.error(request,'Save operation failed!')
                return redirect('accounts:create_department')
        messages.warning(request,'Warning: Some Inputs are incorrect.')
        return redirect('accounts:create_department')
    else:
        form = fms.DepartmentForm()
    context = {'form':form,'departments':departments}
    return render(request,'accounts/admins/create_department.html',context)

def ajax_departments_upload(request: HttpRequest) -> HTTPResponse:
    if request.is_ajax():
        pass
    context = {}
    return JsonResponse()

def create_programme(request: HttpRequest) -> HTTPResponse:
    programmes = database_models_query(mdl.Programme,request.user)
    if request.method == 'POST':
        form = fms.ProgrammeForm(request.POST)
        if form.is_valid():
            new_programme = form.save(commit=False)
            try:
                new_programme.user = request.user
                new_programme.save()
                messages.success(request,'Save operation successfull.')
                return redirect('accounts:create_programme')
            except Exception as e:
                messages.error(request,'Save operation failed.')
                return redirect('accounts:create_programme')
        messages.warning(request,'Warning: Some Inputs are incorrect.')
        return redirect('accounts:create_programme')
    else:
        form = fms.ProgrammeForm()
    context = {'form':form,'programmes':programmes}
    return render(request,'accounts/admins/create_programme.html',context)

def database_models_query(model,user):
    'Query from any models to return the query object'
    resuts = model.objects.filter(user=user).all()
    if resuts is None:
        results = model.objects.all()
    return results

def ajax_programmes_upload(request: HttpRequest) -> JsonResponse:
    if request.is_ajax():
        pass
    context = {}
    return JsonResponse()

def create_user(request: HttpRequest) -> HTTPResponse:
    users = mdl.User.objects.order_by('-date_joined').all()
    if request.method == "POST":
        form = fms.CreateNewUserForm(request.POST,files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = "com2022"
            email = form.cleaned_data.get('email')
            profile_picture = form.cleaned_data.get('profile_picture')
            hod = form.cleaned_data.get('hod')
            student = form.cleaned_data.get('student')
            dean = form.cleaned_data.get('dean')
            registry = form.cleaned_data.get('registry')
            it_support = form.cleaned_data.get('it_support')
            try:
                new_user = mdl.User(username=username,email=email,profile_picture=profile_picture,is_hod=hod,
                is_student=student,is_dean=dean,is_registry=registry,is_it_support=it_support)
                new_user.set_password(password)
                new_user.save()
                if new_user.is_student:
                    mdl.Student.objects.create(user=new_user)
                elif new_user.is_hod:
                    mdl.Student.objects.create(user=new_user)
                elif new_user.is_dean:
                    mdl.Dean.objects.create(user=new_user)
                elif new_user.is_registry:
                    mdl.Registry.objects.create(user=new_user)
                elif new_user.is_it_support:
                    mdl.Itsupport.objects.create(user=new_user)
                messages.success(request,message ="User created")
                return redirect("accounts:create_user")
            except Exception as e:
                messages.error(request,f"Some Fields Are Not Valid {e}")
                return redirect("accounts:create_user")
        else:
            messages.error(request,f"Some Fields Are Not Valid {form.errors}")
            return redirect("accounts:create_user")                
    else:
        form = fms.CreateNewUserForm()
    context = {'form':form,'users':users}
    return render(request,'accounts/admins/create_user.html',context)

def ajax_user_upload(request:HttpRequest) -> JsonResponse:
    if request.is_ajax():
        pass
    context = {}
    return JsonResponse

def show_all_users(request:HttpRequest) -> HTTPResponse:
    users = mdl.User.objects.order_by('-date_joined').all()
    context = {
        'users': users
    }
    return render(request,'accounts/admins/users.html',context)

def edit_faculty(request: HttpRequest,faculty_id) -> HTTPResponse:
    context = {}
    return render(request,'accounts/admins/edit_faculty.html',context)

def edit_department(request: HttpRequest,department_id) -> HTTPResponse:
    context = {}
    return render(request,'accounts/admins/edit_department.html',context)

def edit_programme(request: HttpRequest,programme_id) -> HTTPResponse:
    context = {}
    return render(request,'accounts/admins/edit_programme.html',context)

# =========================== student site ================================
def student_dashboard(request: HttpRequest) -> HTTPResponse:
    complaints = cmdl.Complaint.objects.filter(complainer=request.user).count()
    current_complaints = cmdl.Complaint.user_current_model_count(request.user)
    resolved_complaints = cmdl.Complaint.objects.filter(resolved_complaint=True,complainer=request.user).count()
    unresolved_complaints = cmdl.Complaint.objects.filter(resolved_complaint=False,complainer=request.user).count()
    context = {'complaints':complaints,'new_complains':current_complaints,
                'resolved':resolved_complaints,'unresolved':unresolved_complaints}
    return render(request,'accounts/student/dashboard.html',context)

def student_profile(request: HttpRequest ) -> HTTPResponse:
    context = {}
    return render(request,'accounts/student/profile.html',context)

# =========================== HOD site ========================
def hod_dashboard(request: HttpRequest) -> HTTPResponse:
    context = {}
    return render(request,'accounts/hod/dashboard.html',context)

def hod_add_student(request: HttpRequest) -> HTTPResponse:
    context = {}
    return render(request,'accounts/hod/add_student.html',context)

def students(request: HttpRequest) -> HTTPResponse:
    context = {}
    return render(request,'accounts/hod/students.html',context)

# =========================== Dean site =================================
def dean_dashboard(request: HttpRequest) -> HTTPResponse:
    context = {}
    return render(request,'accounts/dean/dashboard.html',context)

# ======================== registry site ==================================
def registry_dashbaord(request: HttpRequest) -> HTTPResponse:
    context = {}
    return render(request,'accounts/registry/dashboard.html',context)