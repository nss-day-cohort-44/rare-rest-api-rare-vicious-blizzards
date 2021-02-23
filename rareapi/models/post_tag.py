from django.db import models

class PostTag(models.Model):
    post = models.ForeignKey("Post", related_name="tags", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", related_name="tags", on_delete=models.CASCADE)