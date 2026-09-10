/** Video generation types aligned with backend schemas. */

export type VideoStatus = 'queued' | 'processing' | 'completed' | 'failed' | 'timeout' | 'cancelled';
export type VideoStyle = 'cinematic' | 'realistic' | 'anime' | '3d' | 'product';
export type AspectRatio = '16:9' | '9:16' | '1:1';
export type Duration = 5 | 10;

export interface VideoGeneration {
  id: string;
  originalPrompt: string;
  enhancedPrompt?: string | null;
  negativePrompt?: string | null;
  style: VideoStyle;
  aspectRatio: AspectRatio;
  duration: Duration;
  provider: string;
  model: string;
  providerJobId?: string | null;
  status: VideoStatus;
  videoUrl?: string | null;
  thumbnailUrl?: string | null;
  errorMessage?: string | null;
  createdAt: string;
  updatedAt: string;
  completedAt?: string | null;
}

export interface VideoGenerateRequest {
  prompt: string;
  enhanced_prompt?: string | null;
  negative_prompt?: string | null;
  style: VideoStyle;
  aspect_ratio: AspectRatio;
  duration: Duration;
}

/** Maps for UI display labels */
export const STYLE_LABELS: Record<VideoStyle, string> = {
  cinematic: 'Cinematic',
  realistic: 'Realistic',
  anime: 'Anime',
  '3d': '3D',
  product: 'Product Commercial',
};

export const ASPECT_RATIO_LABELS: Record<AspectRatio, string> = {
  '16:9': '16:9 Landscape',
  '9:16': '9:16 Portrait',
  '1:1': '1:1 Square',
};

export const DURATION_LABELS: Record<Duration, string> = {
  5: '5 seconds',
  10: '10 seconds',
};

export const TERMINAL_STATUSES: VideoStatus[] = ['completed', 'failed', 'timeout', 'cancelled'];
