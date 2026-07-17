# tasks/serializers import
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer auxiliar para renderizar los datos de la categoría en modo lectura."""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class UserSerializer(serializers.ModelSerializer):
    """Serializer auxiliar para renderizar los datos del usuario creador en modo lectura."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para entregar información detallada en el GET (JSON anidado)
    category_detail = CategorySerializer(source='category', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    
    # Campo de solo lectura para exponer la traducción amigable del enum (ej: "Pendiente" en lugar de "PENDING")
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # Campos de escritura obligatorios que aceptan el ID plano (Primary Key)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = [
            'id', 
            'title', 
            'description', 
            'status', 
            'status_display', 
            'created_at', 
            'due_date', 
            'category', 
            'category_detail', 
            'user', 
            'user_detail'
        ]
        # created_at se genera automáticamente mediante auto_now_add=True
        read_only_fields = ['id', 'created_at']

    def validate_status(self, value):
        """Validación personalizada opcional para el estado de la tarea."""
        # Django ya valida las opciones gracias a 'choices' en el modelo, 
        # pero aquí puedes agregar lógica extra si la requieres en el Serializer.
        if value not in Task.StatusChoices.values:
            raise serializers.ValidationError("El estado proporcionado no es válido.")
        return value