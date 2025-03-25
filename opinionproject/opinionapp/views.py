from django.shortcuts import render , redirect
from opinionapp.models import Opinion
from opinionapp.models import user
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def home(request):
    opinion = Opinion.objects.all()
    return render(request, 'index.html', {'opinion': opinion})

def opinion(request):    # For New Post
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        image = request.FILES.get('image')  # Corrected syntax
        opinion = Opinion(title=title, message=message, image=image)
        opinion.save()
    return render(request, 'post.html')

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