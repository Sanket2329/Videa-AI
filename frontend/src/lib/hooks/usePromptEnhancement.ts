import { useMutation } from '@tanstack/react-query';
import { promptsApi } from '../api/prompts';
import { EnhancePromptRequest } from '../types/prompt';

export function usePromptEnhancement() {
  return useMutation({
    mutationFn: (request: EnhancePromptRequest) => promptsApi.enhancePrompt(request),
  });
}
