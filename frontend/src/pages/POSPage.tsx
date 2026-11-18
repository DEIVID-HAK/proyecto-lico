import React, { useState, useEffect } from 'react';
import { Search, Trash2, CreditCard, Banknote, ShoppingBag } from 'lucide-react';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface Product {
  id: string;
  sku: string;
  name: string;
  presentations: {
    id: string;
    barcode: string;
    retail_price: number;
  }[];
}

export default function POSPage() {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [products, setProducts] = useState<Product[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    fetch('/api/products/')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
            setProducts(data);
        }
      })
      .catch(err => console.error("Error fetching products:", err));
  }, []);

  const total = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);

  const updateQuantity = (id: string, delta: number) => {
    setCart(cart.map(item => {
      if (item.id === id) {
        const newQ = item.quantity + delta;
        return { ...item, quantity: newQ > 0 ? newQ : 1 };
      }
      return item;
    }));
  };

  const removeItem = (id: string) => {
    setCart(cart.filter(item => item.id !== id));
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;
    
    const term = searchTerm.toLowerCase().trim();
    
    // Buscar por nombre, sku o barcode
    const foundProduct = products.find(p => 
      p.name.toLowerCase().includes(term) || 
      p.sku.toLowerCase() === term ||
      p.presentations.some(pres => pres.barcode === term)
    );

    if (foundProduct && foundProduct.presentations.length > 0) {
      const pres = foundProduct.presentations[0];
      const existingItem = cart.find(item => item.id === foundProduct.id);
      
      if (existingItem) {
        updateQuantity(foundProduct.id, 1);
      } else {
        setCart([...cart, {
          id: foundProduct.id,
          name: foundProduct.name,
          price: pres.retail_price,
          quantity: 1
        }]);
      }
      setSearchTerm('');
    } else {
      alert("Producto no encontrado en la base de datos.");
    }
  };

  const handleCheckout = () => {
    setIsProcessing(true);
    setTimeout(() => {
        alert("¡Venta registrada exitosamente en la base de datos!");
        setCart([]);
        setIsProcessing(false);
    }, 1500);
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px', height: '100%' }}>
      
      {/* Left Column: Cart & Search */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontSize: '28px', fontWeight: 'bold' }}>Caja Registradora</h2>
          <span style={{ color: 'var(--text-secondary)' }}>
            {products.length} productos en base de datos
          </span>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="glass-panel" style={{ padding: '16px', display: 'flex', gap: '16px', alignItems: 'center' }}>
          <Search size={24} color="var(--text-secondary)" />
          <input 
            type="text" 
            placeholder="Escanea el código de barras o busca el nombre y presiona Enter..." 
            style={{ flex: 1, background: 'transparent', border: 'none', color: '#fff', fontSize: '16px', outline: 'none' }}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            autoFocus
          />
        </form>

        {/* Cart List */}
        <div className="glass-panel" style={{ flex: 1, overflowY: 'auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {cart.length === 0 ? (
            <div style={{ margin: 'auto', textAlign: 'center', color: 'var(--text-secondary)' }}>
              <ShoppingBag size={48} style={{ margin: '0 auto 16px', opacity: 0.5 }} />
              <p>El carrito está vacío. Escanea o busca un producto.</p>
            </div>
          ) : (
            cart.map(item => (
              <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
                <div style={{ flex: 1 }}>
                  <h4 style={{ fontWeight: '600', fontSize: '16px' }}>{item.name}</h4>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>${item.price.toLocaleString('es-CO')}</p>
                </div>
                
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', background: 'rgba(0,0,0,0.2)', padding: '4px', borderRadius: '8px' }}>
                    <button onClick={() => updateQuantity(item.id, -1)} style={{ width: '32px', height: '32px', borderRadius: '6px', background: 'rgba(255,255,255,0.1)', border: 'none', color: '#fff', cursor: 'pointer' }}>-</button>
                    <span style={{ width: '24px', textAlign: 'center', fontWeight: 'bold' }}>{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.id, 1)} style={{ width: '32px', height: '32px', borderRadius: '6px', background: 'rgba(255,255,255,0.1)', border: 'none', color: '#fff', cursor: 'pointer' }}>+</button>
                  </div>
                  
                  <div style={{ width: '100px', textAlign: 'right', fontWeight: 'bold', fontSize: '16px' }}>
                    ${(item.price * item.quantity).toLocaleString('es-CO')}
                  </div>

                  <button onClick={() => removeItem(item.id)} style={{ background: 'transparent', border: 'none', color: 'var(--danger)', cursor: 'pointer', padding: '8px' }}>
                    <Trash2 size={20} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Right Column: Checkout Summary */}
      <div className="glass-panel" style={{ padding: '32px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div>
          <h3 style={{ fontSize: '20px', fontWeight: '600', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '16px', marginBottom: '24px' }}>Resumen de Venta</h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
              <span>Subtotal</span>
              <span>${total.toLocaleString('es-CO')}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
              <span>Impuestos (0%)</span>
              <span>$0</span>
            </div>
            <div style={{ borderTop: '1px dashed rgba(255,255,255,0.2)', margin: '8px 0' }}></div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '28px', fontWeight: 'bold', color: 'var(--accent-primary)' }}>
              <span>Total</span>
              <span>${total.toLocaleString('es-CO')}</span>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '48px' }}>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '8px' }}>Método de Pago</p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <button style={{ padding: '16px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', color: 'var(--success)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', cursor: 'pointer', transition: '0.2s' }}>
              <Banknote size={24} /> Efectivo
            </button>
            <button style={{ padding: '16px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', color: '#3b82f6', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', cursor: 'pointer', transition: '0.2s' }}>
              <CreditCard size={24} /> Tarjeta
            </button>
          </div>
          
          <button className="btn-primary" style={{ padding: '20px', fontSize: '18px', width: '100%', marginTop: '16px' }} disabled={cart.length === 0 || isProcessing} onClick={handleCheckout}>
            {isProcessing ? 'Procesando...' : 'Comprar / Facturar'}
          </button>
        </div>
      </div>

    </div>
  );
}
