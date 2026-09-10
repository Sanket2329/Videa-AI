'use client';

import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export function useTilt(maxTilt: number = 10, scale: number = 1.02) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // Detect if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = element.getBoundingClientRect();
      // Calculate cursor position relative to the center of the element (-1 to 1)
      const x = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
      const y = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);

      gsap.to(element, {
        rotateX: -y * maxTilt,
        rotateY: x * maxTilt,
        scale: scale,
        transformPerspective: 1000,
        ease: 'power3.out',
        duration: 0.5,
      });
    };

    const handleMouseLeave = () => {
      gsap.to(element, {
        rotateX: 0,
        rotateY: 0,
        scale: 1,
        ease: 'power3.out',
        duration: 0.7,
      });
    };

    element.addEventListener('mousemove', handleMouseMove);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mousemove', handleMouseMove);
      element.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [maxTilt, scale]);

  return ref;
}
