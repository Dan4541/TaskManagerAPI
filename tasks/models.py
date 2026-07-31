from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):    
    name = models.CharField(max_length=100, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        # El método __str__ es el equivalente al método ToString() en C#
        return self.name


class Task(models.Model):

    # Definición de enumerados para el estado
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        IN_PROGRESS = 'IN_PROGRESS', 'En Progreso'
        COMPLETED = 'COMPLETED', 'Completada'

    title = models.CharField(max_length=200, verbose_name="Títle")
    description = models.TextField(verbose_name="Description")
    
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="status"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    due_date = models.DateTimeField(blank=True, null=True, verbose_name="Due Date")
    
    # RELACIONES (Foreign Keys)
    # models.PROTECT evita que se borre una categoría si tiene tareas asociadas
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='tasks',
        verbose_name="Category"
    )
    
    # models.CASCADE borra las tareas del usuario si el usuario es eliminado del sistema
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name="User Creator"
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-due_date', 'created_at'] # Ordena por fecha límite descendente

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})" # type: ignore