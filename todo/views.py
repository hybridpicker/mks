from django.shortcuts import render, redirect
from todo.models import TodoList, Category, FinishedItems
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def todo_view(request):
    todos = TodoList.objects.all()
    checked = FinishedItems.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(id=category))
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
                                category=category)
                        done.save()
                except MultiValueDictKeyError:
                    pass
            except MultiValueDictKeyError:
                pass
    if request.method == "GET":
        try:
            task_id = request.GET['id']
            task = FinishedItems.objects.get(id=int(task_id))
            todo = TodoList(title=task.title,
                        content=task.content,
                        due_date=task.due_date,
                        category=task.category)
            todo.save()
            task.delete()
        except MultiValueDictKeyError:
            pass
    return render(request,
        "todo/todo_list.html",
        {"todos": todos,
        "checked": checked,
        "categories":categories})
