// User types
export interface User {
  id: string
  email: string
  full_name: string
  created_at: string
  updated_at: string
}

// Conversation styles
export type ConversationStyle =
  | 'professional'
  | 'entry-level'
  | 'newbie'
  | 'ten-year-old'
  | 'detailed'
  | 'concise'
  | 'funny'
  | 'academic'
  | 'practical'

export const CONVERSATION_STYLES: { value: ConversationStyle; label: string; description: string }[] = [
  {
    value: 'professional',
    label: 'Professional',
    description: 'Technical language for experienced railway engineers',
  },
  {
    value: 'entry-level',
    label: 'Entry-Level',
    description: 'Clear explanations for junior engineers',
  },
  {
    value: 'newbie',
    label: 'Newbie',
    description: 'Simple terms for those new to ETCS',
  },
  {
    value: 'ten-year-old',
    label: '10-Year-Old',
    description: 'Very simple language with analogies',
  },
  {
    value: 'detailed',
    label: 'Detailed',
    description: 'In-depth technical explanations',
  },
  {
    value: 'concise',
    label: 'Concise',
    description: 'Brief, to-the-point answers',
  },
  {
    value: 'funny',
    label: 'Funny',
    description: 'Technical info with humor',
  },
  {
    value: 'academic',
    label: 'Academic',
    description: 'Formal, research-oriented style',
  },
  {
    value: 'practical',
    label: 'Practical',
    description: 'Focus on real-world application',
  },
]

// Citation types
export interface Citation {
  subset: string
  section?: string
  paragraph?: string
  page?: number
  line?: number
  text: string
  document_id: string
}

// Message types
export interface Message {
  id: string
  conversation_id: string
  role: 'user' | 'assistant'
  content: string
  citations?: Citation[]
  created_at: string
}

// Conversation types
export interface Conversation {
  id: string
  user_id: string
  title: string
  style: ConversationStyle
  created_at: string
  updated_at: string
  messages?: Message[]
}

// Document types
export interface Document {
  id: string
  title: string
  subset_number: string
  version: string
  file_path: string
  page_count: number
  uploaded_at: string
  processed: boolean
}

// Bookmark types
export interface Bookmark {
  id: string
  user_id: string
  conversation_id: string
  message_id: string
  note?: string
  created_at: string
  conversation?: Conversation
  message?: Message
}

// Search result types
export interface SearchResult {
  document_id: string
  document_title: string
  subset: string
  section: string
  content: string
  page: number
  score: number
}

// API response types
export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface ApiError {
  detail: string
  status_code: number
}

// Chat message payload
export interface ChatMessagePayload {
  conversation_id: string | null
  message: string
  style: ConversationStyle
}

// Chat response
export interface ChatResponse {
  conversation_id: string
  message: Message
  citations: Citation[]
}
