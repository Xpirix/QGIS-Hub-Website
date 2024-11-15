from api.views import ResourceAPIDownload, ResourceAPIList
from django.urls import path
from django.urls import re_path as url
from api.views import (
    UserTokenDetailView,
    UserTokenListView,
    user_token_create,
    user_token_update,
    user_token_delete,
    ResourceCreateView,
    ResourceDetailView,
)
urlpatterns = [
    path("resources/", ResourceAPIList.as_view(), name="resource-list"),
    path(
        "resource/<uuid:uuid>/", ResourceAPIDownload.as_view(), name="resource-download"
    ),
    path(
        "resource/create", ResourceCreateView.as_view(), name="resource-create"
    ),
    path(
        "resource/<str:resource_type>/<uuid:uuid>/", ResourceDetailView.as_view(), name="resource-detail"
    ),
    url(
        r"^tokens/$",
        UserTokenListView.as_view(),
        name="user_token_list",
    ),
    url(
        r"^tokens/(?P<pk>\d+)/$",
        UserTokenDetailView.as_view(),
        name="user_token_detail",
    ),
    url(
        r"^tokens/create/$",
        user_token_create,
        {},
        name="user_token_create",
    ),
    url(
        r"^tokens/(?P<token_id>\d+)/update$",
        user_token_update,
        {},
        name="user_token_update",
    ),
    url(
        r"^tokens/(?P<token_id>[^\/]+)/delete/$",
        user_token_delete,
        {},
        name="user_token_delete",
    ),

]
