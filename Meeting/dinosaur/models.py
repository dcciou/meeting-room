from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


#會議室
class ConfeRoom(models.Model):
    num = models.CharField(max_length=5)
    size = models.CharField(max_length=5)
    open_time = models.DateTimeField(default=timezone.now) 
    close_time = models.DateTimeField(default=timezone.now)
    
    class Meta:  # 正确的 Meta 类定义
        ordering = ["num"]
    
    def __str__(self):
        return self.num


#訂單資料
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ConfeRoom, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title
