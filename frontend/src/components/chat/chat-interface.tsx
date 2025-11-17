"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { StyleSelector } from "./style-selector"
import { MessageList } from "./message-list"
import { Send, Loader2 } from "lucide-react"
import { ConversationStyle } from "@/types"

export function ChatInterface() {
  const [message, setMessage] = useState("")
  const [style, setStyle] = useState<ConversationStyle>("professional")
  const [isLoading, setIsLoading] = useState(false)
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
    setMessage("")
    setIsLoading(true)

    // Simulate API call - will be replaced with actual API integration
    setTimeout(() => {
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: 'This is a placeholder response. In Phase 2, this will be connected to the RAG system with real ETCS documentation citations.',
        citations: [
          {
            subset: 'Subset-026',
            section: '3.4.2',
            page: 42,
            paragraph: 5,
            text: 'Example citation text from the document',
            document_id: 'doc-1'
          }
        ]
      }
      setMessages(prev => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1500)
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
