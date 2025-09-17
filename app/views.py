from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.utils.html import format_html

def HomePage(request):
  documents_list = Document.objects.select_related('user', 'author').all()
  paginator = Paginator(documents_list, 12)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'documents': page_obj
  }
  return render(request, 'HomePage.html', context)

def DocumentDetailPage(request, document_id):
    document = get_object_or_404(Document.objects.select_related('user', 'author'), id=document_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = request.user.favorite_documents.filter(id=document_id).exists()
    context = {
        'document': document,
        'is_favorite': is_favorite
    }
    return render(request, 'DocumentDetailPage.html', context)

# View mới cho trang chi tiết tác giả
def AuthorDetailPage(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    # Sử dụng related_name 'documents' để lấy tất cả tài liệu của tác giả
    documents = author.documents.select_related('user').all()
    context = {
        'author': author,
        'documents': documents
    }
    return render(request, 'AuthorDetailPage.html', context)

def LoginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, f'Chào mừng, {user.username}!')
      return redirect('/')
    else:
      messages.error(request, 'Tên người dùng hoặc mật khẩu không đúng.')
      return redirect('login')
  return render(request, 'authentication/Login.html')

def RegisterPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if User.objects.filter(username=username).exists():
      messages.error(request, 'Tên người dùng đã tồn tại')
      return redirect('register')
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    messages.success(request, 'Tài khoản đã được tạo thành công. Bạn có thể đăng nhập ngay bây giờ.')
    if user is not None:
      login(request, user)
      messages.success(request, f'Chào mừng, {user.username}!')
    return redirect('login')
  return render(request, 'authentication/Register.html')

def LogoutUser(request):
  logout(request)
  return redirect('login')

def ForgotPasswordPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email người dùng này không tồn tại')
            return redirect('forgot-password')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(reverse('reset-password', kwargs={'uidb64': uid, 'token': token}))

        messages.success(request, format_html('Liên kết đặt lại mật khẩu của bạn: <a href="{}">{}</a>', reset_link, reset_link))
        return redirect('forgot-password')

    return render(request, 'authentication/ForgotPassword.html')

def ResetPasswordPage(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                messages.error(request, "Mật khẩu không khớp.")
                return redirect(request.path)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Mật khẩu đã được đặt lại thành công. Bạn có thể đăng nhập ngay bây giờ.")
            return redirect('login')
        return render(request, 'authentication/ResetPassword.html')
    else:
        messages.error(request, "Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.")
        return redirect('forgot-password')

@login_required(login_url='login')
def ProfilePage(request):
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Tên người dùng đã tồn tại')
                return redirect('profile')
            user.username = new_username

        if new_password:
            if new_password != confirm_password:
                messages.error(request, 'Mật khẩu không khớp')
                return redirect('profile')
            user.set_password(new_password)

        user.save()
        login(request, user)
        messages.success(request, 'Hồ sơ đã được cập nhật thành công!')
        return redirect('profile')
    return render(request, 'Navbar/ProfilePage.html')

@login_required(login_url='login')
def UploadPage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        file = request.FILES.get('file')
        if title and author_name and description and image and file:
            author_instance, created = Author.objects.get_or_create(name=author_name)
            
            Document.objects.create(
                user=request.user,
                title=title,
                author=author_instance,
                description=description,
                image=image,
                document=file
            )
            messages.success(request, 'Tài liệu đã được tải lên thành công!')
            return redirect('upload')
        else:
            messages.error(request, 'Tài liệu không hợp lệ. Vui lòng kiểm tra lại.')
            return redirect('upload')
    return render(request, 'Navbar/UploadPage.html')

@login_required(login_url='login')
def ToggleFavorite(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        if request.user in document.favorited_by.all():
            document.favorited_by.remove(request.user)
            messages.success(request, 'Đã xóa khỏi danh sách yêu thích.')
        else:
            document.favorited_by.add(request.user)
            messages.success(request, 'Đã thêm vào danh sách yêu thích.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
def FavoritePage(request):
    favorite_documents = request.user.favorite_documents.select_related('user').all()
    context = {
        'documents': favorite_documents
    }
    return render(request, 'Navbar/FavoritePage.html', context)

def Search(request):
    query = request.GET.get('q')
    if query:
        documents = Document.objects.filter(title__icontains=query).select_related('user', 'author')
    else:
        documents = Document.objects.select_related('user', 'author').all()
    
    data = []
    for document in documents:
        data.append({
            'id': document.id,
            'title': document.title,
            'author_name': document.author.name if document.author else '',
            'author_id': document.author.id if document.author else None,
            'description': document.description,
            'image_url': document.image.url,
            'document_url': document.document.url,
            'username': document.user.username,
            'is_favorite': request.user in document.favorited_by.all() if request.user.is_authenticated else False
        })
    
    return JsonResponse(data, safe=False)
