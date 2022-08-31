from django.urls import path
from . import views as vi

app_name = 'accounts'

urlpatterns = [
    path('', vi.users_login, name='login'),
    path('logout', vi.log_out_user, name='logout'),
    path('dashboard', vi.dashboard, name='dashboard'),
    path('profile/<int:user_id>', vi.profile, name='profile'),
    # ========================= Main admin create option =========================================
    path('create-faculty', vi.create_faculty, name='create_faculty'),
    path('view-hods', vi.view_hods, name='hods'),
    path('view-registries', vi.view_registries, name='registry'),
    path('view-deans', vi.view_deans, name='deans'),
    path('create-department', vi.create_department, name='create_department'),
    path('create-programme', vi.create_programme, name='create_programme'),
    path('show-users', vi.show_all_users, name='users'),
    path('create-user', vi.create_user, name='create_user'),
    path('delete-user/<int:user_id>', vi.delete_user, name='delete_user'),
    # =========================== Main  admin Edit option ========================================
    path('edit-faculty/<int:faculty_id>', vi.edit_faculty, name='edit_faculty'),
    path('edit-department/<int:department_id>',
         vi.edit_department, name='edit_department'),
    path('edit-programme/<int:programme_id>',
         vi.edit_programme, name='edit_programme'),
    # ====================== Delete record =============================================
    path('delete-faculty/<int:faculty_id>',
         vi.delete_faculty, name="delete_faculty"),
    path('delete-programme/<int:programme_id>',
         vi.delete_programme, name="delete_programme"),

    # ============================== Student option ==============================================
    path('student/dashboard', vi.student_dashboard, name='student_dashboard'),
    # ============================== HOD option ==================================================
    path('hod/dashboard', vi.hod_dashboard, name='hod_dashboard'),
    #     path('hod/add-student', vi.hod_add_student, name='hod_add_student'),
    path('student', vi.hod_students, name='hod_students'),
    # ============================== Dean Option =================================================
    path('dean/dashboard', vi.dean_dashboard, name='dean_dashboard'),
    # ============================== Registry option =============================================
    path('registry/dashboard', vi.registry_dashbaord, name='registry_dashboard'),
]
