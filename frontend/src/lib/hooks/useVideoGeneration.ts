import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { videosApi } from '../api/videos';
import { TERMINAL_STATUSES, VideoGenerateRequest } from '../types/video';

export function useVideoGeneration(videoId?: string) {
  const queryClient = useQueryClient();

  // Query to poll status when a videoId is provided and not terminal
  const statusQuery = useQuery({
    queryKey: ['video', videoId],
    queryFn: () => videosApi.getStatus(videoId!),
    enabled: !!videoId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      // Stop polling if the status is terminal
      if (status && TERMINAL_STATUSES.includes(status)) {
        return false;
      }
      return 3000; // Poll every 3 seconds
    },
  });

  // Mutation to start generation
  const generateMutation = useMutation({
    mutationFn: (request: VideoGenerateRequest) => videosApi.generate(request),
    onSuccess: (data) => {
      // Optimistically add to cache
      queryClient.setQueryData(['video', data.id], data);
    },
  });

  return {
    statusQuery,
    generateMutation,
  };
}
