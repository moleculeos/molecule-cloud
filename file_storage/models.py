from django.db import models
from django.contrib.auth.models import User


class Directory(models.Model):
    root = models.BooleanField(default=False)
    parent = models.ForeignKey("Directory", on_delete=models.CASCADE, related_name="child", null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=255)
    shared_to = models.ManyToManyField(User, related_name="shared_folders_to_me")

    @property
    def public_to(self):
        tested_dir = self
        while tested_dir.shared_to.count() == 0 and not self.root:
            tested_dir = tested_dir.parent
        return tested_dir.shared_to


class File(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="files")
    filetype = models.CharField(max_length=50)
    last_edit = models.DateTimeField(auto_now=True)
    shared_to = models.ManyToManyField(User, related_name="shared_files_to_me")
    file = models.FileField(upload_to='user_data')

    @property
    def public_to(self):
        if self.shared_to.count() == 0:
            return self.directory.public_to
        else:
            return self.shared_to
