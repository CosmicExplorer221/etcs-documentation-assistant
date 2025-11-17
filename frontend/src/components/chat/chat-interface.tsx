"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { StyleSelector } from "./style-selector"
import { MessageList } from "./message-list"
import { Send, Loader2 } from "lucide-react"
import { ConversationStyle } from "@/types"
import { apiClient } from "@/lib/api-client"

export function ChatInterface() {
  const [message, setMessage] = useState("")
  const [style, setStyle] = useState<ConversationStyle>("professional")
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Array<{
    id: string
    role: 'user' | 'assistant'
    content: string
    citations?: any[]
  }>>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your ETCS Documentation Assistant. I can help you understand ETCS technical specifications, answer questions about railway standards, and provide detailed citations from official documentation. How can I assist you today?',
    }
  ])

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading) return

    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: message,
    }

    setMessages(prev => [...prev, userMessage])
    const userQuery = message
    setMessage("")
    setIsLoading(true)

    try {
      // Call real RAG API (Phase 2)
      const response = await apiClient.sendMessage(conversationId, userQuery, style)

      // Save conversation ID for subsequent messages
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id)
      }

      const assistantMessage = {
        id: response.message.id,
        role: 'assistant' as const,
        content: response.message.content,
        citations: response.citations || []
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: 'Sorry, I encountered an error while processing your request. Please make sure the backend server is running and try again.',
        citations: []
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex h-full flex-col">
      {/* Header with Style Selector */}
      <div className="border-b p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Chat</h2>
          <StyleSelector value={style} onChange={setStyle} />
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} />
      </div>

      {/* Input Area */}
      <div className="border-t p-4">
        <div className="flex gap-2">
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me anything about ETCS documentation..."
            className="min-h-[80px] resize-none"
            disabled={isLoading}
          />
          <Button
            onClick={handleSendMessage}
            disabled={!message.trim() || isLoading}
            size="icon"
            className="h-[80px] w-12"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
        <p className="mt-2 text-xs text-muted-foreground">
          Press Enter to send, Shift+Enter for new line
        </p>
      </div>
    </div>
  )
}
