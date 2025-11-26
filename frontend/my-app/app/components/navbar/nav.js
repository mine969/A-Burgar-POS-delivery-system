import Link from 'next/link'
import Image from 'next/image'
import BurgerImg from '../../../img/BurgerA.png'
import VectorImg from '../../../img/Vector.png'

export default function Navbar() {
  return (
    <nav className="flex h-auto py-4 md:h-[87.195px] px-4 md:px-12 justify-between items-center shrink-0 w-full bg-[#FFECDC] border-b-[2px] border-[#8D0202]">
      <Image src={BurgerImg} alt="Burger" className="h-8 md:h-12 w-auto" />
      
      <ul className="hidden md:flex gap-9 font-bold text-lg items-center">
        <Link href="/">
          <li className="cursor-pointer hover:text-red-500 transition-colors">Home</li>
        </Link>
        <Link href="/components/order">
          <li className="cursor-pointer hover:text-red-500 transition-colors">Menu</li>
        </Link>
        <li className="cursor-pointer hover:text-red-500 transition-colors">About</li>
      </ul>

      <Image src={VectorImg} alt="logo" className="h-6 md:h-8 w-auto" />
    </nav>
  )
}
