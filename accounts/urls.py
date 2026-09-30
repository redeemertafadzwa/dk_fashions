from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("verify/", views.verify_view, name="verify"),
    path("verify/resend/", views.resend_code_view, name="resend_code"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("manage-users/", views.manage_users_view, name="manage_users"),
    path("manage-users/<int:user_id>/toggle-admin/", views.toggle_admin_view, name="toggle_admin"),
]
