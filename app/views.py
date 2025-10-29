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
  if not request.user.is_authenticated:
        return render(request, 'HomePage.html', {'documents': Paginator([ ], 12).get_page(1)})

  try:
      profile = request.user.profile
  except Profile.DoesNotExist:
      profile = None

  if profile and profile.department:
      documents_list = Document.objects.select_related('user', 'author', 'department').filter(department=profile.department)
  else:
      documents_list = Document.objects.none()

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

def AuthorDetailPage(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    documents_list = author.documents.select_related('user').all()
    paginator = Paginator(documents_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'documents': page_obj
    }
    return render(request, 'AuthorDetailPage.html', context)

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Tên người dùng hoặc mật khẩu không đúng.')
            return redirect('login')

        if not user.check_password(password):
            messages.error(request, 'Tên người dùng hoặc mật khẩu không đúng.')
            return redirect('login')

        if not user.is_superuser:
            if not hasattr(user, 'profile') or not user.profile.is_approved:
                if user.profile.status == 'pending':
                    messages.error(request, 'Tài khoản của bạn đang chờ phê duyệt.')
                elif user.profile.status == 'rejected':
                    messages.error(request, 'Tài khoản của bạn đã bị từ chối.')
                else:
                    messages.error(request, 'Tài khoản của bạn chưa được phê duyệt.')
                return redirect('login')

        if not user.is_active:
            messages.error(request, 'Tài khoản của bạn không hoạt động.')
            return redirect('login')

        login(request, user)
        
        if user.is_superuser:
            return redirect('/admin')
        
        if hasattr(user, 'profile') and user.profile.is_manager:
            messages.success(request, f'Chào mừng quản lý, {user.username}!')
            return redirect('management')
        
        messages.success(request, f'Chào mừng, {user.username}!')
        return redirect('/')

    return render(request, 'authentication/Login.html')

def RegisterPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    full_name = request.POST.get('full_name')
    department_id = request.POST.get('department')
    team_id = request.POST.get('team')

    if User.objects.filter(username=username).exists():
      messages.error(request, 'Tên người dùng đã tồn tại')
      return redirect('register')
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_active = False
    user.save()
    
    department = Department.objects.get(id=department_id) if department_id else None
    team = Team.objects.get(id=team_id) if team_id else None
    
    Profile.objects.create(user=user, full_name=full_name, department=department, team=team, status='pending')

    messages.success(request, 'Tài khoản đã được tạo thành công. Vui lòng đợi quản trị viên phê duyệt.')
    return redirect('login')
  
  departments = Department.objects.all()
  teams = Team.objects.all()
  context = {
      'departments': departments,
      'teams': teams
  }
  return render(request, 'authentication/Register.html', context)

def get_teams(request):
    department_id = request.GET.get('department_id')
    teams = Team.objects.filter(department_id=department_id).order_by('name')
    return JsonResponse(list(teams.values('id', 'name')), safe=False)

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
        messages.success(request, format_html('<a href="{}">Nhấn cái này để đặt lại mật khẩu</a>', reset_link, reset_link))
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
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Tên người dùng đã tồn tại')
                return redirect('profile')
            user.username = new_username

        if new_password:
            if not user.check_password(old_password):
                messages.error(request, 'Mật khẩu cũ không đúng.')
                return redirect('profile')

            if new_password != confirm_password:
                messages.error(request, 'Mật khẩu mới không khớp.')
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
        document = request.FILES.get('file')

        if image and image.size > 3 * 1024 * 1024:
            return JsonResponse({'status': 'error', 'message': 'Kích thước ảnh không được vượt quá 3MB.'})

        if document and document.size > 5 * 1024 * 1024:
            return JsonResponse({'status': 'error', 'message': 'Kích thước tệp không được vượt quá 5MB.'})

        if title and author_name and description and image and document:
            author_instance, created = Author.objects.get_or_create(name=author_name)
            
            Document.objects.create(
                user=request.user,
                title=title,
                author=author_instance,
                description=description,
                image=image,
                document=document,
                department=request.user.profile.department
            )
            return JsonResponse({'status': 'success', 'message': f'Tài liệu "{title}" đã được tải lên thành công!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Tài liệu không hợp lệ. Vui lòng kiểm tra lại.'})
            
    else:
        documents_list = Document.objects.filter(user=request.user)
        paginator = Paginator(documents_list, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'documents': page_obj
        }
        return render(request, 'Navbar/UploadPage.html', context)

@login_required(login_url='login')
def ToggleFavorite(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        if request.user in document.favorited_by.all():
            document.favorited_by.remove(request.user)
            messages.success(request, f'Đã xóa "{document.title}" khỏi danh sách yêu thích.')
        else:
            document.favorited_by.add(request.user)
            messages.success(request, f'Đã thêm "{document.title}" vào danh sách yêu thích.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
def FavoritePage(request):
    favorite_documents_list = request.user.favorite_documents.select_related('user').all()
    paginator = Paginator(favorite_documents_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'documents': page_obj
    }
    return render(request, 'Navbar/FavoritePage.html', context)

@login_required(login_url='login')
def EditDocumentsPage(request):
    documents_list = Document.objects.filter(user=request.user)
    paginator = Paginator(documents_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'documents': page_obj
    }
    return render(request, 'Navbar/EditDocumentsPage.html', context)

@login_required(login_url='login')
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    if request.method == 'POST':
        document.title = request.POST.get('title')
        author_name = request.POST.get('author')
        document.description = request.POST.get('description')
        
        author, _ = Author.objects.get_or_create(name=author_name)
        document.author = author

        if 'image' in request.FILES:
            image = request.FILES['image']
            if image.size > 3 * 1024 * 1024:
                messages.error(request, 'Kích thước ảnh không được vượt quá 3MB.')
                return redirect('edit_document', document_id=document.id)
            document.image = image

        if 'document' in request.FILES:
            document_file = request.FILES['document']
            if document_file.size > 5 * 1024 * 1024:
                messages.error(request, 'Kích thước tệp không được vượt quá 5MB.')
                return redirect('edit_document', document_id=document.id)
            document.document = document_file
            
        document.save()
        messages.success(request, 'Tài liệu đã được cập nhật thành công.')
        return redirect('edit_documents')
    else:
        context = {
            'document': document
        }
        return render(request, 'Navbar/EditDocumentPage.html', context)

@login_required(login_url='login')
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    document.delete()
    messages.success(request, 'Tài liệu đã được xóa thành công.')
    return redirect('edit_documents')

@login_required
def ManagementPage(request):
    if not (hasattr(request.user, 'profile') and request.user.profile.is_manager):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('/')

    try:
        department = request.user.profile.department
        if not department:
            raise Department.DoesNotExist
    except (Profile.DoesNotExist, Department.DoesNotExist):
        messages.error(request, "Bạn không phải là người quản lý của bất kỳ phòng ban nào.")
        return redirect('/')

    documents = Document.objects.filter(department=department)
    employees = User.objects.filter(profile__department=department, profile__status='approved')
    pending_users = Profile.objects.filter(status='pending', department=department).select_related('user', 'department', 'team')

    context = {
        'department': department,
        'documents': documents,
        'employees': employees,
        'pending_users': pending_users,
    }
    return render(request, 'ManagementPage.html', context)

@login_required
def manage_employee(request, employee_id):
    if not (hasattr(request.user, 'profile') and request.user.profile.is_manager):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('/')
    
    manager_department = request.user.profile.department
    employee = get_object_or_404(User, id=employee_id)

    if employee.profile.department != manager_department:
        messages.error(request, "You do not have permission to edit this employee.")
        return redirect('management')

    if request.method == 'POST':
        employee.profile.full_name = request.POST.get('full_name')
        team_id = request.POST.get('team')

        employee.profile.team = Team.objects.get(id=team_id) if team_id else None
        employee.profile.save()

        messages.success(request, f"Employee {employee.username} has been updated.")
        return redirect('management')

    teams = Team.objects.filter(department=manager_department)
        
    context = {
        'employee': employee,
        'teams': teams
    }
    return render(request, 'ManageEmployeePage.html', context)

@login_required
def manage_document(request, document_id):
    if not (hasattr(request.user, 'profile') and request.user.profile.is_manager):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('/')

    document = get_object_or_404(Document, id=document_id)
    
    if document.department != request.user.profile.department:
        messages.error(request, "You do not have permission to edit this document.")
        return redirect('management')

    if request.method == 'POST':
        document.title = request.POST.get('title')
        author_name = request.POST.get('author')
        document.description = request.POST.get('description')
        
        author, _ = Author.objects.get_or_create(name=author_name)
        document.author = author

        if 'image' in request.FILES:
            document.image = request.FILES['image']

        if 'document' in request.FILES:
            document.document = request.FILES['document']
            
        document.save()
        messages.success(request, 'Tài liệu đã được cập nhật thành công.')
        return redirect('management')

    context = {
        'document': document
    }
    return render(request, 'ManageDocumentPage.html', context)

@login_required
def delete_employee(request, employee_id):
    if not (hasattr(request.user, 'profile') and request.user.profile.is_manager):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('/')

    employee = get_object_or_404(User, id=employee_id)
    if employee.profile.department != request.user.profile.department:
        messages.error(request, "You do not have permission to delete this employee.")
        return redirect('management')
        
    employee.delete()
    messages.success(request, f"Employee {employee.username} has been deleted.")
    return redirect('management')

@login_required
def delete_managed_document(request, document_id):
    if not (hasattr(request.user, 'profile') and request.user.profile.is_manager):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('/')

    document = get_object_or_404(Document, id=document_id)
    if document.department != request.user.profile.department:
        messages.error(request, "You do not have permission to delete this document.")
        return redirect('management')

    document.delete()
    messages.success(request, f"Document '{document.title}' has been deleted.")
    return redirect('management')

@login_required
def ApprovalPage(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.is_manager)):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('/')

    if request.user.is_superuser:
        pending_users = Profile.objects.filter(status='pending').select_related('user', 'department', 'team')
    else:
        manager_department = request.user.profile.department
        pending_users = Profile.objects.filter(status='pending', department=manager_department).select_related('user', 'department', 'team')

    context = {
        'pending_users': pending_users
    }
    return render(request, 'ApprovalPage.html', context)

@login_required
def approve_user(request, user_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.is_manager)):
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('/')

    user_to_approve = get_object_or_404(User, id=user_id)
    
    if hasattr(request.user, 'profile') and request.user.profile.is_manager and not request.user.is_superuser:
        if user_to_approve.profile.department != request.user.profile.department:
            messages.error(request, "You do not have permission to approve this user.")
            return redirect('approval_page')

    user_to_approve.is_active = True
    user_to_approve.profile.is_approved = True
    user_to_approve.profile.status = 'approved'
    user_to_approve.save()
    user_to_approve.profile.save()

    messages.success(request, f"User {user_to_approve.username} has been approved.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def reject_user(request, user_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.is_manager)):
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('/')

    user_to_reject = get_object_or_404(User, id=user_id)

    if hasattr(request.user, 'profile') and request.user.profile.is_manager and not request.user.is_superuser:
        if user_to_reject.profile.department != request.user.profile.department:
            messages.error(request, "You do not have permission to reject this user.")
            return redirect('approval_page')

    user_to_reject.profile.status = 'rejected'
    user_to_reject.profile.save()

    messages.success(request, f"User {user_to_reject.username} has been rejected.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def Search(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)

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

def SecretPage(request):
  return render(request, 'secret/15102518.html')
