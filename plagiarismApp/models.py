from django.db import models


""" class CustomManager(models.Manager):
    def delete(self):
        for obj in self.get_queryset():
            obj.delete()
 """
class File(models.Model):
    filepath = models.FileField(upload_to='files/', null=True, verbose_name="")
    Name = models.CharField(max_length=200)
    # objects = CustomManager()

    """ def delete(self, using=None, keep_parents=False):
        self.filepath.storage.delete(self.filepath.name)
        super().delete()
 """
    def __str__(self):
        return "MY_File_Upload"





