from django.contrib import admin
from .models import Task, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Columnas para la tabla de categorías
    list_display = ('name', 'description', 'created_at')
    # Buscador por nombre de categoría
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # 1. Columnas que se mostrarán en el listado de tareas del panel
    list_display = ('title', 'status', 'category', 'user', 'due_date', 'created_at')
    
    # 2. FILTRAR POR ESTADO (Aquí cumplimos la práctica: usa tu campo 'status')
    # También agregamos filtro por categoría y fecha límite para darles más herramientas
    list_filter = ('status', 'category', 'due_date')
    
    # 3. Buscador por texto (busca en el título de la tarea o descripción)
    search_fields = ('title', 'description')
    
    # 4. Permitir cambiar el estado de la tarea directamente desde la lista, sin entrar al detalle
    list_editable = ('status',)
    
    # 5. Optimización de consultas para evitar el problema de N+1 queries al cargar relaciones
    # Al igual que Include() en Entity Framework, select_related hace un JOIN en SQL
    list_select_related = ('category', 'user')
