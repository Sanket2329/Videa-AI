/** Prompt enhancement types. */

export interface EnhancePromptRequest {
  prompt: string;
  style: string;
}

export interface EnhancedPrompt {
  original_prompt: string;
  enhanced_prompt: string;
  negative_prompt: string;
  camera: string;
  lighting: string;
  style: string;
  motion: string;
}
