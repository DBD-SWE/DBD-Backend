from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField('Permission', related_name='types' )
    
    ''' 
    
    suggestion to add description field as at is important to know what the type is about:
        description = models.CharField(max_length=255, blank=True)
        
    '''

    def __str__(self):
        return self.name
    @classmethod
    def get_default_pk(cls):
        type, created = cls.objects.get_or_create(
            name='user'
        )
        return type.pk
class Permission(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.identifier
