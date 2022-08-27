from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpRequest
from . import froms as fms
from . import models as mdl
from accounts import models as acmdl

import complaintsApi

# Create your views here.


def admin_send_message(request):
    context = {}
    return render(request, 'complaintsApi/admins/send_message.html', context)


def send_complaints(request):
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
            new_complaint.save()
            messages.success(request, 'Sent')
            return redirect('complaints:send_complaints')
        else:
            messages.error(request, 'Error occurred Check Your Fields')
    else:
        form = fms.ComplaintCreationForm()
    context = {'complaints': complaints, 'form': form}
    return render(request, 'complaintsApi/send_complaints.html', context)


def admin_complaints_responds(request):
    '''
    @ get all compliants by students
    '''
    complaints = mdl.Complaint.objects.order_by('-date_created').all()
    context = {
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
                user = acmdl.User.objects.filter(is_dean=True).first()
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
# =================== hod =================


def hod_send_message(request):
    context = {}
    return render(request, 'complaintsApi/hod/send_message.html', context)


def hod_complaints(request):
    context = {}
    return render(request, 'complaintsApi/hod/complaints.html', context)


def hod_complaints_responds(request):
    context = {}
    return render(request, 'complaintsApi/hod/complaint_respond.html', context)

# ====================== deans ======================


def dean_send_message(request):
    context = {}
    return render(request, 'complaintsApi/deans/send_message.html', context)


def dean_complaints(request):
    context = {}
    return render(request, 'complaintsApi/deans/complaints.html', context)


def dean_complaints_responds(request):
    context = {}
    return render(request, 'complaintsApi/deans/complaint_respond.html', context)

# ==================== registry ========================


def registry_send_message(request):
    context = {}
    return render(request, 'complaintsApi/registry/send_message.html', context)


def registry_complaints(request):
    context = {}
    return render(request, 'complaintsApi/registry/complaints.html', context)


def registry_complaints_responds(request):
    context = {}
    return render(request, 'complaintsApi/registry/complaint_respond.html', context)

# ======================== students ========================


def student_send_message(request):
    context = {}
    return render(request, 'complaintsApi/students/send_message.html', context)


def my_complaints(request):
    complaints = mdl.Complaint.objects.filter(
        complainer=request.user).order_by('-date_updated').all()
    context = {'complaints': complaints}
    return render(request, 'complaintsApi/students/my_complaints.html', context)


def view_complaint_detailed(request, complaint_id):
    complaint = get_object_or_404(
        mdl.Complaint, pk=complaint_id, complainer=request.user)
    context = {'complaint': complaint}
    return render(request, 'complaintsApi/students/view_complaint_detailed.html', context)


def view_complaints_details(request: HttpRequest, complain_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ show the detailes of the complaints
    '''
    complain = get_object_or_404(mdl.Complaint, pk=complain_id)
    context = {'complain': complain}

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


def edit_student_complaint(request, complaint_id):
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
    context = {'complaint': complaint, 'form': form}
    return render(request, 'complaintsApi/students/edit_complaints.html', context)


def delete_complaint(request: HttpRequest, complaint_id: int) -> HttpResponse:
    complaint = get_object_or_404(
        mdl.Complaint, id=complaint_id, complainer=request.user)
    complaint.delete()
    messages.success(request, 'Complaints Deleted Successfully.')
    return redirect('complaints:my_complaints')


def student_complaints_responds(request):
    context = {}
    return render(request, 'complaintsApi/students/complaint_respond.html', context)
