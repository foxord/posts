from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts
from .forms import PostsForm  # Убедитесь, что форма называется PostsForm


def post_list(request):
    # Получаем все посты, сортируя от новых к старым
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})


def post_create(request):
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Перенаправление на список постов
    else:
        form = PostsForm()
    return render(request, 'posts/post_form.html', {'form': form, 'post': None})


def post_update(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if request.method == 'POST':
        form = PostsForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostsForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'post': post})


def post_delete(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


def ping(request):
    return JsonResponse({'status': 'ok'})
