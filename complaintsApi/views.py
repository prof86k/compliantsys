from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . import froms as fms
from . import models as mdl
from accounts import models as acmdl

# Create your views here.
def admin_send_message(request):
    context = {}
    return render(request,'complaints/admins/send_message.html',context)

def admin_complaints(request):
    context = {}
    return render(request,'complaints/admins/complaints.html',context)

def admin_complaints_responds(request):
    context = {}
    return render(request,'complaints/admins/complaint_respond.html',context)

# =================== hod =================
def hod_send_message(request):
    context = {}
    return render(request,'complaints/hod/send_message.html',context)

def hod_complaints(request):
    context = {}
    return render(request,'complaints/hod/complaints.html',context)

def hod_complaints_responds(request):
    context = {}
    return render(request,'complaints/hod/complaint_respond.html',context)

# ====================== deans ======================
def dean_send_message(request):
    context = {}
    return render(request,'complaints/deans/send_message.html',context)

def dean_complaints(request):
    context = {}
    return render(request,'complaints/deans/complaints.html',context)

def dean_complaints_responds(request):
    context = {}
    return render(request,'complaints/deans/complaint_respond.html',context)

# ==================== registry ========================
def registry_send_message(request):
    context = {}
    return render(request,'complaints/registry/send_message.html',context)

def registry_complaints(request):
    context = {}
    return render(request,'complaints/registry/complaints.html',context)

def registry_complaints_responds(request):
    context = {}
    return render(request,'complaints/registry/complaint_respond.html',context)

# ======================== students ========================
def student_send_message(request):
    context = {}
    return render(request,'complaints/students/send_message.html',context)

def student_complaints(request):
    context = {}
    return render(request,'complaints/students/complaints.html',context)

def student_complaints_responds(request):
    context = {}
    return render(request,'complaints/students/complaint_respond.html',context)