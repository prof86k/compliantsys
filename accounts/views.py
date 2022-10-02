from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from . import forms as fms
from . import models as mdl
from complaintsApi import models as cmdl


# Create your views here.
def users_login(request: HttpRequest) -> HttpResponse:
    '''login of users'''
    if request.method == 'POST':
        form = fms.UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                if user.is_it_support:
                    # return to the main dashboard
                    return redirect('accounts:dashboard')
                elif user.is_student:
                    # return to the student dashboard
                    return redirect('accounts:student_dashboard')
                elif user.is_hod:
                    # return to the hod dashboard
                    return redirect('accounts:hod_dashboard')
                elif user.is_dean:
                    # return to the dean dashboard
                    return redirect('accounts:dean_dashboard')
                elif user.is_registry:
                    # return to the registry
                    return redirect('accounts:registry_dashboard')
                else:
                    messages.error(
                        request, 'Your Role Is Not Recognised In The System')
            else:
                messages.error(request, 'User or password is invalid!.')
    else:
        form = fms.UserLoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def log_out_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, 'Login again to access your dashboard.')
    return redirect('accounts:login')

# ======================== administrators IT support =============================================


@login_required()
def dashboard(request: HttpRequest) -> HttpResponse:
    users = mdl.User.objects.count()
    complaints = cmdl.Complaint.objects.count()
    new_complaints_count = cmdl.Complaint.current_model_count()
    new_complaints = cmdl.Complaint.current_complaints()
    paginator = Paginator(new_complaints, 1)
    page_number = request.GET.get('page')
    new_complaints_objs = paginator.get_page(page_number)
    resolved_complaints = cmdl.Complaint.objects.filter(
        solve=True
    ).count()
    context = {
        'users': users, 'complaints': complaints,
        'resolved_complaints': resolved_complaints,
        'new_complaints_count': new_complaints_count,
        'new_complaints_objs': new_complaints_objs
    }
    return render(request, 'accounts/admins/dashboard.html', context)


@login_required
def profile(request: HttpRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(mdl.User, id=user_id)
    mdl.UserProfile.objects.get_or_create(user=user)
    user_profile = mdl.UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = fms.UserProfileForm(
            instance=user_profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            programme = mdl.Programme.objects.filter(
                title=form.cleaned_data.get('programme')).first()
            department = mdl.Department.objects.filter(
                title=form.cleaned_data.get('department')).first()
            faculty = mdl.Faculty.objects.filter(
                title=form.cleaned_data.get('faculty')).first()
            if (user.is_student and request.user == user) or (user.is_it_support and (form.cleaned_data.get('student') == True)):
                mdl.Student.objects.get_or_create(
                    user=user, programme=programme)
                update_student = form.save(commit=False)
                update_student.programme = programme or None
                update_student.faculty = programme.department.faculty or faculty or None
                update_student.department = programme.department or department or None
                update_student.save()
                messages.success(
                    request, 'Update Successfull')
                return redirect('accounts:profile', user_id=user.id)
            elif (user.is_hod and request.user == user) or (user.is_it_support and (form.cleaned_data.get('hod') == True)):
                mdl.Hod.objects.get_or_create(user=user, department=department)
                update_hod = form.save(commit=False)
                update_hod.department = department
                update_hod.save()
                messages.success(request, 'Update Successfull')
                return redirect('accounts:profile', user_id=user.id)
            elif (user.is_dean and request.user == user) or (user.is_it_support and (form.cleaned_data.get('dean') == True)):
                mdl.Dean.objects.get_or_create(user=user, faculty=faculty)
                update_dean = form.save(commit=False)
                update_dean.faculty = faculty
                update_dean.save()
                messages.success(request, 'Update Successfull')
                return redirect('accounts:profile', user_id=user.id)
            elif (user.is_registry and request.user == user) or (user.is_it_support and (form.cleaned_data.get('registry') == True)):
                mdl.Registry.objects.get_or_create(user=user)
                form.save()
                messages.success(request, 'Update Successfull')
                return redirect('accounts:profile', user_id=user.id)
            elif (user.is_it_support and form.cleaned_data.get('it_support') == True):
                it = mdl.Itsupport.objects.get_or_create(user=user)
                print(it)
                form.save()
                messages.success(request, 'IT support Update Successfull')
                return redirect('accounts:profile', user_id=user.id)
        else:
            messages.error(request, 'Some Fields had Errors!')
            return redirect('accounts:profile', user_id=user.id)
    else:
        form = fms.UserProfileForm(instance=user_profile)
    context = {'user': user, 'form': form}
    return render(request, 'accounts/profile.html', context)


def create_faculty(request: HttpRequest) -> HttpResponse:
    faculties = database_models_query(mdl.Faculty, user=request.user)
    if request.method == 'POST':
        form = fms.FacultyForm(request.POST)
        if form.is_valid():
            new_faculty = form.save(commit=False)
            try:
                new_faculty.user = request.user
                new_faculty.save()
                messages.success(request, 'Save Operation successful.')
                return redirect('accounts:create_faculty')
            except Exception as e:
                messages.error(request, 'Save operation failed!')
                return redirect('accounts:create_faculty')
        messages.warning(request, 'Warning: Some Inputs are incorrect.')
        return redirect('accounts:create_faculty')
    else:
        form = fms.FacultyForm()
    context = {'form': form, 'faculties': faculties}
    return render(request, 'accounts/components/add_faculty.html', context)


def create_department(request: HttpRequest) -> HttpResponse:
    departments = database_models_query(mdl.Department, request.user)
    if request.method == 'POST':
        form = fms.DepartmentForm(request.POST)
        if form.is_valid():
            new_department = form.save(commit=False)
            try:
                new_department.user = request.user
                new_department.save()
                messages.success(request, 'Save Operation successful.')
                return redirect('accounts:create_department')
            except Exception as e:
                messages.error(request, 'Save operation failed!')
                return redirect('accounts:create_department')
        messages.warning(request, 'Warning: Some Inputs are incorrect.')
        return redirect('accounts:create_department')
    else:
        form = fms.DepartmentForm()
    context = {'form': form, 'departments': departments}
    return render(request, 'accounts/components/create_department.html', context)


def view_deans(request: HttpRequest) -> HttpResponse:
    '''
    @ list all the deans of the school
    '''
    deans = mdl.Dean.objects.all()
    context = {
        'deans': deans
    }
    return render(request, 'accounts/admins/deans.html', context)


def view_hods(request: HttpRequest) -> HttpResponse:
    '''
    @ list all the hods of the school
    '''
    hods = mdl.Hod.objects.all()
    context = {
        'hods': hods
    }
    return render(request, 'accounts/admins/hods.html', context)


def view_registries(request: HttpRequest) -> HttpResponse:
    '''
    @ list all the registries of the school
    '''
    registries = mdl.Registry.objects.all()
    context = {
        'registries': registries
    }
    return render(request, 'accounts/admins/registries.html', context)


def create_programme(request: HttpRequest) -> HttpResponse:
    programmes = database_models_query(mdl.Programme, request.user)
    if request.method == 'POST':
        form = fms.ProgrammeForm(request.POST)
        if form.is_valid():
            hod = mdl.Hod.objects.filter(user=request.user, department=mdl.Department.objects.filter(
                title=form.cleaned_data.get('department')).first()).first()
            new_programme = form.save(commit=False)
            try:
                if (hod) or mdl.User.objects.filter(username=request.user.username, is_it_support=True).first():
                    new_programme.user = request.user
                    new_programme.save()
                    messages.success(request, 'Save operation successfull.')
                else:
                    messages.error(
                        request, 'Sorry you can only add a prgramme to your department.')
                return redirect('accounts:create_programme')
            except Exception as e:
                messages.error(request, 'Save operation failed.')
                return redirect('accounts:create_programme')
        messages.warning(request, 'Warning: Some Inputs are incorrect.')
        return redirect('accounts:create_programme')
    else:
        form = fms.ProgrammeForm()
    context = {'form': form, 'programmes': programmes}
    return render(request, 'accounts/components/create_programme.html', context)


def database_models_query(model, user):
    'Query from any models to return the query object'
    results = model.objects.filter(user=user).all()
    if user.is_it_support or not results:
        results = model.objects.all()
    return results


def create_user(request: HttpRequest) -> HttpResponse:
    users = mdl.User.objects.order_by('-date_joined').all()
    if request.method == "POST":
        form = fms.CreateNewUserForm(request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = "com2022"
            email = form.cleaned_data.get('email')
            hod = form.cleaned_data.get('hod')
            student = form.cleaned_data.get('student')
            dean = form.cleaned_data.get('dean')
            registry = form.cleaned_data.get('registry')
            it_support = form.cleaned_data.get('it_support')
            try:
                new_user = mdl.User(username=username, email=email, is_hod=hod,
                                    is_student=student, is_dean=dean, is_registry=registry, is_it_support=it_support)
                new_user.set_password(password)
                new_user.save()
                messages.success(request, message="User created")
                return redirect("accounts:create_user")
            except Exception as e:
                messages.error(request, f"Some Fields Are Not Valid {e}")
                return redirect("accounts:create_user")
        else:
            messages.error(request, f"Some Fields Are Not Valid {form.errors}")
            return redirect("accounts:create_user")
    else:
        form = fms.CreateNewUserForm()
    context = {'form': form, 'users': users}
    return render(request, 'accounts/components/create_user.html', context)


def show_all_users(request: HttpRequest) -> HttpResponse:
    users = mdl.User.objects.order_by('-date_joined').all()
    context = {
        'users': users
    }
    return render(request, 'accounts/admins/users.html', context)


def delete_user(request: HttpRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(mdl.User, id=user_id)
    user.delete()
    messages.success(request, 'Record Deleted Successfully.')
    return redirect('accounts:users')


def edit_faculty(request: HttpRequest, faculty_id: int) -> HttpResponse:
    '''
    @ edit the created faculty information
    '''
    facutly = get_object_or_404(mdl.Faculty, id=faculty_id)
    if request.method == "POST":
        form = fms.FacultyForm(instance=facutly, data=request.POST)
        if form.is_valid():
            update_faculty = form.save(commit=False)
            update_faculty.user = request.user
            update_faculty.save()
            messages.success(
                request, 'Faculty information updated successfully.')
            return redirect('accounts:create_faculty')
    else:
        form = fms.FacultyForm(instance=facutly)
    context = {
        'form': form,
        'faculty': facutly,
    }
    return render(request, 'accounts/components/edit_faculty.html', context)


def edit_department(request: HttpRequest, department_id: int) -> HttpResponse:
    '''
    @ edit department information 
    '''
    department = get_object_or_404(mdl.Department, id=department_id)
    if request.method == 'POST':
        form = fms.DepartmentForm(instance=department, data=request.POST)
        if form.is_valid():
            update_department = form.save(commit=False)
            update_department.user = request.user
            update_department.save()
            messages.success(
                request, 'Department information updated successfully.')
            return redirect('accounts:create_department')
    else:
        form = fms.DepartmentForm(instance=department)
    context = {
        'form': form,
        'department': department,
    }
    return render(request, 'accounts/components/edit_department.html', context)


def edit_programme(request: HttpRequest, programme_id: int) -> HttpResponse:
    '''
    @ update information of a programme
    '''
    programme = get_object_or_404(mdl.Programme, id=programme_id)
    if request.method == 'POST':
        form = fms.ProgrammeForm(instance=programme, data=request.POST)
        if form.is_valid():
            update_programme = form.save(commit=False)
            update_programme.user = request.user
            update_programme.save()
            messages.success(
                request, 'Programme information updated successfully.')
            return redirect('accounts:create_programme')
    else:
        form = fms.ProgrammeForm(instance=programme)
    context = {
        'form': form,
        'programme': programme,
    }
    return render(request, 'accounts/components/edit_programme.html', context)


def delete_faculty(request: HttpRequest, faculty_id: int) -> HttpResponse:
    try:
        faculty = get_object_or_404(
            mdl.Faculty, user=request.user, id=faculty_id)
    except Exception as e:
        if get_object_or_404(mdl.User, username=request.user.username, is_it_support=True):
            faculty = get_object_or_404(mdl.Faculty, id=faculty_id)
        else:
            messages.success(request, "Delete Operation Denied!")
            return redirect('accounts:create_faculty')
    finally:
        faculty.delete()
        messages.success(request, "Delete Operation successfull")
        return redirect('accounts:create_faculty')


def delete_programme(request: HttpRequest, programme_id: int) -> HttpResponse:
    try:
        faculty = get_object_or_404(
            mdl.Programme, user=request.user, id=programme_id)
    except Exception as e:
        if get_object_or_404(mdl.User, username=request.user.username, is_it_support=True):
            faculty = get_object_or_404(mdl.Programme, id=programme_id)
        else:
            messages.success(request, "Delete Operation Denied!")
            return redirect('accounts:create_programme')
    finally:
        faculty.delete()
        messages.success(request, "Delete Operation successfull")
        return redirect('accounts:create_programme')


def delete_department(request: HttpRequest, department_id: int) -> HttpResponse:
    try:
        faculty = get_object_or_404(
            mdl.Department, user=request.user, id=department_id)
    except Exception as e:
        if get_object_or_404(mdl.User, username=request.user.username, is_it_support=True):
            faculty = get_object_or_404(mdl.Department, id=department_id)
        else:
            messages.success(request, "Delete Operation Denied!")
            return redirect('accounts:create_department')
    finally:
        faculty.delete()
        messages.success(request, "Delete Operation successfull")
        return redirect('accounts:create_department')

# =========================== student site ================================


def student_dashboard(request: HttpRequest) -> HttpResponse:
    if get_object_or_404(mdl.User, username=request.user):
        complaints = cmdl.Complaint.objects.filter(
            complainer=request.user).count()
        current_complaints = cmdl.Complaint.user_current_model_count(
            request.user)
        resolved_complaints = cmdl.Complaint.objects.filter(
            solve=True, complainer=request.user).count()
        unresolved_complaints = cmdl.Complaint.objects.filter(
            solve=False, complainer=request.user).count()
    else:
        complaints = cmdl.Complaint.objects.count()
        current_complaints = cmdl.Complaint.current_model_count()
        resolved_complaints = cmdl.Complaint.objects.filter(
            resolved_complaint=True).count()
        unresolved_complaints = cmdl.Complaint.objects.filter(
            resolved_complaint=False).count()
    context = {'complaints': complaints, 'new_complains': current_complaints,
               'resolved': resolved_complaints, 'unresolved': unresolved_complaints}
    return render(request, 'accounts/student/dashboard.html', context)

# =========================== HOD site ========================


def hod_dashboard(request: HttpRequest) -> HttpResponse:
    complaints: list = cmdl.Complaint.admin_user_users_complaints(
        user=request.user)
    new_complaints_count: int = cmdl.Complaint.current_model_count()
    new_complaints: list = cmdl.Complaint.current_complaints()
    paginator = Paginator(new_complaints, 5)
    page_number = request.GET.get('page')
    new_complaints_objs = paginator.get_page(page_number)
    resolved_complaints: int = cmdl.Complaint.objects.filter(
        solve=True, forward_to_user=request.user
    ).count()
    context = {
        'complaints': len(complaints),
        'resolved_complaints': resolved_complaints,
        'new_complaints_count': new_complaints_count,
        'new_complaints_objs': new_complaints_objs
    }
    return render(request, 'accounts/hod/dashboard.html', context)


def hod_students(request: HttpRequest) -> HttpResponse:
    '''
        @ hod student
    '''
    hod = get_object_or_404(mdl.Hod, user=request.user)
    user_deparmtent = get_object_or_404(mdl.UserProfile, user=hod.user)
    context = {
        'hod': hod,
        'user_deparmtent': user_deparmtent,
    }
    return render(request, 'accounts/hod/students.html', context)

# =========================== Dean site =================================


def dean_dashboard(request: HttpRequest) -> HttpResponse:
    '''
        @ deans dashboard
    '''
    complaints = cmdl.Complaint.dean_users_complaints(user=request.user)
    new_forwarded_complaints = cmdl.Complaint.dean_users_new_complaints(
        user=request.user)
    forwarded_solved_complaints = cmdl.Complaint.dean_users_new_complaints(
        user=request.user, solve=True)
    paginator = Paginator(new_forwarded_complaints, 5)
    page_number = request.GET.get('page')
    new_complaints_objs = paginator.get_page(page_number)
    context = {
        'complaints': len(complaints), 'new_complaints_objs': new_complaints_objs,
        'new_forward_complaints_count': len(new_forwarded_complaints),
        'forwarded_solved_complaints': len(forwarded_solved_complaints),
    }
    return render(request, 'accounts/dean/dashboard.html', context)

# ======================== registry site ==================================


def registry_dashbaord(request: HttpRequest) -> HttpResponse:
    '''
        @ registry 
    '''
    complaints = cmdl.Complaint.dean_users_complaints(user=request.user)
    new_forwarded_complaints = cmdl.Complaint.dean_users_new_complaints(
        user=request.user)
    forwarded_solved_complaints = cmdl.Complaint.dean_users_new_complaints(
        user=request.user, solve=True)
    paginator = Paginator(new_forwarded_complaints, 5)
    page_number = request.GET.get('page')
    new_complaints_objs = paginator.get_page(page_number)
    context = {
        'complaints': len(complaints), 'new_complaints_objs': new_complaints_objs,
        'new_forward_complaints_count': len(new_forwarded_complaints),
        'forwarded_solved_complaints': len(forwarded_solved_complaints),
    }
    return render(request, 'accounts/registry/dashboard.html', context)
