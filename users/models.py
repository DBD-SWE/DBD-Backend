from django.db import models
import enum

class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField('Permission', related_name='types' )


    def __str__(self):
        return self.name
    @classmethod
    def get_default_pk(cls):
        type, created = cls.objects.get_or_create(
            name='user'
        )
        return type.pk

class CRUDOperations(enum.Enum):
    CREATE = 'C'
    READ = 'R'
    UPDATE = 'U'
    DELETE = 'D'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Permission(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(
        max_length=1,
        choices=CRUDOperations.choices(),
        help_text="Type of CRUD operation"
    )

    class Meta:
        unique_together = ('name', 'identifier')

    def __str__(self):
        return f"{self.name} - {CRUDOperations(self.identifier).name}"




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
