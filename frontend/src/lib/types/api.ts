/** Consistent API response wrapper matching backend's ApiResponse schema. */
export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: { code: string; message: string } | null;
}
