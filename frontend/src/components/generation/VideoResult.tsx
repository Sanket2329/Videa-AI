'use client';

import { useTilt } from '@/hooks/useTilt';
import { AspectRatio } from '@/lib/api/videos';
import { cn } from '@/lib/utils';
import { Download, Play } from 'lucide-react';

interface VideoResultProps {
  videoUrl: string;
  originalPrompt: string;
  enhancedPrompt?: string | null;
  aspectRatio: AspectRatio;
  style: string;
  duration: number;
}

export function VideoResult({ videoUrl, originalPrompt, enhancedPrompt, aspectRatio, style, duration }: VideoResultProps) {
  const tiltRef = useTilt(5, 1.01);
  
  const aspectRatioClass = 
    aspectRatio === '9:16' ? 'aspect-[9/16] max-w-[400px]' : 
    aspectRatio === '1:1' ? 'aspect-square max-w-[600px]' : 
    'aspect-[16/9] w-full';

  return (
    <div className="w-full flex flex-col items-center gap-12 animate-in fade-in slide-in-from-bottom-8 duration-1000">
      
      <div 
        ref={tiltRef as any}
        className={cn(
          "relative w-full rounded-2xl overflow-hidden glass-panel border border-white/10 shadow-[0_0_50px_rgba(139,92,246,0.1)]",
          aspectRatioClass
        )}
      >
        <video
          src={videoUrl}
          controls
          autoPlay
          loop
          playsInline
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 rounded-2xl ring-1 ring-inset ring-white/10 pointer-events-none" />
      </div>

      <div className="w-full max-w-3xl glass-panel rounded-[24px] p-8 flex flex-col gap-8">
        <div className="space-y-4">
          <h4 className="text-[10px] font-bold tracking-[0.2em] text-white/40 uppercase">Enhanced Prompt</h4>
          <p className="text-lg text-white/90 font-light leading-relaxed">
            {enhancedPrompt || originalPrompt}
          </p>
        </div>

        <div className="flex flex-wrap gap-4 pt-6 border-t border-white/5">
          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-bold tracking-[0.2em] text-white/40 uppercase">Style</span>
            <span className="text-sm font-medium text-white/80 uppercase">{style.replace('-', ' ')}</span>
          </div>
          <div className="flex flex-col gap-1 px-4 border-l border-white/5">
            <span className="text-[10px] font-bold tracking-[0.2em] text-white/40 uppercase">Ratio</span>
            <span className="text-sm font-medium text-white/80">{aspectRatio}</span>
          </div>
          <div className="flex flex-col gap-1 px-4 border-l border-white/5">
            <span className="text-[10px] font-bold tracking-[0.2em] text-white/40 uppercase">Duration</span>
            <span className="text-sm font-medium text-white/80">{duration} SEC</span>
          </div>
        </div>

        <div className="flex items-center gap-4 pt-2">
          <a
            href={videoUrl}
            download
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 flex items-center justify-center gap-2 bg-white text-black hover:bg-white/90 h-12 rounded-xl text-xs font-bold tracking-[0.15em] transition-colors"
          >
            <Download className="w-4 h-4" />
            DOWNLOAD VIDEO
          </a>
          <button onClick={() => window.location.reload()} className="flex-1 h-12 rounded-xl border border-white/10 text-white/80 hover:bg-white/5 hover:text-white text-xs font-bold tracking-[0.15em] transition-colors">
            GENERATE AGAIN
          </button>
        </div>
      </div>

    </div>
  );
}
