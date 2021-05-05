from django.core.exceptions import PermissionDenied

class UserIsOwnerOrAdminMixin():
    '''
    Выполняем проверку. Будет возвращено True в случае,
     если USER_ID обьекта совпадает с пользователем,
     залогинившимся в систему. Это означает, что это его владелец,
      либо это администратор user.is_staff.
    '''

    def has_permission(self):
        return self.get_object().user == self.request.user or self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise PermissionDenied  # Выбрасываем ошибку 403.
        return super().dispatch(request, *args, **kwargs)
