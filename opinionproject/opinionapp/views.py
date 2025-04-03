from django.shortcuts import render , redirect
from django.http import JsonResponse
from opinionapp.models import Opinion, reaction
from django.db.models import Sum
import json
from opinionapp.models import user
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def home(request):
    opinions = Opinion.objects.all()
    for opinion in opinions:
        opinion.total_likes = reaction.objects.filter(opinion=opinion).aggregate(Sum('likes'))['likes__sum'] or 0
        opinion.total_comments = reaction.objects.filter(opinion=opinion).count()
        opinion.comments = reaction.objects.filter(opinion=opinion, parent__isnull=True).prefetch_related('replies')
    return render(request, 'index.html', {'opinions': opinions})

def opinion(request):    # For New Post
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        image = request.FILES.get('image')  # Corrected syntax
        opinion = Opinion(title=title, message=message, image=image)
        opinion.save()
    return render(request, 'post.html')

def like_opinion(request, opinion_id):
    if request.method == 'POST':
        opinion = Opinion.objects.get(id=opinion_id)
        reaction_obj, created = reaction.objects.get_or_create(opinion=opinion, parent=None)  # Ensure parent=None for top-level reactions
        reaction_obj.likes += 1
        reaction_obj.save()
        return JsonResponse({'likes': reaction_obj.likes})

def comment_opinion(request, opinion_id):
    if request.method == 'POST':
        opinion = Opinion.objects.get(id=opinion_id)
        data = json.loads(request.body)
        comment_text = data.get('comment')
        reaction_obj = reaction.objects.create(opinion=opinion, comments=comment_text)
        return JsonResponse({'comment': reaction_obj.comments, 'id': reaction_obj.id})

def reply_comment(request, comment_id):
    if request.method == 'POST':
        parent_comment = reaction.objects.get(id=comment_id)
        data = json.loads(request.body)
        reply_text = data.get('reply')
        reply = reaction.objects.create(
            opinion=parent_comment.opinion,
            comments=reply_text,
            parent=parent_comment
        )
        return JsonResponse({'reply': reply.comments})

def signup(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match!"})
        
        if user.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error": "Email already exists!"})
        
        new_user = user(name=name, email=email, password=make_password(password))
        new_user.save()
        return redirect("login")
    
    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user_obj = user.objects.get(email=email)
            if check_password(password, user_obj.password):
                request.session['user_id'] = user_obj.id  # Store user session
                return redirect("home")
            else:
                return render(request, "login.html", {"error": "Invalid password!"})
        except user.DoesNotExist:
            return render(request, "login.html", {"error": "User not found!"})
    
    return render(request, "login.html")