from django.urls import path

from . import views as ves

app_name = 'complaints'

urlpatterns = [ 
    path('send-complaint',ves.send_complaints,name='send_complaints'),
    # student complaints
    path('my-complaints',ves.student_complaints,name='student_complaints'),
    path('view-complaint/<int:complaint_id>',ves.view_complaint_detailed,name='view_detailed'),
    path('edit-complaint/<int:complaint_id>',ves.edit_student_complaint,name='edit_complaint'),
]