from django.db.models import Q, Exists, OuterRef
from rest_framework import filters

from users.models import BannedUser, InvitedUser

class DynamicSearchFilter(filters.BaseFilterBackend):
    """
    An advanced dynamic filter that allows filtering by any model field including related fields
    and custom method fields such as 'banned' and 'invited'.
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        query = Q()

        for key, value in query_params.items():
            print(f"Processing filter: {key}={value}")  # Debug statement
            add_filters = {'banned': BannedUser, 'invited': InvitedUser}
            if key in add_filters:
                is_true = value.lower() == 'true'
                filter_exists = Exists(add_filters[key].objects.filter(user=OuterRef('pk')))
                if is_true:
                    queryset = queryset.filter(filter_exists)
                else:
                    queryset = queryset.exclude(filter_exists)
            else:
                keys = key.split('__')
                if len(keys) > 1:  # Handling nested model fields
                    try:
                        related_field = queryset.model._meta.get_field(keys[0])
                        if related_field.is_relation:
                            related_model = related_field.related_model
                            if hasattr(related_model, keys[1]):
                                field_query = Q(**{f"{key}__icontains": value})
                                query &= field_query  # Changed to logical AND
                                print(f"Added to query: {field_query}")  # Debug statement
                    except Exception as e:
                        print(f"Error processing field {keys[0]}: {e}")  # Debug statement
                elif hasattr(queryset.model, key):
                    field_query = Q(**{f"{key}__icontains": value})
                    query &= field_query  # Changed to logical AND
                    print(f"Added to query: {field_query}")  # Debug statement

        filtered_queryset = queryset.filter(query) if query else queryset
        print(f"Final QuerySet: {filtered_queryset.query}")  # Debug statement to view the raw SQL query
        return filtered_queryset
