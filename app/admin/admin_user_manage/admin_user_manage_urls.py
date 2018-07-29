from django.urls import path

from app.admin.admin_user_manage import admin_user_manage_api

urlpatterns = [
    # path('',admin_user_manage_api.admin_user_manage),
    path('userList/',admin_user_manage_api.user_list),
    path('userAddPage/',admin_user_manage_api.user_add_page),
    path('userAdd/',admin_user_manage_api.user_add),
    path('lookUser/', admin_user_manage_api.look_user),
    path('EditUserPsd/', admin_user_manage_api.edit_user_psd),
    path('deleteUser/', admin_user_manage_api.delete_user),

]