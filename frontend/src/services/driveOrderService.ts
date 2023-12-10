import { get, post } from './APIHelper';
import { driverOrderDTO, driverInvitationDTO, driverInvitationTotalDTO, orderDTO } from '../DTO/orders';
import { userDTO } from '../DTO/user';
import { convertUTC } from './formatService';
import { getUserId } from '../utils/userUtil';

interface PostDriverOrderRequest {
  token: string;
  startPoint: {
    lat: number;
    lng: number;
  }
  startName: string;
  endPoint: {
    lat: number;
    lng: number;
  }
  endName: string;
  departureTime: number;
  passengerCount: number;
}

const postDriverOrder = async (params: PostDriverOrderRequest) => {
  try {
    const response = await post(
      "/order/driver",
      JSON.stringify(params),
      {
        headers: {
          "Content-Type": "application/json"
        }
      }
    );
    console.log("postDriverOrder response: ", response);
    return response;
  } catch (error) {
    console.log("postDriverOrder error: ", error);
  }
}

const getDriverUnfinishedOrder = async () => {
  const userId = getUserId();
  try {
    const response: any = await get(`/order/driver/unfinished/${userId}`);
    console.log("getDriverUnfinishedOrder response: ", response);
    return response;
  } catch (error) {
    console.log("getDriverUnfinishedOrder error: ", error);
  }
}

const getStartEnd = async (orderId: number) => {
  try {
    const response: {data: driverOrderDTO} = await get(`/order/driver/${orderId}`) as {data: driverOrderDTO};
    const startEnd = [
      { name: response.data.startName, 
        time: convertUTC(response.data.departureTime),
        place: {
          lat: response.data.startPoint.lat,
          lng: response.data.startPoint.lng
        } 
      },
      { name: response.data.endName, 
        time: "",
        place: {
          lat: response.data.endPoint.lat,
          lng: response.data.startPoint.lng
        }
      }
    ];
    return startEnd;
  } catch (error) {
    console.log(`startEnd: ${error}`);
  }
}

const getUserName = async (userId: number) => {
  try {
    const response: { data: userDTO } = await get(`/user/${userId}`) as { data: userDTO };
    return response.data.userName;
  } catch (error) {
    console.log(error);
    return "none";
  }
}

const getInvitationTotal = async (orderId: number) => {
  try {
    const response: {data: driverInvitationTotalDTO} = await get(`/match/driver/invitation/total/${orderId}`) as { data: driverInvitationTotalDTO };
    const acceptedOrders = await Promise.all(response.data.invitations
      .map(async (order) => {
        const name: string = await getUserName(order.passengerOrder.userId);
        return {
          userId: order.passengerOrder.userId,
          userName: name,
          startName: order.passengerOrder.startName,
          endName: order.passengerOrder.endName,
          pickTime: convertUTC(order.passengerOrder.departureTime1),
          arriveTime: convertUTC(order.passengerOrder.arrivalTime),
          state: order.accepted,
          startPlace: {
            lat: order.passengerOrder.startPoint.lat,
            lng: order.passengerOrder.startPoint.lng
          },
          endPlace: {
            lat: order.passengerOrder.endPoint.lat,
            lng: order.passengerOrder.endPoint.lng
          },
          fee: order.passengerOrder.fee,
          passengerCount: order.passengerOrder.passengerCount
        };
      }));
    return acceptedOrders;
  } catch (error) {
    console.log(error);
  }
}

export { postDriverOrder, getStartEnd, getInvitationTotal, getDriverUnfinishedOrder };
