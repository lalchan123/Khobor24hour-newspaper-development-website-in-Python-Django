
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import math
from PIL import Image


# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


class SportPost(models.Model):
    sport_title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='sport_posts')
    updated_on = models.DateTimeField(auto_now= True)
    image = models.ImageField(default='/static/images/postdefault.jpg', upload_to='images/')
    sport_content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    visit_sport = models.PositiveIntegerField(default=0)
    
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.sport_title

    def save(self, *args, **kwargs):
        super(SportPost, self).save(*args, **kwargs)
        imag = Image.open(self.image.path)
        if imag.width > 300 or imag.height> 300:
            output_size = (300, 300)
            imag.thumbnail(output_size)
            imag.save(self.image.path)  

    

    @property
    def comment_count(self):
        return SportComment.objects.filter(sportpost=self).count()






class SportComment(models.Model):
    sportpost = models.ForeignKey(SportPost, on_delete= models.CASCADE, related_name='sport_comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete= models.CASCADE, null=True, blank=True, related_name='replies_sport_comment')

    
    class Meta:
        # sort comments in chronological order by default
        ordering = ('created',)

    def __str__(self):
        return self.name
