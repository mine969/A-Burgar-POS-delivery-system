'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function Menu() {
  const [menuItems, setMenuItems] = useState([]);
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    loadMenu();
  }, []);

  const loadMenu = async () => {
    try {
      const items = await api.getMenu();
      setMenuItems(items);
    } catch (err) {
      setError('Failed to load menu');
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (item) => {
    setCart([...cart, { ...item, quantity: 1 }]);
  };

  const placeOrder = async () => {
    try {
      const token = localStorage.getItem('token');
      const orderItems = cart.map(item => ({
        menu_item_id: item.id,
        quantity: 1
      }));
      await api.createOrder(orderItems, token, "123 Demo St");
      alert('Order placed successfully!');
      setCart([]);
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center text-black">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Menu</h1>
          <div className="bg-white p-4 rounded-lg shadow">
            <span className="font-bold text-gray-800">Cart: {cart.length} items</span>
            {cart.length > 0 && (
              <button
                onClick={placeOrder}
                className="ml-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Place Order
              </button>
            )}
          </div>
        </div>

        {error && <div className="text-red-500 mb-4">{error}</div>}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {menuItems.map((item) => (
            <div key={item.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition">
              <div className="p-6">
                <div className="flex justify-between items-start">
                  <h3 className="text-xl font-semibold text-gray-900">{item.name}</h3>
                  <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    ${item.price}
                  </span>
                </div>
                <p className="mt-2 text-gray-600">{item.description}</p>
                <div className="mt-4">
                  <button
                    onClick={() => addToCart(item)}
                    className="w-full py-2 px-4 bg-gray-900 text-white rounded hover:bg-gray-800 transition"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
