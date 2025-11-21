'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function MenuPage() {
  const [menu, setMenu] = useState<any[]>([]);
  const [cart, setCart] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    
    api.getMenu().then(setMenu);
  }, [router]);

  const addToCart = (item: any) => {
    setCart([...cart, item]);
  };

  const placeOrder = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    const items = cart.map(item => ({
      menu_item_id: item.id,
      quantity: 1
    }));

    await api.createOrder(items, token);
    alert('Order placed successfully!');
    setCart([]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-orange-500 text-white p-6 shadow-lg">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold">Menu</h1>
          <div className="flex items-center gap-4">
            <span className="bg-white text-orange-500 px-4 py-2 rounded-full font-semibold">
              Cart: {cart.length} items
            </span>
            <button
              onClick={() => { localStorage.removeItem('token'); router.push('/login'); }}
              className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {menu.map((item) => (
            <div key={item.id} className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition">
              <h3 className="text-xl font-bold text-gray-800 mb-2">{item.name}</h3>
              <p className="text-gray-600 mb-4">{item.description}</p>
              <div className="flex justify-between items-center">
                <span className="text-2xl font-bold text-orange-500">${item.price}</span>
                <button
                  onClick={() => addToCart(item)}
                  className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg"
                >
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>

        {cart.length > 0 && (
          <div className="fixed bottom-6 right-6">
            <button
              onClick={placeOrder}
              className="bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-full shadow-2xl text-lg font-bold"
            >
              Place Order (${cart.reduce((sum, item) => sum + item.price, 0).toFixed(2)})
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
