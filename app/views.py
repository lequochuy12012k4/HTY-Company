from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count

def is_admin(user):
    return user.is_superuser

def is_manager(user):
    return hasattr(user, 'profile') and user.profile.is_manager

def HomePage(request):
    if not request.user.is_authenticated:
        return render(request, 'HomePage.html', {'documents': Paginator([ ], 12).get_page(1)})
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.user.is_superuser:
        documents_list = Document.objects.all().order_by('-created_at')
    elif profile and profile.department:
        documents_list = Document.objects.select_related('user', 'author', 'department').filter(department=profile.department).order_by('-created_at')
    else:
        documents_list = Document.objects.none()

    paginator = Paginator(documents_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'documents': page_obj
    }

    if request.user.is_superuser:
        context['document_count'] = Document.objects.count()
        context['user_count'] = User.objects.filter(is_superuser=False).count()
        context['manager_count'] = Profile.objects.filter(is_manager=True).count()

        department_data = []
        profiles = Profile.objects.select_related('user', 'department').filter(user__is_superuser=False).order_by('department__name', 'user__username')

        departments = {}
        for p in profiles:
            dept_name = p.department.name if p.department else "Không có phòng ban"
            if dept_name not in departments:
                departments[dept_name] = []
            departments[dept_name].append(p.user.username)

        context['department_data'] = [{'name': name, 'users': users} for name, users in departments.items()]

        context['user_document_counts'] = User.objects.filter(
            is_superuser=False 
        ).annotate(
            doc_count=Count('document') 
        ).values('username', 'doc_count').order_by('-doc_count')


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
            return redirect('home')
        
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
        messages.error(request, "Bạn không có quyền truy cập trang này.")
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
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect('/')
    
    manager_department = request.user.profile.department
    employee = get_object_or_404(User, id=employee_id)

    if employee.profile.department != manager_department:
        messages.error(request, "Bạn không có quyền chỉnh sửa nhân viên này.")
        return redirect('management')

    if request.method == 'POST':
        employee.profile.full_name = request.POST.get('full_name')
        team_id = request.POST.get('team')

        employee.profile.team = Team.objects.get(id=team_id) if team_id else None
        employee.profile.save()

        messages.success(request, f"Nhân viên {employee.username} đã được cập nhật thành công.")
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
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect('/')

    document = get_object_or_404(Document, id=document_id)
    
    if document.department != request.user.profile.department:
        messages.error(request, "Bạn không có quyền chỉnh sửa tài liệu này.")
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
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect('/')

    employee = get_object_or_404(User, id=employee_id)
    if employee.profile.department != request.user.profile.department:
        messages.error(request, "Bạn không có quyền xóa nhân viên này.")
        return redirect('management')
        
    employee.delete()
    messages.success(request, f"Nhân viên {employee.username} đã bị xóa.")
    return redirect('management')

@login_required
def delete_managed_document(request, document_id):
    if not (hasattr(request.user, 'profile') and request.user.profile.is_manager):
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect('/')

    document = get_object_or_404(Document, id=document_id)
    if document.department != request.user.profile.department:
        messages.error(request, "Bạn không có quyền xóa tài liệu này")
        return redirect('management')

    document.delete()
    messages.success(request, f"Tài liệu '{document.title}' đã được xóa.")
    return redirect('management')

@login_required
def ApprovalPage(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.is_manager)):
        messages.error(request, "Bạn không có quyền truy cập trang này.")
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
        messages.error(request, "Bạn không có quyền thực hiện hành động này.")
        return redirect('/')

    user_to_approve = get_object_or_404(User, id=user_id)
    
    if hasattr(request.user, 'profile') and request.user.profile.is_manager and not request.user.is_superuser:
        if user_to_approve.profile.department != request.user.profile.department:
            messages.error(request, "Bạn không có quyền phê duyệt nhân viên này.")
            return redirect('approval_page')

    user_to_approve.is_active = True
    user_to_approve.profile.is_approved = True
    user_to_approve.profile.status = 'approved'
    user_to_approve.save()
    user_to_approve.profile.save()

    messages.success(request, f"Nhân viên {user_to_approve.username} đã được duyệt")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def reject_user(request, user_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.is_manager)):
        messages.error(request, "Bạn không có quyền thực hiện hành động này.")
        return redirect('/')

    user_to_reject = get_object_or_404(User, id=user_id)

    if hasattr(request.user, 'profile') and request.user.profile.is_manager and not request.user.is_superuser:
        if user_to_reject.profile.department != request.user.profile.department:
            messages.error(request, "Bạn không có quyền từ chối nhân viên này.")
            return redirect('approval_page')

    user_to_reject.profile.status = 'rejected'
    user_to_reject.profile.save()
    user_to_reject.delete()

    messages.success(request, f"Nhân viên {user_to_reject.username} đã bị từ chối.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def Search(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)

    query = request.GET.get('q')
    if query:
        number_of_results = 6
        documents = Document.objects.filter(title__icontains=query).select_related('user', 'author')[:number_of_results]
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

@user_passes_test(is_admin)
def manage_departments(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        manager_id = request.POST.get('manager')
        if name:
            manager = None
            if manager_id:
                manager = User.objects.get(id=manager_id)
            Department.objects.create(name=name, manager=manager)
            messages.success(request, 'Thêm phòng ban thành công.')
        return redirect('manage_departments')
    
    departments = Department.objects.all()
    users = User.objects.filter(is_superuser=False, profile__status='approved')
    
    document_count = Document.objects.count()
    user_count = User.objects.filter(is_superuser=False).count()
    manager_count = User.objects.filter(profile__is_manager=True).count()

    context = {
        'departments': departments,
        'users': users,
        'document_count': document_count,
        'user_count': user_count,
        'manager_count': manager_count,
    }
    return render(request, 'ManageDepartmentsPage.html', context)

@user_passes_test(is_admin)
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    old_manager = department.manager

    if request.method == 'POST':
        name = request.POST.get('name')
        manager_id = request.POST.get('manager')
        
        department.name = name
        new_manager = None
        if manager_id:
            new_manager = User.objects.get(id=manager_id)
        department.manager = new_manager
        department.save()
        
        if old_manager and old_manager != new_manager:
            if not Department.objects.filter(manager=old_manager).exists():
                old_manager.profile.is_manager = False
                old_manager.profile.save()

        if new_manager:
            new_manager.profile.is_manager = True
            new_manager.profile.save()

        messages.success(request, 'Cập nhật phòng ban thành công.')
        return redirect('manage_departments')
    
    users = User.objects.filter(is_superuser=False, profile__status='approved')
    context = {
        'department': department,
        'users': users
    }
    return render(request, 'EditDepartmentPage.html', context)

@user_passes_test(is_admin)
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    messages.success(request, 'Xóa phòng ban thành công.')
    return redirect('manage_departments')

@user_passes_test(is_admin)
def manage_teams(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        if name and department_id:
            Team.objects.create(name=name, department_id=department_id)
            messages.success(request, 'Thêm ban thành công.')
        return redirect('manage_teams')
    
    teams = Team.objects.all()
    departments = Department.objects.all()
    context = {
        'teams': teams,
        'departments': departments,
    }
    return render(request, 'ManageTeamsPage.html', context)

@user_passes_test(is_admin)
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        
        team.name = name
        team.department_id = department_id
        team.save()
        
        messages.success(request, 'Cập nhật ban thành công.')
        return redirect('manage_teams')
    
    departments = Department.objects.all()
    context = {
        'team': team,
        'departments': departments
    }
    return render(request, 'EditTeamPage.html', context)

@user_passes_test(is_admin)
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    messages.success(request, 'Xóa ban thành công.')
    return redirect('manage_teams')

@user_passes_test(is_admin)
def manage_users(request):
    users = Profile.objects.filter(status='approved')
    context = {'users': users}
    return render(request, 'ManageUsersPage.html', context)

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        department_id = request.POST.get('department')
        team_id = request.POST.get('team')
        
        user.profile.full_name = full_name
        user.profile.department_id = department_id
        user.profile.team_id = team_id
        user.profile.save()
        
        messages.success(request, 'Cập nhật người dùng thành công.')
        return redirect('manage_users')
    
    departments = Department.objects.all()
    teams = Team.objects.all()
    context = {
        'user': user,
        'departments': departments,
        'teams': teams,
        'is_admin': True
    }
    return render(request, 'EditUserPage.html', context)

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'Xóa người dùng thành công.')
    return redirect('manage_users')
