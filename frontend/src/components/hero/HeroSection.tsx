'use client';

import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { FloatingCard } from './FloatingCard';
import { Video, Wand2, MonitorPlay, Sparkles } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export function HeroSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const textRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || !textRef.current || !cardsRef.current) return;
    
    // Parallax text
    gsap.to(textRef.current, {
      y: 200,
      opacity: 0,
      ease: 'none',
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top top',
        end: 'bottom top',
        scrub: true,
      }
    });

    // Animate cards converging
    const cards = gsap.utils.toArray('.hero-card') as HTMLElement[];
    
    // Initial random scatter
    cards.forEach((card, i) => {
      gsap.set(card, {
        x: (Math.random() - 0.5) * window.innerWidth * 1.5,
        y: (Math.random() - 0.5) * window.innerHeight * 1.5,
        rotationZ: (Math.random() - 0.5) * 45,
        scale: 0.8 + Math.random() * 0.4,
        opacity: 0
      });
    });

    // Entrance animation
    gsap.to(cards, {
      x: (i) => {
        const radius = window.innerWidth * 0.35;
        const angle = (i / cards.length) * Math.PI * 2;
        return Math.cos(angle) * radius;
      },
      y: (i) => {
        const radius = window.innerHeight * 0.35;
        const angle = (i / cards.length) * Math.PI * 2;
        return Math.sin(angle) * radius;
      },
      rotationZ: (i) => (i % 2 === 0 ? 5 : -5),
      scale: 1,
      opacity: 0.7,
      duration: 2,
      stagger: 0.1,
      ease: 'power3.out',
      delay: 0.5
    });

    // Scroll to converge
    gsap.to(cards, {
      x: 0,
      y: 0,
      rotationZ: 0,
      scale: 0.9,
      opacity: 0,
      ease: 'power2.inOut',
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top top',
        end: 'bottom 20%',
        scrub: 1,
      }
    });

    return () => {
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  }, []);

  return (
    <section ref={containerRef} className="relative min-h-[120vh] w-full flex items-center justify-center perspective-[2000px] overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80vw] h-[80vw] max-w-[800px] max-h-[800px] bg-violet-600/20 rounded-full blur-[120px] mix-blend-screen pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] max-w-[600px] max-h-[600px] bg-cyan-600/10 rounded-full blur-[100px] mix-blend-screen pointer-events-none" />

      {/* Floating 3D Cards */}
      <div ref={cardsRef} className="absolute inset-0 pointer-events-none flex items-center justify-center z-0">
        <FloatingCard className="hero-card absolute w-64 h-32 flex flex-col items-center justify-center gap-3">
          <Wand2 className="w-6 h-6 text-violet-400" />
          <span className="text-sm font-medium tracking-widest text-white/80">PROMPT ENHANCEMENT</span>
        </FloatingCard>
        
        <FloatingCard className="hero-card absolute w-48 h-48 flex flex-col items-center justify-center gap-3">
          <Video className="w-8 h-8 text-cyan-400" />
          <span className="text-sm font-medium tracking-widest text-white/80">CINEMATIC</span>
        </FloatingCard>

        <FloatingCard className="hero-card absolute w-40 h-56 flex flex-col items-center justify-center gap-3">
          <MonitorPlay className="w-6 h-6 text-blue-400" />
          <span className="text-sm font-medium tracking-widest text-white/80">9:16</span>
        </FloatingCard>

        <FloatingCard className="hero-card absolute w-56 h-40 flex flex-col items-center justify-center gap-3">
          <Sparkles className="w-6 h-6 text-fuchsia-400" />
          <span className="text-sm font-medium tracking-widest text-white/80">AI READY</span>
        </FloatingCard>
      </div>

      {/* Main Typography */}
      <div ref={textRef} className="relative z-10 flex flex-col items-center text-center px-6 mt-[-20vh]">
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tighter leading-[1.1] max-w-5xl">
          TURN YOUR IDEAS INTO <br/>
          <span className="cinematic-text-gradient">CINEMATIC VIDEOS</span>.
        </h1>
        <p className="mt-8 text-lg md:text-xl text-white/60 max-w-2xl font-light tracking-wide">
          Describe a scene and let AI bring it to life.
        </p>
      </div>
    </section>
  );
}
