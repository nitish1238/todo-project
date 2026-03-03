from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Todo

def todo_list(request):
    if request.method == 'POST':
        # Handle different actions
        action = request.POST.get('action')
        
        if action == 'create':
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            priority = request.POST.get('priority', 'medium')
            
            if title:
                Todo.objects.create(
                    title=title,
                    description=description,
                    priority=priority
                )
                messages.success(request, 'Todo created successfully!')
            else:
                messages.error(request, 'Title is required!')
                
        elif action == 'update':
            todo_id = request.POST.get('todo_id')
            todo = get_object_or_404(Todo, id=todo_id)
            
            todo.title = request.POST.get('title')
            todo.description = request.POST.get('description', '')
            todo.priority = request.POST.get('priority', 'medium')
            todo.save()
            messages.success(request, 'Todo updated successfully!')
            
        elif action == 'toggle':
            todo_id = request.POST.get('todo_id')
            todo = get_object_or_404(Todo, id=todo_id)
            todo.completed = not todo.completed
            todo.save()
            status = "completed" if todo.completed else "pending"
            messages.success(request, f'Todo marked as {status}!')
            
        elif action == 'delete':
            todo_id = request.POST.get('todo_id')
            todo = get_object_or_404(Todo, id=todo_id)
            todo.delete()
            messages.success(request, 'Todo deleted successfully!')
            
        return redirect('todo_list')
    
    # GET request - display todos
    filter_status = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')
    
    todos = Todo.objects.all()
    
    if filter_status == 'completed':
        todos = todos.filter(completed=True)
    elif filter_status == 'pending':
        todos = todos.filter(completed=False)
    
    if search_query:
        todos = todos.filter(title__icontains=search_query)
    
    # Get a single todo for editing if specified
    edit_id = request.GET.get('edit')
    edit_todo = None
    if edit_id:
        try:
            edit_todo = Todo.objects.get(id=edit_id)
        except Todo.DoesNotExist:
            pass
    
    context = {
        'todos': todos,
        'filter_status': filter_status,
        'search_query': search_query,
        'edit_todo': edit_todo,
    }
    return render(request, 'todo/index.html', context)