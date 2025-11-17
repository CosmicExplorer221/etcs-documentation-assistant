"use client"

import { ScrollArea } from "@/components/ui/scroll-area"
import { MessageBubble } from "./message-bubble"
import { useEffect, useRef } from "react"

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  citations?: any[]
}

interface MessageListProps {
  messages: Message[]
}

export function MessageList({ messages }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  return (
    <ScrollArea className="h-full">
      <div ref={scrollRef} className="flex flex-col gap-4 p-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </div>
    </ScrollArea>
  )
}
