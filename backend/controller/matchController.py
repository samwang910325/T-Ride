# TODO: token validation should be in service
from quart import Blueprint, request, make_response
from services.matchService import *
from services.userService import *
from services.orderService import *
from utils import utils
from controller.models import *


match = Blueprint('match_page', __name__)

match_service = MatchService()
user_service = UserService()
order_service = OrderService()


@match.route('/driver/invitation', methods=['POST'])
async def match_driver_invitation():
    body = await request.json
    if not utils.is_keys_in_dict(body, [
        "token",
        "driverOrderId",
        "passengerOrderId"]):
        return await make_response("Incorrect parameter format", 400)

    user_id = user_service.get_user_id(body["token"])
    if user_id is None:
        return await make_response("Invalid token", 401)

    ret = match_service.send_invitation(
        user_id,
        body["driverOrderId"],
        body["passengerOrderId"])

    if ret == "user not found":
        return await make_response("Invalid token", 401)
    if ret == "user incorrect":
        return await make_response("Not the driver's own order", 403)
    if ret == "driver order not found" or ret == "passenger order not found":
        return await make_response("Order not found", 404)
    if ret == "driver order is finished" or\
        ret == "passenger order is finished" or\
        ret == "already matched" or\
        ret == "already invited":
        return await make_response("Invitation already sent, accepted, or order completed", 409)

    return await make_response("Invitation sent successfully", 200)


@match.route('/driver/invitation/<int:driverOrderId>/<int:passengerOrderId>', methods=['DELETE'])
async def delete_driver_invitation(driverOrderId, passengerOrderId):
    token = request.args.get('token')

    # TODO: 實現邏輯，處理取消司機邀請的情況

    return jsonify({'message': 'NOT implemented'}), 200


@match.route('/driver/invitation/total/<int:driverOrderId>', methods=['GET'])
async def get_driver_total_invitations(driverOrderId):
    ret = match_service.get_driver_invitations(driverOrderId)

    if ret == 'order not found':
        return await make_response('Order not found', 404)

    # TODO: arrival time跟排序都在service就算好才丟出來
    return utils.to_json({'invitations': sorted([InvitationVo(invitation, order_service.get_estimated_arrival_time(
        invitation.order.start_point,
        invitation.order.end_point,
        invitation.order.departure_time1)) for invitation in ret], key=lambda invitation: invitation.passengerOrder.departureTime1)})


@match.route('/passenger/invitation/total/<int:passengerOrderId>', methods=['GET'])
async def get_passenger_total_invitations(passengerOrderId):
    ret = match_service.get_passenger_invitation_orders(passengerOrderId)

    if ret == 'order not found':
        return await make_response('Order not found', 404)

    return utils.to_json({'driverOrders': [DriverOrderVo(order) for order in ret]})


@match.route('/passenger/accepted/<int:passengerOrderId>', methods=['GET'])
async def get_passenger_accepted(passengerOrderId):
    ret = match_service.get_passenger_accepted_order(passengerOrderId)

    if ret == 'order not found':
        return await make_response('Order not found', 404)

    return utils.to_json({"driverOrder": ret})


@match.route('/passenger/invitation/accept', methods=['POST'])
async def accept_invitation():
    data = await request.get_json()
    # TODO: 實現邏輯，處理接受邀請的情況

    return jsonify({'message': 'NOT implemented'}), 200