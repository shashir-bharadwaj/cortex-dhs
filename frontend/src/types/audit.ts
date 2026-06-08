export interface AuditLog {
  id: number;
  user_id?: number;
  action: string;
  model: string;
  object_id?: number;
  before_data?: string;
  after_data?: string;
  timestamp: string;
}