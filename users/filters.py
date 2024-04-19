from django.db.models import Q
from rest_framework import filters

from django.db.models import Exists, OuterRef

from users.models import BannedUser, InvitedUser

class DynamicSearchFilter(filters.BaseFilterBackend):
    """
    An advanced dynamic filter that allows filtering by any model field including related fields
    and custom method fields such as 'banned'.
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        query = Q()
 
        for key, value in query_params.items():

            add_filters = {'banned': BannedUser, 'invited': InvitedUser}
            if key in add_filters:
                is_true = value.lower() == 'true'
                if is_true:
                    queryset = queryset.filter(Exists(add_filters[key].objects.filter(user=OuterRef('pk'))))
                else:
                    queryset = queryset.exclude(Exists(add_filters[key].objects.filter(user=OuterRef('pk'))))
            else:
                keys = key.split('__')
                # Check for nested model fields
                if len(keys) > 1 and hasattr(queryset.model, keys[0]):
                    related_model = getattr(queryset.model, keys[0]).field.related_model
                    if hasattr(related_model, keys[1]):
                        query |= Q(**{f"{key}__icontains": value})
                elif hasattr(queryset.model, key):
                    query |= Q(**{f"{key}__icontains": value})

        return queryset.filter(query) if query else queryset
