from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=255);

    def __str__(self):
        return self.name;

class Permission(models.Model):
    name = models.CharField(max_length=255);
    identifier = models.CharField(max_length=255);

    def __str__(self):
        return self.name;

class User(models.Model):
    username = models.CharField(max_length=255);
    password = models.CharField(max_length=255);
    email = models.EmailField(max_length=255);
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='users');

    def __str__(self):
        return self.username;

class TypePermission(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE);
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE);

    class Meta:
        unique_together = ('type', 'permission');

    def __str__(self):
        return f"{self.type.name} - {self.permission.name}";
