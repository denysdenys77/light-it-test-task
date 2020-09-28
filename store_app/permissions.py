from rest_framework.permissions import BasePermission


# group names
CASHIER = 'Cashier'
CONSULTANT = 'Consultant'
ACCOUNTANT = 'Accountant'


class OrderCreate(BasePermission):
    """
    Permission class to give Cashier opportunity
    to create new Order instance.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.groups.filter(name=CASHIER).exists()
        return True


class OrderFilter(BasePermission):
    """
    Differentiation of access of viewing orders
    objects rights by filter parameter:

    - status=1 -- CONSULTANT
    - status=2 -- CASHIER
    - start_date or/and finish_date -- ACCOUNTANT
    """

    def has_permission(self, request, view):
        if request.method == 'GET':

            permission_per_status = {
                "1": request.user.groups.filter(name=CONSULTANT).exists(),
                "2": request.user.groups.filter(name=CASHIER).exists()
            }

            order_status = request.query_params.get('status')
            start_date = request.query_params.get('start_date')
            finish_date = request.query_params.get('finish_date')

            if order_status:
                return permission_per_status.get(order_status, False)
            elif start_date or finish_date:
                return request.user.groups.filter(name=ACCOUNTANT).exists()
        return True


class OrderChangeStatus(BasePermission):
    """
    Differentiation of access of changing order
    status rights by  parameter:
    - status=2 -- CONSULTANT
    - status=3 -- CASHIER
    """

    def has_permission(self, request, view):

        permission_per_status = {
            "2": request.user.groups.filter(name=CONSULTANT).exists(),
            "3": request.user.groups.filter(name=CASHIER).exists()
        }

        if request.method == 'PATCH':
            new_status = request.data.get('status')
            if new_status:
                return permission_per_status.get(new_status, False)
        return True


class GetBill(BasePermission):
    """
    Permission class to give Cashier opportunity
    get Bill for existing Order instance.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.groups.filter(name=CASHIER).exists()
        return True
