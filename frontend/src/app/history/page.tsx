'use client';

import { useVideoHistory } from '@/lib/hooks/useVideoHistory';
import { ScrollGallery } from '@/components/history/ScrollGallery';

export default function HistoryPage() {
  const { historyQuery } = useVideoHistory();

  if (historyQuery.isLoading) {
    return (
      <div className="w-full h-screen flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 rounded-full border-2 border-t-violet-500 border-white/10 animate-spin" />
          <span className="text-xs font-bold tracking-[0.2em] text-white/40 uppercase">Loading creations...</span>
        </div>
      </div>
    );
  }

  if (historyQuery.isError) {
    return (
      <div className="w-full h-screen flex items-center justify-center text-red-400">
        <span className="text-xs font-bold tracking-[0.2em] uppercase">Failed to load history</span>
      </div>
    );
  }

  return (
    <div className="w-full bg-[#050505]">
      <ScrollGallery videos={historyQuery.data || []} />
    </div>
  );
}
