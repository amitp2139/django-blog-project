from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from . models import blog
from . forms import edit_blog
# Create your views here.
def index(request):
    blogs=blog.objects.all()
    context={'blogs':blogs}
    return render(request,'home.html',context)
def about(request):
    return render(request,'about.html')
def user_register(request):
    if request.method=='POST':
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1!=pass2:
            messages.warning(request,'password does not match')
            return redirect('register')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request,'username already exits')
            return redirect('register') 
        elif User.objects.filter(email=email).exists():
            messages.warning(request,'email already exits')
            return redirect('register')
        else:
            user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pass1)
            user.save()
            messages.success(request,uname+'has been registered successfully')
            return redirect('login')
    return render(request,'register.html')
def user_login(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.warning(request,'invalid credantial')
            return redirect('login')

    return render(request,'login.html')
def user_logout(request):
    logout(request)
    return redirect('/')
def post_blog(request):

    if request.method=='POST':
        title=request.POST.get("title")
        desc=request.POST.get("description")
        blogs=blog(title=title,dsc=desc,user_id=request.user)
        blogs.save()
        messages.success(request,"post has been upload successfully")
        return redirect('post_blog')
    return render(request,'blog_post.html')
def blog_detail(request,id):
    blogs=blog.objects.get(id=id)
    context={'blog':blogs}
    return render(request,'blog_detail.html',context)  
def delete(request,id):
    blogs=blog.objects.get(id=id)
    blogs.delete()
    messages.success(request,"post has been deleted")
    return redirect('/')
def edit(request,id):
    blogs=blog.objects.get(id=id)
    edit_blogs=edit_blog(instance=blogs)
    if request.method=="POST":
        form=edit_blog(request.POST,instance=blogs)
        if form.is_valid():
            form.save()
            messages.success(request,'post has been updated successfully')
            return redirect("/")
    return render(request,"edit_blog.html",{'edit_blog':edit_blogs})