const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async register(email: string, password: string, name: string) {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name, role: 'customer' })
    });
    return response.json();
  },

  async login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    });
    return response.json();
  },

  async getMenu() {
    const response = await fetch(`${API_BASE_URL}/menu/`);
    return response.json();
  },

  async createOrder(items: any[], token: string) {
    const response = await fetch(`${API_BASE_URL}/orders/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ items })
    });
    return response.json();
  }
};
