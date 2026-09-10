'use client';

import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, useScroll, useMotionValueEvent } from 'framer-motion';
import { cn } from '@/lib/utils';
import { useAuth } from '@/context/AuthContext';

export function Navbar() {
  const pathname = usePathname();
  const { scrollY } = useScroll();
  const [scrolled, setScrolled] = useState(false);
  const { user, logout } = useAuth();

  useMotionValueEvent(scrollY, "change", (latest) => {
    setScrolled(latest > 50);
  });

  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      className={cn(
        "fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 transition-all duration-500",
        scrolled ? "bg-black/40 backdrop-blur-md border-b border-white/5 py-4" : "bg-transparent py-6"
      )}
    >
      <div className="flex items-center gap-4">
        <Link href="/" className="text-sm font-bold tracking-[0.2em] text-white/90 hover:text-white transition-colors">
          AI VIDEO STUDIO
        </Link>
        <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10">
          <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
          <span className="text-[10px] font-medium tracking-wider text-white/60">AI ENGINE READY</span>
        </div>
      </div>

      <nav className="flex items-center gap-6">
        <Link 
          href="/" 
          className={cn(
            "text-xs font-medium tracking-widest uppercase transition-all hover:text-white",
            pathname === '/' ? "text-white" : "text-white/40"
          )}
        >
          Create
        </Link>
        {user && (
          <Link 
            href="/history" 
            className={cn(
              "text-xs font-medium tracking-widest uppercase transition-all hover:text-white",
              pathname === '/history' ? "text-white" : "text-white/40"
            )}
          >
            History
          </Link>
        )}
        {user ? (
          <button
            onClick={logout}
            className="text-xs font-medium tracking-widest uppercase transition-all text-white/40 hover:text-white"
          >
            Logout
          </button>
        ) : (
          <Link
            href="/login"
            className="text-xs font-medium tracking-widest uppercase transition-all text-white/40 hover:text-white"
          >
            Login
          </Link>
        )}
      </nav>
    </motion.header>
  );
}
