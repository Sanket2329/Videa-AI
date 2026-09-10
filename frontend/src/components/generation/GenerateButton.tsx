'use client';

import { cn } from '@/lib/utils';
import { ArrowRight, Loader2 } from 'lucide-react';
import { useTilt } from '@/hooks/useTilt';

interface GenerateButtonProps {
  isGenerating: boolean;
  disabled: boolean;
  onClick: () => void;
}

export function GenerateButton({ isGenerating, disabled, onClick }: GenerateButtonProps) {
  const tiltRef = useTilt(10, 1.02);

  return (
    <button
      ref={tiltRef as any}
      disabled={disabled || isGenerating}
      onClick={onClick}
      className={cn(
        "group relative w-full overflow-hidden rounded-[24px] transition-all duration-500",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        "h-20"
      )}
    >
      <div className="absolute inset-0 bg-white" />
      <div className="absolute inset-0 bg-gradient-to-r from-white via-violet-100 to-cyan-100 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      <div className="relative h-full flex items-center justify-center gap-4 text-black">
        {isGenerating ? (
          <>
            <Loader2 className="w-6 h-6 animate-spin text-violet-600" />
            <span className="text-sm font-bold tracking-[0.2em] uppercase">INITIALIZING...</span>
          </>
        ) : (
          <>
            <span className="text-sm font-bold tracking-[0.2em] uppercase">GENERATE VIDEO</span>
            <ArrowRight className="w-5 h-5 transition-transform duration-500 group-hover:translate-x-2" />
          </>
        )}
      </div>
    </button>
  );
}
