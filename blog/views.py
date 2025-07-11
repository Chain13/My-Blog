from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm
import json


def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        form = CommentForm(request.POST)
        if form.is_valid():
            cmt = form.save(commit=False)
            cmt.post = post
            if request.user.is_authenticated:
                cmt.author = request.user
                cmt.name = request.user.username
            else:
                cmt.name = "Guest"
            cmt.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # ตรวจสอบว่า user เป็นเจ้าของบทความเท่านั้น
    if request.user != post.author:
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

            # ✅ แปลง tag JSON string กลับเป็น list
            tags_json = request.POST.get("tags", "[]")
            print(tags_json)
            # try:
            #     tags = json.loads(tags_json)
            # except json.JSONDecodeError:
            #     tags = []

            # ✅ บันทึกแท็กกลับเข้า post
            # post.tags.set(tags)  # <- เพิ่มบรรทัดนี้
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})


from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .models import Post

def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_profile).order_by('-published_date')
    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'posts': posts,
    })

from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            success = True
            # # ✅ ส่งอีเมล
            # send_mail(
            #     subject=f"📬 New Contact from {contact.name}",
            #     message=contact.message,
            #     from_email=contact.email,  # หรือ settings.DEFAULT_FROM_EMAIL
            #     recipient_list=[settings.CONTACT_RECEIVER_EMAIL],  # ระบุอีเมลที่จะรับ
            #     fail_silently=False,
            # )

            # return redirect('contact_thank_you')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'success': success})
