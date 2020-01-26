from django.shortcuts import render, redirect
from todo.models import TodoList, Category, FinishedItems
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def todo_view(request):
    todos = TodoList.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save()
            return redirect('todo_view')
        if "taskDelete" in request.POST:
            try:
                checkedlist = request.POST["checkedbox"]
                for todo_id in checkedlist:
                    todo = TodoList.objects.get(id=int(todo_id))
                    #Save it into Finished Items before deleting#
                    done = FinishedItems(title=todo.title,
                            content=todo.content,
                            due_date=todo.due_date,
                            category_id=todo.category.id)
                    done.save()
            except MultiValueDictKeyError:
                pass
    return render(request, "todo/todo_list.html", {"todos": todos, "categories":categories})
