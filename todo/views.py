from django.shortcuts import render, redirect
from todo.models import TodoList, Category, FinishedItems
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/team/login/')
def todo_view(request):
    todos = TodoList.objects.all()
    checked = FinishedItems.objects.all()
    categories = Category.objects.all()
    current_user = request.user
    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category
            print(current_user)
            Todo = TodoList(title=title,
                            content=content,
                            due_date=date,
                            category=Category.objects.get(id=category),
                            created_by_id=current_user.id,)
            Todo.save()
            return redirect('todo_view')
        if "taskDelete" in request.POST:
            try:
                checkedlist = request.POST.getlist("checkedbox")
                try:
                    for todo_id in checkedlist:
                        todo_task = TodoList.objects.get(id=int(todo_id))
                        category = todo_task.category
                        #Save it into Finished Items before deleting#
                        done = FinishedItems(title=todo_task.title,
                                content=todo_task.content,
                                due_date=todo_task.due_date,
                                category=category,
                                created_by=str(todo_task.created_by),
                                done_user=current_user,)
                        done.save()
                except MultiValueDictKeyError:
                    pass
            except MultiValueDictKeyError:
                pass
    if request.method == "GET":
        try:
            task_id = request.GET['priority_id']
            try:
                task = FinishedItems.objects.get(id=int(task_id))
                todo = TodoList(title=task.title,
                            content=task.content,
                            due_date=task.due_date,
                            category=task.category,
                            created_by=task.created_by,)
                todo.save()
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
                todo = TodoList(title=task.title,
                            content=task.content,
                            due_date=task.due_date,
                            category=task.category,
                            created_by=task.created_by,)
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
        "categories":categories})
