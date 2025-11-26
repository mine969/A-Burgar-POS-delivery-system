import React from 'react'
import Navbar from '../navbar/nav'
import BurgerCard from '../Card/BurgerCard'


export default function OrderPage() {
  return (
    <div className="min-h-screen bg-[#FFECDC] flex flex-col font-bangers">
        <div className="bg-img"> 

      <Navbar />
      <div className=" text-[#BD0000]">
        <h1 className="text-6xl mt-10 px-6 md:px-32 ">Choose Your Meal</h1>
        <BurgerCard name="Classic Burger" price={10.99} image="https://via.placeholder.com/150" />       
      </div>
        </div>
    </div>
  )
}
