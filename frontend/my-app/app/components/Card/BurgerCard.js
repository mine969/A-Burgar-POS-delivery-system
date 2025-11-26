import Image from 'next/image'

export default function BurgerCard({ name, price, image }) {
  return (
    <div className="bg-[#FFF1E4] rounded-3xl p-4 flex flex-col items-center shadow-lg border-2 border-[#8D0202] transform hover:scale-105 transition-transform duration-300">
      <div className="relative w-40 h-40 mb-4">
        <Image 
          src={image} 
          alt={name} 
          fill 
          className="object-contain"
        />
      </div>
      <h3 className="text-[#BD0000] text-3xl font-bold mb-2 text-center leading-none">{name}</h3>
      <p className="text-[#4A3F35] text-2xl font-bold mb-4">${price}</p>
      <button className="bg-[#BD0000] text-[#FFF1E4] px-6 py-2 rounded-full text-xl hover:bg-[#8D0202] transition-colors shadow-md">
        Add to Cart
      </button>
    </div>
  )
}
