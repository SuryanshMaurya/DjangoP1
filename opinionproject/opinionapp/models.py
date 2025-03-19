from django.db import models

# Create your models here.
class Opinion(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    message = models.TextField()
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class reaction(models.Model):
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    opinion = models.ForeignKey(Opinion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.opinion.title
    
class user(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# Opinion
#   ├── Reaction (Comment 1)
#   │     ├── Reaction (Reply to Comment 1)
#   │     │     └── Reaction (Reply to Reply to Comment 1)
#   │     └── Reaction (Another Reply to Comment 1)
#   └── Reaction (Comment 2)
#         └── Reaction (Reply to Comment 2)