from repository.orderRepository import *
from repository.matchRepository import *
from repository.userRepository import *
from services.models import *


class MatchService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.order_repository = OrderRepository()
        self.match_repository = MatchRepository()

    def send_invitation(self, driver_id, driver_order_id, passenger_order_id):
        '''
        return "user not found",
               "user incorrect",
               "driver order not found",
               "driver order is finished",
               "passenger order not found",
               "passenger order is finished",
               "already matched",
               "already invited"

        return None on success
        '''
        if self.user_repository.get_user(driver_id) is None:
            return "user not found"

        driver_order = self.order_repository.get_driver_order(driver_order_id)
        if driver_order is None:
            return "driver order not found"
        if driver_order.finished:
            return "driver order is finished"

        passenger_order = self.order_repository.get_passenger_order(passenger_order_id)
        if passenger_order is None:
            return "passenger order not found"
        if passenger_order.finished:
            return "passenger order is finished"

        if driver_id != driver_order.user_id:
            return "user incorrect"

        if passenger_order_id in [order.order_id for order in\
            self.order_repository.get_driver_related_orders(driver_order_id)]:
            return "already matched"
        if passenger_order_id in [order.order_id for order in\
            self.order_repository.get_invited_orders(driver_order_id)]:
            return "already invited"

        self.match_repository.send_invitation(driver_order.order_id, passenger_order.order_id)

    def get_driver_invitations(self, order_id):
        '''
        return "order not found"

        return list of invitations
        '''
        order = self.order_repository.get_driver_order(order_id)
        if order is None:
            return "order not found"

        invitations = self.match_repository.get_driver_invitations(order_id)

        return [InvitationDto(invitation) for invitation in invitations]

    def get_passenger_invitation_orders(self, order_id):
        '''
        return "order not found"

        return list of driver orders
        '''
        order = self.order_repository.get_passenger_order(order_id)
        if order is None:
            return "order not found"

        driver_orders = self.order_repository.get_passenger_invitation_orders(order_id)

        return [DriverOrderDto(order) for order in driver_orders]

    def get_passenger_accepted_order(self, order_id):
        '''
        return "order not found"

        return None if no driver order is accepted
        '''
        order = self.order_repository.get_passenger_order(order_id)
        if order is None:
            return "order not found"

        driver_order = self.order_repository.get_passenger_related_order(order_id)

        if driver_order is None:
            return None

        return DriverOrderDto(driver_order)