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
# CatViewSet работает с моделью Cat. Значит при проверке в методе
# has_object_permission в obj будет передан объект этой модели
# то есть, какой то конкретный котик.
# Так как в этой модели есть поле owner, то при проверке будет проведено сравнение
# - пользователя из запроса и содержимое этого поля
# теперь новый кастомный пермишн можно подключить к вьюсету CatViewSet
