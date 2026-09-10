"use client";

import { cn } from "@/lib/utils";
import { useTilt } from "@/hooks/useTilt";
import { AspectRatio, VideoDuration } from "@/lib/api/videos";

function CardOption<T>({ 
  selected, 
  onClick, 
  label, 
  icon,
  disabled
}: { 
  selected: boolean; 
  onClick?: () => void; 
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
}) {
  const tiltRef = useTilt(10, 1.05);

  return (
    <button
      ref={tiltRef as any}
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "relative flex flex-col items-center justify-center p-4 rounded-2xl transition-all duration-300",
        selected 
          ? "bg-white/10 border-white/30 shadow-[0_0_20px_rgba(255,255,255,0.05)]" 
          : "bg-white/5 border-white/5 hover:bg-white/10 hover:border-white/10",
        "border backdrop-blur-md",
        disabled && "cursor-not-allowed opacity-80 hover:bg-white/10"
      )}
    >
      {selected && (
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-violet-500/20 to-transparent pointer-events-none" />
      )}
      {icon && <div className={cn("mb-2 transition-colors", selected ? "text-violet-400" : "text-white/40")}>{icon}</div>}
      <span className={cn(
        "text-xs font-bold tracking-widest uppercase transition-colors",
        selected ? "text-white" : "text-white/60"
      )}>
        {label}
      </span>
    </button>
  );
}

export function ConfigCards({
  style,
  setStyle,
}: {
  style: string;
  setStyle: (s: string) => void;
  aspectRatio: AspectRatio;
  setAspectRatio: (a: AspectRatio) => void;
  duration: VideoDuration;
  setDuration: (d: VideoDuration) => void;
}) {
  const styles = [
    { label: "Cinematic", value: "cinematic" },
    { label: "Realistic", value: "realistic" },
    { label: "Anime", value: "anime" },
    { label: "3D Render", value: "3d-render" },
    { label: "Commercial", value: "commercial" }
  ];

  return (
    <div className="w-full space-y-12">
      <div className="space-y-4">
        <h3 className="text-xs font-bold tracking-[0.2em] text-white/40 uppercase pl-2">Style</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {styles.map(s => (
            <CardOption key={s.value} selected={style === s.value} onClick={() => setStyle(s.value)} label={s.label} />
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div className="space-y-4">
          <h3 className="text-xs font-bold tracking-[0.2em] text-white/40 uppercase pl-2">Aspect Ratio</h3>
          <div className="grid grid-cols-1 gap-4">
            <CardOption 
              selected={true} 
              disabled={true}
              label="16:9 (DEFAULT)" 
              icon={<div className="w-8 h-4.5 border-2 border-current rounded-sm" />} 
            />
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-xs font-bold tracking-[0.2em] text-white/40 uppercase pl-2">Duration</h3>
          <div className="grid grid-cols-1 gap-4">
            <CardOption 
              selected={true} 
              disabled={true}
              label="3 SEC (DEFAULT)" 
            />
          </div>
        </div>
      </div>
    </div>
  );
}
