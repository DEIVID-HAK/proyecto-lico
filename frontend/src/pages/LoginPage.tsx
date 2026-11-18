import React, { useState } from 'react';
import { Lock, User } from 'lucide-react';
import './LoginPage.css';

interface LoginPageProps {
  onLogin: () => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsVerifying(true);

    // Simulate server request as seen in Script.js
    setTimeout(() => {
      setIsVerifying(false);
      if (username === 'admin' && password === 'admin') {
        onLogin(); 
      } else {
        alert("Credenciales incorrectas. (Pista: usa admin / admin)");
      }
    }, 1200);
  };

  return (
    <div className="login-page-container">
      <div className="custom-login-box">
        <form id="loginForm" onSubmit={handleSubmit}>
          <h2>LOGIN</h2>
          
          <div className="custom-input-group">
            <input 
              type="text" 
              id="username" 
              required 
              value={username} 
              onChange={e => setUsername(e.target.value)} 
            />
            <label>Username</label>
            <User size={16} />
          </div>

          <div className="custom-input-group">
            <input 
              type="password" 
              id="password" 
              required 
              value={password} 
              onChange={e => setPassword(e.target.value)} 
            />
            <label>Password</label>
            <Lock size={16} />
          </div>

          <button 
            type="submit" 
            className="custom-login-btn" 
            id="submitBtn"
            disabled={isVerifying}
          >
            {isVerifying ? 'Verifying...' : 'Sign In'}
          </button>

          <p className="signup-link">
            New here? <a href="#">Create Account</a>
          </p>
        </form>
      </div>
    </div>
  );
}
