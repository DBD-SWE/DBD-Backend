from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from users.models import Permission  
from django.urls import URLPattern, URLResolver, get_resolver

class Command(BaseCommand):
    help = 'Populate the permissions table with all possible permissions.'

    def handle(self, *args, **kwargs):
        # Define the CRUD operations
        crud_operations = ['C', 'R', 'U', 'D']

        # Get the URL resolver
        resolver = get_resolver()

        # Get all URL patterns
        urls = get_urls(resolver)

        # Iterate over all URL patterns
        for url in urls:
            for operation in crud_operations:
                permission, created = Permission.objects.get_or_create(name=url, identifier=operation)
                if created:
                    self.stdout.write(f'Created permission for {url} with operation {operation}')

        self.stdout.write(self.style.SUCCESS('Successfully populated permissions.'))

def get_urls(resolver, base_path=''):
    url_patterns = []
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            # Recursively fetch patterns from included URLconf
            next_level = f"{base_path}{pattern.pattern.regex.pattern}" if hasattr(pattern.pattern, 'regex') else f"{base_path}{pattern.pattern._route}"
            url_patterns.extend(get_urls(pattern, base_path=next_level))
        elif isinstance(pattern, URLPattern):
            # Handle different types of patterns
            if hasattr(pattern.pattern, 'regex'):
                full_pattern = f"{base_path}{pattern.pattern.regex.pattern}"
                # Remove regex characters and the end of string regex symbol
                full_pattern = full_pattern.replace('^', '').replace('$', '').replace('\\Z', '')
                # Skip patterns with parameters
                if '<' not in full_pattern and '>' not in full_pattern and full_pattern.split('/').__len__() > 2:
                    url_patterns.append(full_pattern)
            else:
                # Standard route patterns, remove the end of string symbol
                full_pattern = f"{base_path}{pattern.pattern._route}".replace('\\Z', '')
                if full_pattern.split('/').__len__() > 2:
                    url_patterns.append(full_pattern)
    return url_patterns
