'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { HeroSection } from '@/components/hero/HeroSection';
import { PromptEditor } from '@/components/prompt/PromptEditor';
import { ConfigCards } from '@/components/config/ConfigCards';
import { GenerateButton } from '@/components/generation/GenerateButton';
import { GenerationState } from '@/components/generation/GenerationState';
import { VideoResult } from '@/components/generation/VideoResult';
import { useVideoGeneration } from '@/lib/hooks/useVideoGeneration';
import { AspectRatio, Duration, VideoStyle } from '@/lib/types/video';

export default function Home() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login');
    }
  }, [user, isLoading, router]);

  const [prompt, setPrompt] = useState('');
  const [enhancedPrompt, setEnhancedPrompt] = useState<string | null>(null);
  const [negativePrompt, setNegativePrompt] = useState<string | null>(null);
  
  const [style, setStyle] = useState<VideoStyle>('cinematic');
  const [aspectRatio, setAspectRatio] = useState<AspectRatio>('16:9');
  const [duration, setDuration] = useState<Duration>(5);
  
  const [activeVideoId, setActiveVideoId] = useState<string | undefined>();
  
  const { statusQuery, generateMutation } = useVideoGeneration(activeVideoId);
  const currentGeneration = statusQuery.data;

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    try {
      const result = await generateMutation.mutateAsync({
        prompt,
        enhanced_prompt: enhancedPrompt,
        negative_prompt: negativePrompt,
        style,
        aspect_ratio: aspectRatio,
        duration,
      });
      setActiveVideoId(result.id);
      
      // Scroll to generation state
      setTimeout(() => {
        window.scrollBy({ top: window.innerHeight * 0.8, behavior: 'smooth' });
      }, 100);
    } catch (err) {
      console.error('Generation request failed', err);
    }
  };

  const isGenerating = currentGeneration && !['completed', 'failed', 'timeout', 'cancelled'].includes(currentGeneration.status);
  const hasResult = currentGeneration?.status === 'completed' && (currentGeneration.videoUrl || (currentGeneration as any).video_url);

  if (isLoading || !user) {
    return null;
  }

  return (
    <div className="w-full flex flex-col items-center">
      
      {!isGenerating && !hasResult && (
        <>
          <HeroSection />
          
          <div className="w-full max-w-5xl px-6 pb-40 space-y-24 relative z-10 mt-20">
            <div className="space-y-4">
              <h2 className="text-xs font-bold tracking-[0.3em] text-white/50 uppercase ml-4">1. Describe Scene</h2>
              <PromptEditor
                prompt={prompt}
                setPrompt={(val) => {
                  setPrompt(val);
                  if (enhancedPrompt) {
                    setEnhancedPrompt(null);
                    setNegativePrompt(null);
                  }
                }}
                stylePreset={style}
                onEnhanced={(enhanced, negative) => {
                  setEnhancedPrompt(enhanced);
                  setNegativePrompt(negative);
                }}
              />
            </div>

            <div className="space-y-4">
              <h2 className="text-xs font-bold tracking-[0.3em] text-white/50 uppercase ml-4">2. Configure</h2>
              <div className="glass-panel-heavy p-8 md:p-12 rounded-[32px]">
                <ConfigCards
                  style={style}
                  setStyle={setStyle as any}
                  aspectRatio={aspectRatio}
                  setAspectRatio={setAspectRatio}
                  duration={duration}
                  setDuration={setDuration}
                />
              </div>
            </div>

            <div className="pt-12">
              <GenerateButton 
                isGenerating={generateMutation.isPending} 
                disabled={!prompt.trim()} 
                onClick={handleGenerate} 
              />
            </div>
          </div>
        </>
      )}

      {isGenerating && currentGeneration && (
        <div className="w-full min-h-screen flex items-center justify-center p-6 mt-20">
          <GenerationState
            status={currentGeneration.status}
            error={(currentGeneration.errorMessage || (currentGeneration as any).error_message)}
          />
        </div>
      )}

      {hasResult && currentGeneration && (
        <div className="w-full min-h-screen flex items-center justify-center p-6 mt-20">
          <VideoResult
            videoUrl={(currentGeneration.videoUrl || (currentGeneration as any).video_url)!}
            originalPrompt={(currentGeneration.originalPrompt || (currentGeneration as any).original_prompt)}
            enhancedPrompt={(currentGeneration.enhancedPrompt || (currentGeneration as any).enhanced_prompt)}
            style={currentGeneration.style}
            aspectRatio={(currentGeneration.aspectRatio || (currentGeneration as any).aspect_ratio)}
            duration={currentGeneration.duration}
          />
        </div>
      )}
      
    </div>
  );
}
