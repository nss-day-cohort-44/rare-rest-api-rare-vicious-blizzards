from django.db import models

class DemotionQueue(models.Model):
    action = models.CharField(max_length=200)
    admin = models.ForeignKey("RareUser", related_name="admin", on_delete=models.CASCADE)
    approver_one = models.ForeignKey("RareUser", related_name="approver", on_delete=models.CASCADE)