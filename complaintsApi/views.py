from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . import froms as fms
from . import models as mdl
from accounts import models as acmdl

import complaintsApi

# Create your views here.
def admin_send_message(request):
    context = {}
    return render(request,'complaintsApi/admins/send_message.html',context)

def send_complaints(request):
    complaints = mdl.Complaint.objects.filter(complainer=request.user).order_by("-date_updated").all()
    if request.method == "POST":
        form = fms.ComplaintCreationForm(request.POST)
        if form.is_valid():
            new_complaint = form.save(commit=False)
            new_complaint.complainer = request.user
            new_complaint.save()
            messages.success(request,'Sent')
            return redirect('complaints:send_complaints')
        else:
            messages.error(request,'Error occurred Check Your Fields')
    else:
        form = fms.ComplaintCreationForm()
    context = {'complaints':complaints,'form':form}
    return render(request,'complaintsApi/send_complaints.html',context)

def admin_complaints_responds(request):
    context = {}
    return render(request,'complaintsApi/admins/complaint_respond.html',context)

# =================== hod =================
def hod_send_message(request):
    context = {}
    return render(request,'complaintsApi/hod/send_message.html',context)

def hod_complaints(request):
    context = {}
    return render(request,'complaintsApi/hod/complaints.html',context)

def hod_complaints_responds(request):
    context = {}
    return render(request,'complaintsApi/hod/complaint_respond.html',context)

# ====================== deans ======================
def dean_send_message(request):
    context = {}
    return render(request,'complaintsApi/deans/send_message.html',context)

def dean_complaints(request):
    context = {}
    return render(request,'complaintsApi/deans/complaints.html',context)

def dean_complaints_responds(request):
    context = {}
    return render(request,'complaintsApi/deans/complaint_respond.html',context)

# ==================== registry ========================
def registry_send_message(request):
    context = {}
    return render(request,'complaintsApi/registry/send_message.html',context)

def registry_complaints(request):
    context = {}
    return render(request,'complaintsApi/registry/complaints.html',context)

def registry_complaints_responds(request):
    context = {}
    return render(request,'complaintsApi/registry/complaint_respond.html',context)

# ======================== students ========================
def student_send_message(request):
    context = {}
    return render(request,'complaintsApi/students/send_message.html',context)

def student_complaints(request):
    complaints = mdl.Complaint.objects.filter(complainer=request.user).order_by('-date_updated').all()
    context = {'complaints':complaints}
    return render(request,'complaintsApi/students/my_complaints.html',context)

def view_complaint_detailed(request,complaint_id):
    complaint = get_object_or_404(mdl.Complaint,pk=complaint_id,complainer=request.user)
    context = {'complaint':complaint}
    return render(request,'complaintsApi/students/view_complaint_detailed.html',context)

def edit_student_complaint(request,complaint_id):
    complaint = get_object_or_404(mdl.Complaint,pk=complaint_id,complainer=request.user)
    if request.method == 'POST':
        form = fms.ComplaintCreationForm(instance=complaint,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Update Successful')
            return redirect('complaints:edit_complaint',complaint_id=complaint_id)
    else:
        form = fms.ComplaintCreationForm(instance=complaint)
    context = {'complaint':complaint,'form':form}
    return render(request,'complaintsApi/students/edit_complaints.html',context)

def student_complaints_responds(request):
    context = {}
    return render(request,'complaintsApi/students/complaint_respond.html',context)