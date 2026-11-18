import React, { useState } from 'react';
import { PackagePlus, LayoutDashboard, ShoppingCart, LogOut } from 'lucide-react';
import AddProductPage from './pages/AddProductPage';
import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import POSPage from './pages/POSPage';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState('pos');

  if (!isAuthenticated) {
    return <LoginPage onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar - Glassmorphism */}
      <aside className="glass-panel" style={{ width: '280px', margin: '20px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
        <div>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', background: 'linear-gradient(to right, #60a5fa, #a78bfa)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', letterSpacing: '-0.5px' }}>
            LiquorPOS
          </h1>
        </div>
        
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '12px', flex: 1 }}>
          <button className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <LayoutDashboard size={20} /> Dashboard
          </button>
          <button className={`nav-btn ${activeTab === 'pos' ? 'active' : ''}`} onClick={() => setActiveTab('pos')}>
            <ShoppingCart size={20} /> Punto de Venta
          </button>
          <button className={`nav-btn ${activeTab === 'products' ? 'active' : ''}`} onClick={() => setActiveTab('products')}>
            <PackagePlus size={20} /> Productos
          </button>
        </nav>

        <button className="nav-btn" style={{ color: 'var(--danger)', marginTop: 'auto' }} onClick={() => setIsAuthenticated(false)}>
          <LogOut size={20} /> Cerrar Sesión
        </button>
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, padding: '20px 20px 20px 0', overflowY: 'auto' }}>
        {activeTab === 'products' && <AddProductPage />}
        {activeTab === 'dashboard' && <DashboardPage />}
        {activeTab === 'pos' && <POSPage />}
      </main>

      <style>{`
        .nav-btn {
          display: flex;
          align-items: center;
          gap: 12px;
          width: 100%;
          padding: 12px 16px;
          border-radius: 8px;
          border: none;
          background: transparent;
          color: var(--text-secondary);
          font-size: 15px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          text-align: left;
        }
        .nav-btn:hover {
          background: rgba(255,255,255,0.05);
          color: var(--text-primary);
        }
        .nav-btn.active {
          background: rgba(59, 130, 246, 0.15);
          color: var(--accent-primary);
          border-right: 3px solid var(--accent-primary);
        }
      `}</style>
    </div>
  );
}

export default App;
