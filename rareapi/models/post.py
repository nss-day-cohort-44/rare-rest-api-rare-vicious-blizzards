from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)
    post_image = models.ImageField(upload_to="profile_pics", max_length=None, width_field=None, height_field=None)
    content = models.CharField(max_length=5000)
    approved = models.BooleanField(default=None)
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
 