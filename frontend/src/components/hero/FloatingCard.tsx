'use client';

import { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { useTilt } from '@/hooks/useTilt';

interface FloatingCardProps {
  children: ReactNode;
  className?: string;
  depth?: number;
}

export function FloatingCard({ children, className, depth = 1 }: FloatingCardProps) {
  const tiltRef = useTilt(15, 1.05);

  return (
    <div 
      ref={tiltRef}
      className={cn(
        "glass-panel rounded-2xl p-6 transition-all duration-300 ease-out will-change-transform",
        "hover:shadow-[0_0_40px_rgba(139,92,246,0.15)]",
        className
      )}
      style={{ transform: `translateZ(${depth * 50}px)` }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl pointer-events-none" />
      <div className="relative z-10 h-full w-full">
        {children}
      </div>
    </div>
  );
}
