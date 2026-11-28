"""URL configuration: respondent portal at /, administrator screens at /manage/, Django admin at /admin/."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.accounts import views as account_views
from apps.events import views as event_views
from apps.portal import roster_views
from apps.portal.views import home

admin.site.site_header = "CNAP Member Hub: database administration"
admin.site.site_title = "CNAP Member Hub"
admin.site.index_title = "Administration"

from apps.common import prototype as ui_prototype  # noqa: E402


def healthz(request):
    """The host's health check (Render): plain HTTP, no sign-in, no database work."""
    from django.http import HttpResponse

    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path("calendar/<str:key>.ics", event_views.calendar_feed, name="calendar_feed"),
    path("calendar/inbound/<str:key>/", event_views.calendar_inbound, name="calendar_inbound"),
    path("ui-preview/<str:view>/", ui_prototype.switch, name="ui_switch"),
    path("admin/login/", account_views.admin_login),
    path("admin/", admin.site.urls),
    path("roster-check/<str:token>/", roster_views.roster_check, name="roster_check"),
    path("accounts/login/", account_views.LoginView.as_view(), name="login"),
    path("accounts/link/", account_views.link_request, name="link_request"),
    path("accounts/request-access/", account_views.request_access, name="request_access"),
    path("accounts/link/<str:token>/", account_views.link_login, name="link_login"),
    path("accounts/code/", account_views.link_code, name="link_code"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password/",
        auth_views.PasswordChangeView.as_view(success_url="/accounts/password/done/"),
        name="password_change",
    ),
    path(
        "accounts/password/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "site-photo/",
        __import__("apps.common.feedback", fromlist=["site_photo"]).site_photo,
        name="site_photo",
    ),
    path(
        "feedback/",
        __import__("apps.common.feedback", fromlist=["send"]).send,
        name="page_feedback",
    ),
    path("manage/", include("apps.admin_center.urls")),
    path("", include("apps.portal.urls")),
    path("", home, name="home"),
]
