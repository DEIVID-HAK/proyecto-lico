import React from 'react';
import { TrendingUp, Users, Package, DollarSign, AlertCircle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  // Datos falsos (Mock Data) para simular el dashboard
  const stats = [
    { title: 'Ventas del Día', value: '$1.245.000', icon: <DollarSign size={24} />, trend: '+12%', color: '#3b82f6' },
    { title: 'Órdenes Activas', value: '8', icon: <TrendingUp size={24} />, trend: 'Normal', color: '#10b981' },
    { title: 'Clientes', value: '142', icon: <Users size={24} />, trend: '+5%', color: '#a855f7' },
    { title: 'Bajo Inventario', value: '3', icon: <Package size={24} />, trend: 'Requiere atención', color: '#ef4444' },
  ];

  const salesData = [
    { name: 'Lun', ventas: 450000 },
    { name: 'Mar', ventas: 520000 },
    { name: 'Mié', ventas: 480000 },
    { name: 'Jue', ventas: 610000 },
    { name: 'Vie', ventas: 1200000 },
    { name: 'Sáb', ventas: 1850000 },
    { name: 'Dom', ventas: 1100000 },
  ];

  const recentSales = [
    { id: 'ORD-001', time: '10:45 AM', items: '2x Cerveza Aguila, 1x Ron Viejo de Caldas', total: '$52.000', status: 'Completada' },
    { id: 'ORD-002', time: '11:15 AM', items: '1x Whisky Old Parr 12 Años', total: '$180.000', status: 'Completada' },
    { id: 'ORD-003', time: '11:30 AM', items: '6x Cerveza Poker (Lata)', total: '$21.000', status: 'Completada' },
    { id: 'ORD-004', time: '12:05 PM', items: '1x Aguardiente Antioqueño Tapa Roja', total: '$45.000', status: 'En Proceso' },
  ];

  // Custom tooltip formater para pesos colombianos
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', padding: '12px', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}>
          <p style={{ color: '#fff', marginBottom: '4px' }}>{label}</p>
          <p style={{ color: '#38bdf8', fontWeight: 'bold' }}>
            ${payload[0].value.toLocaleString('es-CO')}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px', paddingBottom: '40px' }}>
      
      <div>
        <h2 style={{ fontSize: '28px', fontWeight: 'bold' }}>Panel de Control</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Resumen de operaciones y estado del negocio.</p>
      </div>

      {/* Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
        {stats.map((stat, i) => (
          <div key={i} className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ padding: '12px', borderRadius: '12px', backgroundColor: `${stat.color}20`, color: stat.color }}>
                {stat.icon}
              </div>
              <span style={{ fontSize: '13px', fontWeight: '500', color: stat.color }}>{stat.trend}</span>
            </div>
            <div>
              <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '4px' }}>{stat.title}</h3>
              <p style={{ fontSize: '28px', fontWeight: 'bold' }}>{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Sales Chart */}
      <div className="glass-panel" style={{ padding: '24px', height: '400px', display: 'flex', flexDirection: 'column' }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '24px' }}>Ventas de la Semana</h3>
        <div style={{ flex: 1, width: '100%', height: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={salesData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorVentas" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#38bdf8" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} axisLine={false} tickLine={false} />
              <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} axisLine={false} tickLine={false} tickFormatter={(value) => `$${value/1000}k`} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="ventas" stroke="#38bdf8" strokeWidth={3} fillOpacity={1} fill="url(#colorVentas)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        {/* Recent Sales Table */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '20px' }}>Ventas Recientes</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '12px' }}>Orden</th>
                  <th style={{ padding: '12px' }}>Hora</th>
                  <th style={{ padding: '12px' }}>Artículos</th>
                  <th style={{ padding: '12px' }}>Total</th>
                  <th style={{ padding: '12px' }}>Estado</th>
                </tr>
              </thead>
              <tbody>
                {recentSales.map((sale, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '16px 12px', fontWeight: '500' }}>{sale.id}</td>
                    <td style={{ padding: '16px 12px', color: 'var(--text-secondary)' }}>{sale.time}</td>
                    <td style={{ padding: '16px 12px' }}>{sale.items}</td>
                    <td style={{ padding: '16px 12px', fontWeight: 'bold' }}>{sale.total}</td>
                    <td style={{ padding: '16px 12px' }}>
                      <span style={{ 
                        padding: '4px 8px', 
                        borderRadius: '12px', 
                        fontSize: '12px',
                        backgroundColor: sale.status === 'Completada' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                        color: sale.status === 'Completada' ? 'var(--success)' : '#f59e0b'
                      }}>
                        {sale.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Alerts Sidebar */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '4px' }}>Alertas de Inventario</h3>
          
          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', padding: '16px', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderRadius: '12px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
            <AlertCircle size={20} color="var(--danger)" style={{ flexShrink: 0 }} />
            <div>
              <p style={{ fontSize: '14px', fontWeight: '600', color: 'var(--danger)' }}>Whisky Old Parr 12 Años</p>
              <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Quedan solo 2 unidades en bodega.</p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', padding: '16px', backgroundColor: 'rgba(245, 158, 11, 0.1)', borderRadius: '12px', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
            <AlertCircle size={20} color="#f59e0b" style={{ flexShrink: 0 }} />
            <div>
              <p style={{ fontSize: '14px', fontWeight: '600', color: '#f59e0b' }}>Aguardiente Blanco del Valle</p>
              <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Faltan 5 unidades para el nivel mínimo.</p>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}
