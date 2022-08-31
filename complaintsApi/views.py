from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from . import froms as fms
from . import models as mdl
from accounts import models as acmdl

# Create your views here.


def send_complaints(request: HttpRequest) -> HttpResponse:
    '''
        @ Users send their complaints
        @ each complaints is sent by a user
    '''
    complaints = mdl.Complaint.objects.filter(
        complainer=request.user).order_by("-date_updated").all()
    if request.method == "POST":
        form = fms.ComplaintCreationForm(request.POST)
        if form.is_valid():
            new_complaint = form.save(commit=False)
            new_complaint.complainer = request.user
            department_hod_user = request.user.user_profile.department.department_hod
            new_complaint.forward_to_user = department_hod_user.user
            new_complaint.save()
            messages.success(request, 'Sent')
            return redirect('complaints:send_complaints')
        else:
            messages.error(request, 'Error occurred Check Your Fields')
    else:
        form = fms.ComplaintCreationForm()
    context: dict = {'complaints': complaints, 'form': form}
    return render(request, 'complaintsApi/send_complaints.html', context)


def admin_complaints_responds(request: HttpRequest) -> HttpResponse:
    '''
        @ get all compliants by students
    '''
    complaints = mdl.Complaint.objects.order_by('-date_created').all()
    context: dict = {
        'complaints': complaints,
    }
    return render(request, 'complaintsApi/compliant_list.html', context)


def forward_complaints(request: HttpRequest, complaint_id: int, *args, **kwargs) -> HttpResponse:
    '''
        @ forword the complaint to the next level
    '''
    complaint = get_object_or_404(mdl.Complaint, id=complaint_id)
    if request.method == 'POST':
        form = fms.ForwardComplainForm(request.POST)
        if form.is_valid():
            forward_to = form.cleaned_data.get('forward_to')
            user_repond_text = form.cleaned_data.get('user_repond_text')
            if forward_to == 'dean':
                faculty = complaint.complainer.user_profile.faculty
                user = acmdl.Dean.objects.filter(faculty=faculty).first().user
            elif forward_to == 'registry':
                user = acmdl.User.objects.filter(is_registry=True).first()
            else:
                user = acmdl.User.objects.filter(is_it_support=True).first()
            complaint.forward_to_user = user
            complaint.user_repond_text = user_repond_text
            complaint.forward_to = forward_to
            complaint.forward = True
            complaint.save()
            messages.success(
                request, f'Complaints Forward to {forward_to.title()}')
            return redirect('complaints:forward', complaint_id=complaint.id)
    else:
        form = fms.ForwardComplainForm()
    context = {
        'complaint': complaint,
        'form': form
    }
    return render(request, 'complaintsApi/forward_complaint.html', context)


def view_new_complaint(request: HttpRequest) -> HttpResponse:
    '''
        @ view all the newly sent complaints
    '''
    new_complaints = mdl.Complaint.current_complaints()

    context: dict = {'new_complaints': new_complaints}

    return render(request, 'complaintsApi/new_complaints.html', context)


def view_resolved_complaint(request: HttpRequest) -> HttpResponse:
    '''
        @ view all the resolved sent complaints
    '''
    resolved_complaints = mdl.Complaint.objects.filter(solve=True).all()

    context: dict = {'resolved_complaints': resolved_complaints}

    return render(request, 'complaintsApi/resolved_complaints.html', context)
# =================== hod ======================================================


def hod_complaints(request: HttpRequest) -> HttpResponse:
    '''
        @ list all the complaints sents to hod
    '''
    complaints = mdl.Complaint.objects.filter(
        solve=False, forward_to_user=request.user).all()
    context: dict = {
        'complaints': complaints
    }
    return render(request, 'complaintsApi/hod/complaints.html', context)
# ====================== deans ======================


def dean_complaints(request: HttpRequest) -> HttpResponse:
    ''' 
        @ list all complaints forwarded to deans of the faculty
    '''
    complaints = mdl.Complaint.objects.filter(
        solve=False, forward=True, forward_to_user=request.user).all()
    context: dict = {'complaints': complaints}
    return render(request, 'complaintsApi/deans/complaints.html', context)


def new_forwarded_complaints(request: HttpRequest) -> HttpResponse:
    '''
        @ view newly forwarded complaints
    '''
    if request.user.is_dean:
        new_forwards: list = mdl.Complaint.dean_users_new_complaints(
            user=request.user)
    elif request.user.is_hod:
        new_forwards: list = mdl.Complaint.hod_users_new_complaints(
            user=request.user)
    context: dict = {
        'new_forwards': new_forwards,
    }
    return render(request, 'complaintsApi/deans/new_complaints.html', context)


def resolved_forwarded_complaints(request: HttpRequest) -> HttpResponse:
    '''
        @ view resolved forwarded complaints
    '''
    if request.user.is_dean:
        resolved_forwards: list = mdl.Complaint.dean_users_new_complaints(
            user=request.user, solve=True)
    else:
        resolved_forwards: list = mdl.Complaint.objects.filter(
            forward_to_user=request.user, solve=True)
    context: dict = {
        'resolved_forwards': resolved_forwards,
    }
    return render(request, 'complaintsApi/deans/resolved.html', context, status=200)
# ==================== registry =======================


def registry_complaints(request: HttpRequest) -> HttpResponse:
    '''
        @ list all the complaints forwarded to the registry
    '''
    complaints = mdl.Complaint.objects.filter(
        solve=False, forward=True, forward_to_user=request.user).all()
    context: dict = {'complaints': complaints}
    return render(request, 'complaintsApi/registry/complaints.html', context)
# ======================== students ========================


def my_complaints(request: HttpRequest) -> HttpResponse:
    complaints = mdl.Complaint.objects.filter(
        complainer=request.user).order_by('-date_updated').all()
    context = {'complaints': complaints}
    return render(request, 'complaintsApi/students/my_complaints.html', context)


def view_complaint_detailed(request: HttpRequest, complaint_id: int) -> HttpResponse:
    complaint = get_object_or_404(
        mdl.Complaint, pk=complaint_id, complainer=request.user)
    context: dict = {'complaint': complaint}
    return render(request, 'complaintsApi/students/view_complaint_detailed.html', context)


def view_complaints_details(request: HttpRequest, complain_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ show the detailes of the complaints
    '''
    complain = get_object_or_404(mdl.Complaint, pk=complain_id)
    context: dict = {'complain': complain}

    return render(request, 'complaintsApi/complaint_detailes.html', context)


def resolve_complaint(request: HttpRequest, complaint_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ resolve the complaints
    '''
    complaint = get_object_or_404(mdl.Complaint, pk=complaint_id)
    complaint.solve = True
    complaint.save()
    messages.success(request, 'Complaint Resolved')
    return redirect('complaints:veiw_complain', complain_id=complaint_id)


def reverse_resolve_complaint(request: HttpRequest, complaint_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ severse resolve the complaints
    '''
    complaint = get_object_or_404(mdl.Complaint, pk=complaint_id)
    complaint.solve = False
    complaint.save()
    messages.success(request, 'Resolved Complaint Reversed')
    return redirect('complaints:veiw_complain', complain_id=complaint_id)


def edit_student_complaint(request: HttpRequest, complaint_id: int) -> HttpResponse:
    complaint = get_object_or_404(
        mdl.Complaint, pk=complaint_id, complainer=request.user)
    if request.method == 'POST':
        form = fms.ComplaintCreationForm(instance=complaint, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Successful')
            return redirect('complaints:edit_complaint', complaint_id=complaint_id)
    else:
        form = fms.ComplaintCreationForm(instance=complaint)
    context: dict = {'complaint': complaint, 'form': form}
    return render(request, 'complaintsApi/students/edit_complaints.html', context)


def delete_complaint(request: HttpRequest, complaint_id: int) -> HttpResponse:
    complaint = get_object_or_404(
        mdl.Complaint, id=complaint_id, complainer=request.user)
    complaint.delete()
    messages.success(request, 'Complaints Deleted Successfully.')
    return redirect('complaints:my_complaints')
