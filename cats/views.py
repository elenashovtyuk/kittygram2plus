from rest_framework import viewsets
# from rest_framework import permissions
from rest_framework.throttling import AnonRateThrottle

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    # для того, чтобы настроить права доступа на уровне представлений,
    # импортируем модуль permissions и
    # добавляем к вьюсету новый аттрибут с кортежем пермишенов(разрешений)
    # после этого получить список котиков может даже анонимнеый пользователь,
    # но внести какие-либо изменения анонимный польз-ль не может

    # после создания кастомного пермишн подключаем его  к нашему вьюсету
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (AnonRateThrottle,) # подключим класс для анонимных пользователей

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # во вьюсете CatViewSet переопределим метод get_permissions:
    # зададим условия, при которых должен применяться тот или иной пермишен:
    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию о конкретном объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # во всех остальных случаях вернем текущий перечень пермишенов
        #  без изменений
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
