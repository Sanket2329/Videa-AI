'use client';

import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { VideoGeneration } from '@/lib/types/video';
import { HistoryCard3D } from './HistoryCard3D';

gsap.registerPlugin(ScrollTrigger);

export function ScrollGallery({ videos }: { videos: VideoGeneration[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const scrollWrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Only apply horizontal scroll on desktop, mobile can just be a CSS snap scroll
    const isMobile = window.innerWidth < 768;
    if (isMobile || !containerRef.current || !scrollWrapperRef.current || videos.length < 2) return;

    const sections = gsap.utils.toArray('.gallery-card');
    
    // We scroll the wrapper horizontally based on the height of the container
    gsap.to(sections, {
      xPercent: -100 * (sections.length - 1),
      ease: "none",
      scrollTrigger: {
        trigger: containerRef.current,
        pin: true,
        scrub: 1,
        snap: 1 / (sections.length - 1),
        end: () => "+=" + scrollWrapperRef.current?.offsetWidth,
      }
    });

    return () => {
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  }, [videos]);

  if (videos.length === 0) {
    return (
      <div className="w-full flex flex-col items-center justify-center py-32 text-center">
        <h2 className="text-2xl font-light tracking-widest text-white/40 mb-4">YOUR CREATIVE SPACE IS EMPTY</h2>
        <p className="text-white/20">Generate your first cinematic video above.</p>
      </div>
    );
  }

  return (
    <section ref={containerRef} className="relative w-full h-screen flex items-center overflow-hidden">
      
      {/* Background glow for gallery */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-[50vh] bg-violet-900/10 blur-[100px] pointer-events-none" />

      <div className="absolute top-20 left-12 md:left-24 z-10">
        <h2 className="text-xs font-bold tracking-[0.3em] text-white/50 uppercase">YOUR CREATIONS</h2>
        <p className="text-white/30 text-sm mt-2">Your latest generated videos.</p>
      </div>

      <div 
        ref={scrollWrapperRef} 
        className="flex gap-8 md:gap-16 px-12 md:px-24 items-center w-full md:w-[300vw] lg:w-[200vw] h-full overflow-x-auto md:overflow-x-visible snap-x md:snap-none snap-mandatory"
      >
        {videos.map((video, idx) => (
          <div key={video.id} className="gallery-card w-[80vw] md:w-[400px] shrink-0 snap-center">
            <HistoryCard3D video={video} />
          </div>
        ))}
      </div>
    </section>
  );
}
