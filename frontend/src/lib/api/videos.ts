import { VideoGenerateRequest, VideoGeneration } from '../types/video';
import { apiClient, unwrapResponse } from './client';

export const videosApi = {
  /** Submit a new video generation request */
  generate: (request: VideoGenerateRequest): Promise<VideoGeneration> => {
    return unwrapResponse(
      apiClient.post<any>('/videos/generate', request)
    );
  },

  /** Get the status of a specific video generation */
  getStatus: (id: string): Promise<VideoGeneration> => {
    return unwrapResponse(
      apiClient.get<any>(`/videos/${id}`)
    );
  },

  /** Get the recent generation history */
  getHistory: (): Promise<VideoGeneration[]> => {
    return unwrapResponse(
      apiClient.get<any>('/videos/history')
    );
  },

  /** Delete a generation record */
  delete: (id: string): Promise<{ deleted: boolean }> => {
    return unwrapResponse(
      apiClient.delete<any>(`/videos/${id}`)
    );
  },
};
