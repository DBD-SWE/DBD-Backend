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

    def __str__(self):
        return f"{self.name} - {CRUDOperations(self.identifier).name}"


