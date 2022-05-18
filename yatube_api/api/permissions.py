from rest_framework import permissions


class AuthorOrReadOnlyPermission(permissions.BasePermission):
    """
    Класс проверяет запрос и проводит его если запрос удовлетворяет условиям.
    Запрос пройдет если:
    запрос находится в 'SAFE_METHODS' (GET, GET_LIST)
    Пользователь авторизован (создание постов)
    Если запрос относится к конкретному объекту то он совершится только в этих
    трех случаях:
    1 - Пользователь является автором поста.
    2 - Пользователь является администратором.
    3 - Запрос не изменяет объект (только чтение).
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )
