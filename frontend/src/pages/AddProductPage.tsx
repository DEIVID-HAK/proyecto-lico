import React, { useState } from 'react';
import { Save, AlertCircle } from 'lucide-react';

export default function AddProductPage() {
  const [formData, setFormData] = useState({
    sku: '',
    name: '',
    category: 'Cervezas',
    alcohol_grade_abv: 4.5,
    volume_ml: 330,
    invima_registration: '',
    presentations: [
      {
        name: 'Botella Individual',
        barcode: '',
        units_per_presentation: 1,
        cost: 0,
        retail_price: 0,
        wholesale_price: 0
      }
    ]
  });

  const [status, setStatus] = useState({ type: '', message: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus({ type: 'loading', message: 'Guardando producto...' });
    
    try {
      const response = await fetch('/api/products/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      const data = await response.json();
      
      if (!response.ok) throw new Error(data.detail || 'Error al guardar');
      
      setStatus({ type: 'success', message: '¡Producto registrado con éxito!' });
    } catch (err: any) {
      setStatus({ type: 'error', message: err.message });
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '32px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '28px', fontWeight: '600', marginBottom: '8px' }}>Registrar Nuevo Licor</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Ingresa los datos del producto y su presentación principal para el Punto de Venta.</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          
          <div className="form-group">
            <label className="form-label">SKU (Código Interno)</label>
            <input type="text" className="input-field" required placeholder="Ej: AGU-ANT-750" 
              value={formData.sku} onChange={e => setFormData({...formData, sku: e.target.value})} />
          </div>

          <div className="form-group">
            <label className="form-label">Nombre del Producto</label>
            <input type="text" className="input-field" required placeholder="Ej: Aguardiente Antioqueño Tapa Azul"
              value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
          </div>

          <div className="form-group">
            <label className="form-label">Categoría</label>
            <select className="input-field" value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})}>
              <option>Cervezas</option>
              <option>Aguardiente</option>
              <option>Ron</option>
              <option>Whisky</option>
              <option>Vinos</option>
            </select>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Grado de Alcohol (%)</label>
              <input type="number" step="0.1" className="input-field" required placeholder="Ej: 29.0"
                value={formData.alcohol_grade_abv} onChange={e => setFormData({...formData, alcohol_grade_abv: parseFloat(e.target.value)})} />
            </div>
            <div className="form-group">
              <label className="form-label">Volumen (ml)</label>
              <input type="number" className="input-field" required placeholder="Ej: 750"
                value={formData.volume_ml} onChange={e => setFormData({...formData, volume_ml: parseInt(e.target.value)})} />
            </div>
          </div>

          <div className="form-group" style={{ gridColumn: '1 / -1' }}>
            <label className="form-label">Registro INVIMA</label>
            <input type="text" className="input-field" required={formData.alcohol_grade_abv > 0} placeholder="Ej: L-0001234 (Obligatorio para licores)"
              value={formData.invima_registration} onChange={e => setFormData({...formData, invima_registration: e.target.value})} />
          </div>
        </div>

        <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '32px 0' }} />
        
        <h3 style={{ fontSize: '20px', marginBottom: '20px' }}>Presentación Principal</h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
           <div className="form-group">
            <label className="form-label">Código de Barras</label>
            <input type="text" className="input-field" required placeholder="Ej: 7702004000123"
              value={formData.presentations[0].barcode} 
              onChange={e => {
                const newPres = [...formData.presentations];
                newPres[0].barcode = e.target.value;
                setFormData({...formData, presentations: newPres});
              }} />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
             <div className="form-group">
              <label className="form-label">Costo (COP $)</label>
              <input type="number" className="input-field" required placeholder="Ej: 32000"
                value={formData.presentations[0].cost} 
                onChange={e => {
                  const newPres = [...formData.presentations];
                  newPres[0].cost = parseFloat(e.target.value);
                  setFormData({...formData, presentations: newPres});
                }} />
            </div>
            <div className="form-group">
              <label className="form-label">Precio Venta (COP $)</label>
              <input type="number" className="input-field" required placeholder="Ej: 45000"
                value={formData.presentations[0].retail_price} 
                onChange={e => {
                  const newPres = [...formData.presentations];
                  newPres[0].retail_price = parseFloat(e.target.value);
                  setFormData({...formData, presentations: newPres});
                }} />
            </div>
          </div>
        </div>

        {status.message && (
          <div style={{ 
            padding: '16px', 
            borderRadius: '8px', 
            marginTop: '24px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            backgroundColor: status.type === 'error' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)',
            color: status.type === 'error' ? 'var(--danger)' : 'var(--success)'
          }}>
            <AlertCircle size={20} />
            <span>{status.message}</span>
          </div>
        )}

        <div style={{ marginTop: '32px', display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="btn-primary" disabled={status.type === 'loading'}>
            <Save size={20} /> Guardar Producto
          </button>
        </div>
      </form>
    </div>
  );
}
