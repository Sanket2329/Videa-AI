"use client";

import { useTilt } from "@/hooks/useTilt";
import { VideoGeneration } from "@/lib/types/video";
import { Play, Download, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { useVideoHistory } from "@/lib/hooks/useVideoHistory";

export function HistoryCard3D({ video, className }: { video: VideoGeneration, className?: string }) {
  const tiltRef = useTilt(10, 1.05);
  const [isPlaying, setIsPlaying] = useState(false);
  const { deleteMutation } = useVideoHistory();

  return (
    <div 
      ref={tiltRef as any}
      className={cn(
        "group relative w-full aspect-[4/5] sm:aspect-video md:aspect-[4/5] rounded-[24px] overflow-hidden glass-panel shrink-0",
        "transition-all duration-500 ease-out will-change-transform",
        "hover:z-10 hover:shadow-[0_0_50px_rgba(139,92,246,0.2)]",
        className
      )}
    >
      {isPlaying ? (
        <video 
          src={video.video_url || undefined} 
          autoPlay 
          controls 
          className="absolute inset-0 w-full h-full object-cover"
        />
      ) : (
        <>
          <video 
            src={video.video_url || undefined} 
            autoPlay
            loop
            muted
            playsInline
            className="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-opacity duration-500 blur-[2px] group-hover:blur-none"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
          
          <div className="absolute inset-0 p-6 flex flex-col justify-end pointer-events-none">
            <h3 className="text-sm font-light text-white line-clamp-3 mb-4 tracking-wide leading-relaxed">
              "{video.prompt}"
            </h3>
            
            <div className="flex flex-wrap gap-2 mb-6">
              <span className="px-2 py-1 rounded-md bg-white/10 backdrop-blur-md text-[9px] font-bold tracking-widest text-white/80 uppercase">
                {video.style}
              </span>
              <span className="px-2 py-1 rounded-md bg-white/10 backdrop-blur-md text-[9px] font-bold tracking-widest text-white/80">
                {video.aspect_ratio}
              </span>
              {video.status !== 'completed' && (
                <span className={cn(
                  "px-2 py-1 rounded-md backdrop-blur-md text-[9px] font-bold tracking-widest uppercase",
                  video.status === 'failed' ? "bg-red-500/20 text-red-200" : "bg-blue-500/20 text-blue-200 animate-pulse"
                )}>
                  {video.status}
                </span>
              )}
            </div>

            <div className="flex items-center gap-3 opacity-0 translate-y-4 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-500 pointer-events-auto">
              {video.status === 'completed' ? (
                <button 
                  onClick={() => setIsPlaying(true)}
                  className="flex-1 h-10 flex items-center justify-center gap-2 bg-white text-black rounded-xl text-xs font-bold hover:bg-gray-200 transition-colors"
                >
                  <Play className="w-4 h-4 fill-current" /> PLAY
                </button>
              ) : (
                <button 
                  disabled
                  className="flex-1 h-10 flex items-center justify-center gap-2 bg-white/10 text-white/50 rounded-xl text-xs font-bold cursor-not-allowed"
                >
                  {video.status === 'failed' ? 'FAILED' : 'PROCESSING...'}
                </button>
              )}
              {video.video_url && (
                <a 
                  href={video.video_url}
                  download
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 flex items-center justify-center bg-white/10 rounded-xl text-white hover:bg-white/20 transition-colors"
                >
                  <Download className="w-4 h-4" />
                </a>
              )}
              <button 
                onClick={() => deleteMutation.mutate(video.id)}
                disabled={deleteMutation.isPending}
                className="w-10 h-10 flex items-center justify-center bg-white/10 rounded-xl text-red-400 hover:bg-red-500/20 transition-colors disabled:opacity-50"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        </>
      )}
      <div className="absolute inset-0 rounded-[24px] ring-1 ring-inset ring-white/10 pointer-events-none" />
    </div>
  );
}
