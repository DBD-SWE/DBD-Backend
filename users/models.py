from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField('Permission', related_name='types' )

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
    
    


# class TypePermission(models.Model):
#     type = models.ForeignKey(Type, on_delete=models.CASCADE)
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('type', 'permission')

#     def __str__(self):
#         return f"{self.type.name} - {self.permission.name}"
