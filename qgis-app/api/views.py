from django.contrib.postgres.search import SearchVector
from api.permissions import IsHasAccessOrReadOnly
from rest_framework import filters, permissions
from rest_framework.response import Response
from drf_multiple_model.views import FlatMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination

from geopackages.models import Geopackage
from models.models import Model
from styles.models import Style

from api.serializers import (GeopackageSerializer,
                             ModelSerializer,
                             StyleSerializer)


def filter_resource_type(queryset, request, *args, **kwargs):
    resource_type = request.query_params['resource_type']
    if queryset.model.__name__.lower() == resource_type.lower():
        return queryset
    else:
        return queryset.none()


def filter_resource_subtype(queryset, request, *args, **kwargs):
    resource_subtype = request.query_params['resource_subtype']
    if queryset.model.__name__ == 'Style':
        return queryset.filter(style_type__name__iexact=resource_subtype)
    else:
        return queryset.none()


def filter_creator(queryset, request, *args, **kwargs):
    creator = request.query_params['creator']
    qs = queryset.annotate(
        search=(SearchVector('creator__username')
                + SearchVector('creator__first_name')
                + SearchVector('creator__last_name'))
        ).filter(search=creator)
    return qs


def filter_keyword(queryset, request, *args, **kwargs):
    keyword = request.query_params['keyword']
    qs = queryset.annotate(
        search=(
                SearchVector('name') + SearchVector('description'))
        ).filter(search=keyword)
    return qs


def filter_general(queryset, request, *args, **kwargs):
    resource_type = request.query_params.get('resource_type', None)
    resource_subtype = request.query_params.get('resource_subtype', None)
    creator = request.query_params.get('creator', None)
    keyword = request.query_params.get('keyword', None)
    if resource_type:
        queryset = filter_resource_type(queryset, request, *args, **kwargs)
    if resource_subtype:
        queryset = filter_resource_subtype(queryset, request, *args, **kwargs)
    if creator:
        queryset = filter_creator(queryset, request, *args, **kwargs)
    if keyword:
        queryset = filter_keyword(queryset, request, *args, **kwargs)
    return queryset


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 10


class ResourceAPIList(FlatMultipleModelAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitPagination

    filter_backends = (filters.SearchFilter, )
    search_field = ('name', 'creator')

    querylist = [
        {
            'queryset': Geopackage.approved_objects.all(),
            'serializer_class': GeopackageSerializer,
            'label': 'geopackage',
            'filter_fn': filter_general
        },
        {
            'queryset': Model.approved_objects.all(),
            'serializer_class': ModelSerializer,
            'label': 'model',
            'filter_fn': filter_general
        },
        {
            'queryset': Style.approved_objects.all(),
            'serializer_class': StyleSerializer,
            'label': 'model',
            'filter_fn': filter_general
        },
    ]








# class ResourceAPIDetail(generics.RetrieveUpdateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsHasAccessOrReadOnly]
#     http_method_names = ['get', 'put']
#
#     def get_queryset(self):
#         """Return detail """
#         qs = self.model.approved_objects.all()
#         return qs
#
#     def perform_update(self, serializer):
#         serializer.save(approved=False, require_action=False)

#
# class ReasourceAPIDownload(generics.ListAPIView):
#     def get(self, request, pk, format=None):
#         object = self.model.approved_objects.get(id=pk)
#         object.increase_download_counter()
#         object.save()
#         # zip the resource and license.txt
#         zipfile = zipped_with_license(object.file.file.name, object.name)
#
#         response = HttpResponse(
#             zipfile.getvalue(), content_type="application/x-zip-compressed")
#         response['Content-Disposition'] = 'attachment; filename=%s.zip' % (
#             slugify(object.name, allow_unicode=True)
#         )
#         return response