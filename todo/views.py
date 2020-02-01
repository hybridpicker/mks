from django.shortcuts import render, redirect
from todo.models import TodoList, Category, FinishedItems
from users.models import CustomUser
from .priority import PriorityChoicesField

from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/team/login/')
def todo_view(request):
    todos = TodoList.objects.all()
    checked = FinishedItems.objects.all()
    categories = Category.objects.all()
    current_user = request.user
    priority_choices = PriorityChoicesField
    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            if request.POST["date"] != "":
                date = str(request.POST["date"])
            else:
                date = None
            category = request.POST["category_select"]
            try:
                content = request.POST["content"]
                if content:
                    Todo = TodoList(title=title,
                                    content=content,
                                    due_date=date,
                                    category=Category.objects.get(id=category),
                                    created_by_id=current_user.id,)
            except MultiValueDictKeyError:
                Todo = TodoList(title=title,
                                due_date=date,
                                category=Category.objects.get(id=category),
                                created_by_id=current_user.id,)
            Todo.save()
            return redirect('todo_view')
    if request.method == "GET":
        if "changeTask" in request.GET:
            task_id = request.GET['task_id']
            task = TodoList.objects.get(id=int(task_id))
            if request.GET['content']:
                content = request.GET['content']
                task.content = content
            if request.GET['date']:
                date = request.GET['date']
                task.due_date = date
            task.save()
        try:
            task_id = int(request.GET['delete_task'])
            try:
                task = TodoList.objects.get(id=task_id)
                if task.created_by:
                    done = FinishedItems(title=task.title,
                                content=task.content,
                                due_date=task.due_date,
                                category=task.category,
                                created_by_id=int(task.created_by.id),)
                else:
                    done = FinishedItems(title=task.title,
                                content=task.content,
                                due_date=task.due_date,
                                category=task.category,)
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
            id = request.GET['undelete_id']
            try:
                #Save it into Finished Items before deleting#
                task = FinishedItems.objects.get(id=int(id))
                if task.created_by_id:
                    created_by = CustomUser.objects.get(id=task.created_by_id)
                    todo = TodoList(title=task.title,
                                content=task.content,
                                due_date=task.due_date,
                                category=task.category,
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
