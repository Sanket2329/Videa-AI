import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { videosApi } from '../api/videos';

export function useVideoHistory() {
  const queryClient = useQueryClient();

  const historyQuery = useQuery({
    queryKey: ['videoHistory'],
    queryFn: () => videosApi.getHistory(),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => videosApi.delete(id),
    onSuccess: (_, deletedId) => {
      // Invalidate history
      queryClient.invalidateQueries({ queryKey: ['videoHistory'] });
      // Clear the specific video cache
      queryClient.removeQueries({ queryKey: ['video', deletedId] });
    },
  });

  return {
    historyQuery,
    deleteMutation,
  };
}
