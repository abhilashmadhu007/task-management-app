from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import User
from task.models import Task  
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.role in ["Admin", "SuperAdmin"]:  # only admins can log in
            login(request, user)
            return redirect("dashboard")
        return render(request, "adminpanel/login.html", {"error": "Invalid credentials"})
    return render(request, "adminpanel/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    if request.user.role == "SuperAdmin":
        return render(request, "adminpanel/superadmin_dashboard.html")
    elif request.user.role == "Admin":
        return render(request, "adminpanel/admin_dashboard.html")
    return redirect("login")

# SUPERADMIN: Manage Users
@login_required
def manage_users(request):
    if request.user.role != "SuperAdmin":
        return redirect("dashboard")

    users = User.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            role = request.POST.get("role", "User")
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            user.save()
            messages.success(request, f"User {username} created successfully.")
        elif action == "delete":
            user_id = request.POST.get("user_id")
            User.objects.filter(id=user_id).delete()
            messages.success(request, "User deleted successfully.")
        elif action == "assign_role":
            user_id = request.POST.get("user_id")
            role = request.POST.get("role")
            user = User.objects.get(id=user_id)
            user.role = role
            user.save()
            messages.success(request, f"Role updated to {role}.")
        elif action == "assign_admin":
            user_id = request.POST.get("user_id")
            admin_id = request.POST.get("admin_id")
            user = User.objects.get(id=user_id)
            admin = User.objects.get(id=admin_id)
            if admin.role == "Admin":
                user.assigned_admin = admin
                user.save()
                messages.success(request, f"User {user.username} assigned to {admin.username}.")
            else:
                messages.error(request, "Selected user is not an Admin.")

    admins = User.objects.filter(role="Admin")
    return render(request, "adminpanel/manage_users.html", {"users": users, "admins": admins})

# SUPERADMIN: Manage Admins
@login_required
def manage_admins(request):
    if request.user.role != "SuperAdmin":
        return redirect("dashboard")

    admins = User.objects.filter(role="Admin")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            admin = User(username=username, email=email, role="Admin")
            admin.set_password(password)
            admin.save()
            messages.success(request, f"Admin {username} created successfully.")
        elif action == "delete":
            admin_id = request.POST.get("admin_id")
            User.objects.filter(id=admin_id, role="Admin").delete()
            messages.success(request, "Admin deleted successfully.")

    return render(request, "adminpanel/manage_admins.html", {"admins": admins})

# SUPERADMIN: Manage Tasks
@login_required
def manage_tasks(request):
    if request.user.role != "SuperAdmin":
        return redirect("dashboard")

    tasks = Task.objects.all()
    return render(request, "adminpanel/manage_tasks.html", {"tasks": tasks})

# SUPERADMIN: Task Reports
@login_required
def task_reports(request):
    if request.user.role != "SuperAdmin":
        return redirect("dashboard")

    tasks = Task.objects.filter(status="Completed")
    return render(request, "adminpanel/task_reports.html", {"tasks": tasks})

@login_required
def admin_dashboard(request):
    if request.user.role != "Admin":
        return redirect("dashboard")

    users_qs = User.objects.filter(assigned_admin=request.user)
    tasks_qs = Task.objects.filter(assigned_to__assigned_admin=request.user)

    context = {
        "users_count": users_qs.count(),
        "tasks_count": tasks_qs.count(),
        "pending_count": tasks_qs.filter(status="Pending").count(),
        "in_progress_count": tasks_qs.filter(status="In Progress").count(),
        "completed_count": tasks_qs.filter(status="Completed").count(),
    }
    return render(request, "adminpanel/admin_dashboard.html", context)


# Admin: List / Create / Delete users (Users under this Admin)
@login_required
def user_list(request):
    if request.user.role != "Admin":
        return redirect("dashboard")

    users = User.objects.filter(assigned_admin=request.user)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if not username or not password:
                messages.error(request, "Username and password are required.")
            else:
                u = User(username=username, email=email, role="User", assigned_admin=request.user)
                u.set_password(password)
                u.save()
                messages.success(request, f"User {username} created and assigned to you.")
            return redirect("user_list")

        elif action == "delete":
            user_id = request.POST.get("user_id")
            # only delete if user belongs to this admin
            User.objects.filter(id=user_id, assigned_admin=request.user).delete()
            messages.success(request, "User deleted successfully.")
            return redirect("user_list")

    return render(request, "adminpanel/user_list.html", {"users": users})


# Admin: List tasks and create new tasks for admin's users
@login_required
def task_list(request):
    if request.user.role != "Admin":
        return redirect("dashboard")

    tasks = Task.objects.filter(assigned_to__assigned_admin=request.user).order_by("-due_date")
    users = User.objects.filter(assigned_admin=request.user)

    if request.method == "POST":
        # Creating a new task (assign to one of this admin's users)
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        assigned_to_id = request.POST.get("assigned_to")

        if not title or not assigned_to_id:
            messages.error(request, "Title and Assigned User are required.")
            return redirect("task_list")

        assigned_to = get_object_or_404(User, id=assigned_to_id, assigned_admin=request.user)

        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date if due_date else None,
            status="Pending"
        )
        messages.success(request, f"Task '{task.title}' created and assigned to {assigned_to.username}.")
        return redirect("task_list")

    return render(request, "adminpanel/task_list.html", {"tasks": tasks, "users": users})


# Admin: Edit task (only tasks assigned to this admin's users)
@login_required
def edit_task(request, task_id):
    if request.user.role != "Admin":
        return redirect("dashboard")

    task = get_object_or_404(Task, id=task_id, assigned_to__assigned_admin=request.user)
    users = User.objects.filter(assigned_admin=request.user)

    if request.method == "POST":
        task.title = request.POST.get("title", task.title)
        task.description = request.POST.get("description", task.description)
        due_date = request.POST.get("due_date")
        task.due_date = due_date if due_date else None

        # Reassign only to users under this admin
        assigned_to_id = request.POST.get("assigned_to")
        if assigned_to_id:
            assigned_to = get_object_or_404(User, id=assigned_to_id, assigned_admin=request.user)
            task.assigned_to = assigned_to

        # Admin may change progress but should NOT set completion_report/worked_hours.
        status = request.POST.get("status")
        # allow only Pending / In Progress to be set by Admin (Users should mark Completed)
        if status in ["Pending", "In Progress"]:
            task.status = status
        task.save()
        messages.success(request, "Task updated successfully.")
        return redirect("task_list")

    return render(request, "adminpanel/edit_task.html", {"task": task, "users": users})


# Admin: Delete task (only for tasks within admin scope)
@login_required
def delete_task(request, task_id):
    if request.user.role != "Admin":
        return redirect("dashboard")

    task = get_object_or_404(Task, id=task_id, assigned_to__assigned_admin=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect("task_list")

    # optional: confirmation page
    return render(request, "adminpanel/confirm_delete.html", {"object": task})


# Admin: View a completed task report (only tasks assigned to this admin's users and status=Completed)
@login_required
def view_task_report(request, task_id):
    if request.user.role != "Admin":
        return redirect("dashboard")

    task = get_object_or_404(Task, id=task_id, assigned_to__assigned_admin=request.user, status="Completed")
    # task.completion_report and task.worked_hours expected on Task model
    return render(request, "adminpanel/view_task_report.html", {"task": task})

