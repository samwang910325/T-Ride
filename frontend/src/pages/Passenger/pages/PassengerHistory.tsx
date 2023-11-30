import React from 'react'
import { useNavigate } from "react-router-dom";

export default function PassengerHistory() {

    const navigate = useNavigate();

    return (
        <div>
            <div className="bg-white">
                <div className="p-4">
                    <h2 className="text-lg font-bold">Upcoming Trips</h2>
                </div>
                <div className="space-y-4 p-4">
                    <button className=' w-full'
                        type="button"
                        onClick={() => {
                            navigate("/passenger/Tripinfo")
                        }}>
                        <div className="bg-cover bg-center h-[120px] rounded-lg" style={{ backgroundImage: `url('path_to_image.jpg')` }}>
                            <div className="p-4 flex justify-between items-end h-full bg-gradient-to-t from-black to-transparent rounded-lg">
                                <div>
                                    <h3 className="text-white font-bold">Los Angeles trip</h3>
                                    <p className="text-gray-300">3 days away</p>
                                </div>
                                <p className="text-white">Feb 16</p>
                            </div>
                        </div>
                    </button>
                </div>
            </div>
            <div className="bg-white">
                <div className="p-4">
                    <h2 className="text-lg font-bold">Past Orders</h2>
                </div>
                <div className="space-y-4 p-4">
                    <button className=' w-full'
                        type="button"
                        onClick={() => {
                            navigate("/passenger/Tripinfo")
                        }}>
                        <div className="bg-cover bg-center h-[120px] rounded-lg" style={{ backgroundImage: `url('path_to_image.jpg')` }}>
                            <div className="p-4 flex justify-between items-end h-full bg-gradient-to-t from-black to-transparent rounded-lg">
                                <div>
                                    <h3 className="text-white font-bold">Los Angeles trip</h3>
                                    <p className="text-gray-300">3 days away</p>
                                </div>
                                <p className="text-white">Jan 21</p>
                            </div>
                        </div>
                    </button>
                </div>
            </div>
        </div >
    )
}
