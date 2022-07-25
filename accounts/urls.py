from django.urls import path
from . import views as vi

app_name='accounts'

urlpatterns = [
    path('',vi.users_login,name='login'),
    path('logout',vi.log_out_user,name='logout'),
    path('dashboard',vi.dashboard,name='dashboard'),
    path('profile/<int:user_id>',vi.profile,name='profile'),
    # ========================= Main admin create option =========================================
    path('create-faculty',vi.create_faculty,name='create_faculty'),
    path('upload-faculties',vi.ajax_upload_faculties,name='upload_faculties'),
    path('create-department',vi.create_department,name='create_department'),
    path('upload-departments',vi.ajax_departments_upload,name='upload_departments'),
    path('create-programme',vi.create_programme,name='create_programme'),
    path('upload-programmes',vi.ajax_programmes_upload,name='upload_programme'),
    path('show-users',vi.show_all_users,name='users'),
    path('create-user',vi.create_user,name='create_user'),
    path('upload-users',vi.ajax_user_upload,name='upload_users'),
    # =========================== Main  admin Edit option ========================================
    path('edit-faculty/<int:faculty_id>',vi.edit_faculty,name='edit_faculty'),
    path('edit-department/<int:department_id>',vi.edit_department,name='edit_department'),
    path('edit-programme/<int:programme>',vi.edit_programme,name='edit_programme'),
    # ============================== Student option ==============================================
    path('student/dashboard',vi.student_dashboard,name='student_dashboard'),
    # ============================== HOD option ==================================================
    path('hod/dashboard',vi.hod_dashboard,name='hod_dashboard'),
    path('hod/add-student',vi.hod_add_student,name='hod_add_student'),
    path('student',vi.students,name='students'),
    # ============================== Dean Option =================================================
    path('dean/dashboard',vi.dean_dashboard,name='dean_dashboard'),
    # ============================== Registry option =============================================
    path('registry/dashboard',vi.registry_dashbaord,name='registry_dashboard'),
]