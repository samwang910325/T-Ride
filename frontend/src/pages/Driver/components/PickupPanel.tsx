import { orderDTO } from "../../../DTO/orders";
import { useAppSelector } from "../../../hooks";
import { useState, useRef, useEffect } from "react";
import PickupCard from "./PickupCard";
import { getDriverUnfinishedOrder } from "../../../services/driveOrderService";
import ErrorLoading from "../../../components/ErrorLoading";

type LatLngLiteral = google.maps.LatLngLiteral;
type PickupPanelProps = {
  isLoaded: boolean;
  setPanel: (panel: number) => any;
  orders?: orderDTO[];
  markerOrderId: number | null;
  setShowSpots?: (showSpots: boolean) => void;
};

const PickupPanel = ({ isLoaded, setPanel, orders, markerOrderId, setShowSpots }: PickupPanelProps) => {
  const driverDepart = useAppSelector((state) => state.driverDepartReducer);
  // tempOrderReducer.orders: 紀錄使用者點擊確認後的訂單
  const tempOrderReducer = useAppSelector((state) => state.tempOrderReducer);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const cardContainerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (cardContainerRef.current) {
      document.getElementById(`pickupCard-${markerOrderId}`)?.scrollIntoView({ behavior: "smooth"});
    }
  }, [markerOrderId])

  const backBtnHandler = async() => {
    try{
      setLoading(true);
      const unfinishedOrder = await getDriverUnfinishedOrder();
      console.log(unfinishedOrder);
      if (unfinishedOrder.data.length > 0) {
        setPanel(1);
        alert("您有未完成的訂單");
        setLoading(false);
      }
      else{
        setPanel(0);
        setShowSpots && setShowSpots(false);
      }
    }catch(err){
      setError("發生錯誤");
      setPanel(1);
      setLoading(false);
    }
  }

  return <>
    {
      isLoaded && (
        <>
          <div className='flex flex-col items-center h-fit min-h-[40vh] bg-white rounded-t-3xl overflow-hidden z-50 '>
            <div className='flex items-center justify-evenly bg-white w-[100vw] mt-0'>
              <div className="mt-2">
                <p>
                  乘客人數 <span className='ml-1'>{tempOrderReducer.orders.length}</span> / <span>{driverDepart.passengerCount}</span> 人
                </p>
              </div>
              <div className="mt-2" >
                <p>
                  總金額<span className='ml-1'>0</span>元
                </p>
              </div>
            </div>

            <div 
              ref={cardContainerRef}
              className="flex flex-col h-[36vh] w-[100%] overflow-auto"
            >
              {
                orders && orders.map((order) => (
                  <PickupCard key={order.orderId} order={order} markerOrderId={markerOrderId} />
                ))
              }
            </div>

            <div className='fixed bottom-20 flex justify-center w-[100%]'>
              <button 
                className='rounded bg-[#f3e779] w-[25vw] h-10 text-xl mr-4' 
                onClick={backBtnHandler}
              >
                取消
              </button>

              <button 
                className='rounded bg-cyan-800 w-[60vw] h-10 text-white text-xl'
                onClick={() => {
                  setPanel(2);
                  setShowSpots && setShowSpots(false);
                }}
              >
                確認
              </button>
            </div>
          </div>
          <ErrorLoading error={error} setError={setError} loading={loading} setLoading={setLoading} /> 
        </>
      )
    }
  </>;
}

export default PickupPanel;