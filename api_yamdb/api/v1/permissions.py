from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSuperUser(BasePermission):
    """Проверка прав администратора."""
    message = 'Нужны права администратора'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):
    message = 'К сожалению, вы не авторизованы на данный запрос'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdmin(BasePermission):
    message = 'К сожалению, вы не авторизованы на данный запрос'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            and request.user.is_authenticated
        )


class IsModeratorOrReadOnly(BasePermission):
    message = 'К сожалению, вы не авторизованы на данный запрос'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            and request.user.is_authenticated
        )


class IsAuthorOrReadOnly (BasePermission):
    message = 'К сожалению, вы не авторизованы на данный запрос'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            and request.user.is_authenticated
        )


class IsAuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin)
