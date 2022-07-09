from http.client import HTTPResponse
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
                logged_in_user = get_object_or_404(mdl.User,username=request.user).first()
                if logged_in_user.is_it_support:
                    pass
                elif logged_in_user.is_student:
                    pass
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
    faculties = mdl.Faculty.objects.count()
    departments = mdl.Department.objects.count()
    programmes = mdl.Programme.objects.count()
    context = {
        'users':users,'complaints':complaints,
        'faculties':faculties,'departments':departments,
        'programmes':programmes,
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
    context = {}
    return render(request,'accounts/admins/create_user.html',context)

def ajax_user_upload(request:HttpRequest) -> JsonResponse:
    if request.is_ajax():
        pass
    context = {}
    return JsonResponse

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
    context = {}
    return render(request,'accounts/students/dashboard.html',context)

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