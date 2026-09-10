'use client';

import { useState, useRef, useEffect } from 'react';
import { Wand2, X } from 'lucide-react';
import { usePromptEnhancement } from '@/lib/hooks/usePromptEnhancement';
import { cn } from '@/lib/utils';
import gsap from 'gsap';

interface PromptEditorProps {
  prompt: string;
  setPrompt: (value: string) => void;
  stylePreset: string;
  onEnhanced: (enhanced: string, negative: string) => void;
}

const MAX_CHARS = 1000;

export function PromptEditor({ prompt, setPrompt, stylePreset, onEnhanced }: PromptEditorProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [enhancedTags, setEnhancedTags] = useState<string[]>([]);
  
  const containerRef = useRef<HTMLDivElement>(null);
  const enhanceMutation = usePromptEnhancement();

  useEffect(() => {
    if (isFocused && containerRef.current) {
      gsap.to(containerRef.current, { scale: 1.01, duration: 0.4, ease: 'power2.out' });
    } else if (containerRef.current) {
      gsap.to(containerRef.current, { scale: 1, duration: 0.4, ease: 'power2.out' });
    }
  }, [isFocused]);

  const handleEnhance = async () => {
    if (!prompt.trim() || isEnhancing) return;
    setIsEnhancing(true);
    
    // Cinematic loading transition
    if (containerRef.current) {
      gsap.to(containerRef.current, { 
        boxShadow: '0 0 50px rgba(139, 92, 246, 0.4)',
        borderColor: 'rgba(139, 92, 246, 0.5)',
        duration: 1,
        yoyo: true,
        repeat: -1
      });
    }

    try {
      const result = await enhanceMutation.mutateAsync({
        prompt,
        style: stylePreset,
      });
      
      // Stop animation
      gsap.killTweensOf(containerRef.current);
      gsap.to(containerRef.current, {
        boxShadow: '0 0 0px rgba(139, 92, 246, 0)',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        duration: 0.5
      });

      setPrompt(result.enhanced_prompt);
      onEnhanced(result.enhanced_prompt, result.negative_prompt);
      
      // Generate some fake tags for the "premium" feel from the prompt
      setEnhancedTags(['CAMERA: 50MM', 'LIGHTING: CINEMATIC', `STYLE: ${stylePreset.toUpperCase()}`]);
      
    } catch (err) {
      console.error('Enhancement failed:', err);
      gsap.killTweensOf(containerRef.current);
      gsap.to(containerRef.current, { borderColor: 'rgba(239, 68, 68, 0.5)', duration: 0.2, yoyo: true, repeat: 3 });
    } finally {
      setIsEnhancing(false);
    }
  };

  return (
    <div 
      ref={containerRef}
      className={cn(
        "glass-panel-heavy rounded-3xl p-1 relative overflow-hidden transition-all duration-500",
        isFocused ? "border-white/20 shadow-[0_0_30px_rgba(255,255,255,0.05)]" : "border-white/10"
      )}
    >
      {/* Animated glow background */}
      <div 
        className={cn(
          "absolute -inset-[100%] opacity-20 bg-[conic-gradient(from_0deg,transparent_0_340deg,white_360deg)] animate-[spin_4s_linear_infinite] transition-opacity duration-500",
          isFocused ? "opacity-30" : "opacity-0"
        )} 
      />
      
      <div className="relative bg-[#050505]/90 rounded-[22px] h-full flex flex-col backdrop-blur-xl">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value.slice(0, MAX_CHARS))}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="Describe the scene you want to create..."
          className="w-full h-48 bg-transparent text-white/90 placeholder:text-white/20 px-8 py-8 text-xl md:text-2xl font-light tracking-wide focus:outline-none resize-none"
        />
        
        {enhancedTags.length > 0 && (
          <div className="px-8 pb-4 flex flex-wrap gap-2">
            {enhancedTags.map((tag, i) => (
              <span key={i} className="px-3 py-1 rounded-full text-[10px] font-bold tracking-widest text-violet-300 bg-violet-500/10 border border-violet-500/20">
                {tag}
              </span>
            ))}
          </div>
        )}

        <div className="px-8 py-6 border-t border-white/5 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <span className={cn(
              "text-xs font-mono tracking-widest transition-colors",
              prompt.length >= MAX_CHARS ? "text-red-400" : "text-white/30"
            )}>
              {prompt.length} / {MAX_CHARS}
            </span>
            {prompt.length > 0 && (
              <button 
                onClick={() => { setPrompt(''); setEnhancedTags([]); }}
                className="text-white/30 hover:text-white/80 transition-colors"
                title="Clear prompt"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
          
          <button
            onClick={handleEnhance}
            disabled={!prompt.trim() || isEnhancing}
            className="group relative flex items-center gap-2 px-6 py-2.5 rounded-full overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div className="absolute inset-0 bg-white/5 group-hover:bg-white/10 transition-colors" />
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 bg-gradient-to-r from-violet-600/20 to-cyan-600/20 transition-opacity" />
            <Wand2 className={cn("w-4 h-4 relative z-10 text-violet-400", isEnhancing && "animate-spin")} />
            <span className="text-xs font-bold tracking-widest text-white/90 relative z-10">
              {isEnhancing ? 'ENHANCING...' : '✦ ENHANCE'}
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}
