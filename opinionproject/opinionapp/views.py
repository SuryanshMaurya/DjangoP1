from django.shortcuts import render
from opinionapp.models import Opinion

# Create your views here.
def home(request):
    return render(request, 'index.html')

def opinion(request):    # For New Post
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        image = request.FILES.get('image')  # Corrected syntax
        opinion = Opinion(title=title, message=message, image=image)
        opinion.save()
    return render(request, 'post.html')