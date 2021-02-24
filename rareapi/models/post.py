from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)
    post_image_url = models.CharField(max_length=200)
    content = models.CharField(max_length=5000)
    approved = models.BooleanField(default=None)
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    @property
    def is_current_user(self):
        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self, value):
        self.__is_current_user = value
 