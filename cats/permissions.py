from rest_framework import permissions


# создаем свое кастомное разрешение и в нем
# переопределяем оба метода базового класса
class OwnerOrReadOnly(permissions.BasePermission):
    # Сначала в has_permission()
    # проверяется метод запроса и статус пользователя
    # если метод запроса безопасный или пользователь аутентифицирован,
    # то этот метод вернет  True
    # в этом методе доступа к объекту запроса нет
    def has_permission(self, request, view):
        return (
          request.method in permissions.SAFE_METHODS
          or request.user.is_authenticated
        )

    # если первый метод (has_permission) вернул True,
    #  то после получения объекта, вызываем второй метод
    # в него уже передается запрошенный объект и теперь в этом методе
    # можно проверить - совпадает ли  автор этого объекта
    # с пользователем из запроса
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
