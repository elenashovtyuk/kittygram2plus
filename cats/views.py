from rest_framework import viewsets
from rest_framework import permissions

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    # для того, чтобы настроить права доступа на уровне представлений,
    # импортируем модуль permissions и
    # добавляем к вьюсету новый аттрибут с кортежем пермишенов(разрешений)
    # после этого получить список котиков может даже анонимнеый пользователь,
    # но внести какие-либо изменения анонимный польз-ль не может
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
