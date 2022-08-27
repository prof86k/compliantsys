from django.urls import path

from . import views as ves

app_name = 'complaints'

urlpatterns = [
    path('view-complaints', ves.admin_complaints_responds, name='view_complaints'),
    path('send-complaint', ves.send_complaints, name='send_complaints'),
    path('forward/<int:complaint_id>/complaint',
         ves.forward_complaints, name='forward'),
    # student complaints
    path('my-complaints', ves.my_complaints, name='my_complaints'),
    path('view-complaint/<int:complaint_id>',
         ves.view_complaint_detailed, name='view_detailed'),
    path('complain-details/<int:complain_id>',
         ves.view_complaints_details, name='veiw_complain'),
    path('edit-complaint/<int:complaint_id>',
         ves.edit_student_complaint, name='edit_complaint'),
    path('resolve-complaint/<int:complaint_id>',
         ves.resolve_complaint, name='resolve'),
    path('reverse/resolve-complaint/<int:complaint_id>',
         ves.reverse_resolve_complaint, name='reverse_resolve'),
    path('delete-complaint/<int:complaint_id>',
         ves.delete_complaint, name='delete_complaint'),
]
