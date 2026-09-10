'use client';

import { cn } from '@/lib/utils';
import { Check, CircleDashed } from 'lucide-react';
import { VideoStatus } from '@/lib/types/video';

export function GenerationState({ status, error }: { status: VideoStatus; error?: string | null }) {
  const steps = [
    { id: 'validated', label: 'Prompt validated', active: true, completed: true },
    { id: 'enhanced', label: 'AI enhancement complete', active: true, completed: true },
    { id: 'submitted', label: 'Generation request submitted', active: true, completed: true },
    { id: 'queued', label: 'Queued', active: status === 'queued', completed: ['processing', 'completed'].includes(status) },
    { id: 'generating', label: 'Creating video', active: status === 'processing', completed: status === 'completed' },
    { id: 'finalizing', label: 'Finalizing', active: status === 'processing', completed: status === 'completed' }
  ];

  if (status === 'failed' || status === 'timeout') {
    return (
      <div className="w-full glass-panel-heavy rounded-[32px] p-12 text-center border-red-500/20">
        <h2 className="text-2xl font-light tracking-wide text-white mb-4">GENERATION FAILED</h2>
        <p className="text-red-400 text-sm tracking-wide">{error || "We couldn't complete this generation."}</p>
      </div>
    );
  }

  return (
    <div className="w-full glass-panel-heavy rounded-[32px] p-12 relative overflow-hidden">
      {/* Scanning light effect */}
      <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-violet-500 to-transparent opacity-50 animate-[scan_3s_ease-in-out_infinite]" />
      
      <div className="max-w-md mx-auto">
        <h2 className="text-xl font-light tracking-wide text-white mb-10 text-center">GENERATING YOUR VIDEO</h2>
        
        <div className="space-y-6">
          {steps.map((step, i) => (
            <div 
              key={step.id} 
              className={cn(
                "flex items-center gap-4 transition-all duration-700",
                step.completed ? "opacity-100 translate-x-0" : 
                step.active ? "opacity-100 translate-x-0" : "opacity-30 -translate-x-4"
              )}
            >
              <div className="w-6 h-6 flex items-center justify-center shrink-0">
                {step.completed ? (
                  <Check className="w-5 h-5 text-violet-400" />
                ) : step.active ? (
                  <CircleDashed className="w-5 h-5 text-cyan-400 animate-spin-slow" />
                ) : (
                  <div className="w-2 h-2 rounded-full bg-white/20" />
                )}
              </div>
              <span className={cn(
                "text-sm font-medium tracking-wider",
                step.completed ? "text-white/60" :
                step.active ? "text-white" : "text-white/30"
              )}>
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
