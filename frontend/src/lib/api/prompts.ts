import { EnhancePromptRequest, EnhancedPrompt } from '../types/prompt';
import { apiClient, unwrapResponse } from './client';

export const promptsApi = {
  /** Enhance a user prompt using the LLM */
  enhancePrompt: (request: EnhancePromptRequest): Promise<EnhancedPrompt> => {
    return unwrapResponse(
      apiClient.post<any>('/prompts/enhance', request)
    );
  },
};
