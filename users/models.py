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

class BannedUser(models.Model):

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='banned_user')
    
    banned_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(default='')

    def __str__(self):
        return self.user.email
    

class InvitedUser(models.Model):
    user =  models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='invited_user')
    invited_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=32, unique=True)


    def __str__(self):
        return f'Invited - {self.user.email}'