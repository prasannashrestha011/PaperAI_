'use client';
import { useEffect, useRef, useState } from 'react';

export default function CursorLight() {
  const cursorRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
      setIsVisible(true);
    };

    const handleMouseLeave = () => {
      setIsVisible(false);
    };

    const handleMouseEnter = () => {
      setIsVisible(true);
    };

    window.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseleave', handleMouseLeave);
    document.addEventListener('mouseenter', handleMouseEnter);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseleave', handleMouseLeave);
      document.removeEventListener('mouseenter', handleMouseEnter);
    };
  }, []);

  return (
    <div
      ref={cursorRef}
      className={`fixed pointer-events-none transition-opacity duration-200 ${isVisible ? 'opacity-100' : 'opacity-0'}`}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        transform: 'translate(-50%, -50%)',
        zIndex: 9999,
      }}
    >
      {/* Outer Glow - Extra Large */}
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          width: '800px',
          height: '800px',
          background: 'radial-gradient(circle, rgba(59, 130, 246, 0.06) 0%, rgba(139, 92, 246, 0.03) 30%, transparent 60%)',
          transform: 'translate(-50%, -50%)',
          filter: 'blur(80px)',
        }}
      />
      {/* Middle Glow - Large */}
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          width: '500px',
          height: '500px',
          background: 'radial-gradient(circle, rgba(34, 211, 238, 0.08) 0%, rgba(59, 130, 246, 0.04) 40%, transparent 70%)',
          transform: 'translate(-50%, -50%)',
          filter: 'blur(60px)',
        }}
      />
      {/* Inner Glow - Subtle */}
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          width: '300px',
          height: '300px',
          background: 'radial-gradient(circle, rgba(34, 211, 238, 0.12) 0%, rgba(139, 92, 246, 0.05) 50%, transparent 80%)',
          transform: 'translate(-50%, -50%)',
          filter: 'blur(40px)',
        }}
      />
    </div>
  );
}