from rest_framework.permissions import BasePermission


# ==========================================================
# Admin Permission
# ==========================================================

class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )



# ==========================================================
# Seller Permission
# ==========================================================

class IsSeller(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "SELLER"
        )



# ==========================================================
# Customer Permission
# ==========================================================

class IsCustomer(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "CUSTOMER"
        )