export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center">
      <div className="text-center text-white">
        <h1 className="text-6xl font-bold mb-4">Food Delivery Demo</h1>
        <p className="text-xl mb-8">Order your favorite food online</p>
        <div className="space-x-4">
          <a
            href="/login"
            className="bg-white text-orange-500 px-8 py-3 rounded-full font-bold hover:bg-gray-100 inline-block"
          >
            Login
          </a>
          <a
            href="/register"
            className="bg-orange-600 text-white px-8 py-3 rounded-full font-bold hover:bg-orange-700 inline-block"
          >
            Register
          </a>
        </div>
      </div>
    </div>
  );
}
