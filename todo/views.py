from django.shortcuts import render, redirect
from todo.models import TodoList, Category, FinishedItems
from users.models import CustomUser
from .priority import PriorityChoicesField
from .forms import PriorityForm

from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@login_required(login_url='/team/login/')
@staff_member_required
def todo_view(request):
    todos = TodoList.objects.all()
    checked = FinishedItems.objects.all()
    categories = Category.objects.all()
    current_user = request.user
    priority_choices = PriorityForm()
    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            priority = request.POST["priority_select"]
            category = request.POST["category_select"]
            if request.POST["date"] != "":
                date = str(request.POST["date"])
            else:
                date = None
            try:
                content = request.POST["content"]
                if content:
                    Todo = TodoList(title=title,
                                    content=content,
                                    due_date=date,
                                    priority=priority,
                                    category=Category.objects.get(id=category),
                                    created_by_id=current_user.id,)
                else:
                    Todo = TodoList(title=title,
                                    due_date=date,
                                    priority=priority,
                                    category=Category.objects.get(id=category),
                                    created_by_id=current_user.id,)
            except MultiValueDictKeyError:
                Todo = TodoList(title=title,
                                due_date=date,
                                priority=priority,
                                category=Category.objects.get(id=category),
                                created_by_id=current_user.id,)
            Todo.save()
            return redirect('todo_view')
    if request.method == "GET":
        if "changeTask" in request.GET:
            task_id = request.GET['task_id']
            priority = request.GET['priority_select']
            date = request.GET['date']
            task = TodoList.objects.get(id=int(task_id))
            task.due_date = date
            if date == "":
                task.due_date = None
            task.priority = priority
            if request.GET['content']:
                content = request.GET['content']
                task.content = content
            task.save()
        try:
            task_id = int(request.GET['delete_task'])
            try:
                task = TodoList.objects.get(id=task_id)
                done = FinishedItems(title=task.title,
                            content=task.content,
                            due_date=task.due_date,
                            category=task.category,
                            priority=task.priority,
                            created_by_id=int(task.created_by.id),)
                done.save()
                task.delete()
            except FinishedItems.DoesNotExist:
                pass
        except MultiValueDictKeyError:
            pass
        try:
            priority_id = request.GET['priority_id']
            try:
                task = TodoList.objects.get(id=int(priority_id))
                if task.priority:
                    task.priority = False
                else:
                    task.priority = True
                task.save()
            except TodoList.DoesNotExist:
                pass
        except MultiValueDictKeyError:
            pass
        try:
            id = request.GET['undelete_task']
            try:
                #Save it into Finished Items before deleting#
                task = FinishedItems.objects.get(id=int(id))
                if task.created_by_id:
                    created_by = CustomUser.objects.get(id=task.created_by_id)
                    todo = TodoList(title=task.title,
                                content=task.content,
                                due_date=task.due_date,
                                category=task.category,
                                priority=task.priority,
                                created_by_id=created_by.id,)
                else:
                    todo = TodoList(title=task.title,
                                content=task.content,
                                due_date=task.due_date,
                                category=task.category)
                todo.save()
                task.delete()
            except FinishedItems.DoesNotExist:
                pass
        except MultiValueDictKeyError:
            pass
    return render(request,
        "todo/todo_list.html",
        {"todos": todos,
        "checked": checked,
        "priority_choices": priority_choices,
        "categories":categories})

@login_required(login_url='/team/login/')
def todo_categories_view(request):
    categories = Category.objects.all()
    if request.method == "POST":
        if "categoryAdd" in request.POST:
            category_name = request.POST["categoryName"]
            category = Category(name=category_name)
            category.save()
    if request.method == "GET":
        try:
            category_id = request.GET['delete_category']
            try:
                category = Category.objects.get(id=int(category_id))
                category.delete()
            except Category.DoesNotExist:
                pass
        except MultiValueDictKeyError:
            pass
    return render(request,
        "todo/todo_categories.html",
        {"categories":categories})
