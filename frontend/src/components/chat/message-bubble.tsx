"use client"

import { Card } from "@/components/ui/card"
import { Citation } from "@/types"
import { User, Bot, FileText } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  citations?: Citation[]
}

interface MessageBubbleProps {
  message: Message
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <Bot className="h-4 w-4" />
        </div>
      )}

      <div className={`flex max-w-[80%] flex-col gap-2 ${isUser ? 'items-end' : 'items-start'}`}>
        <Card className={`p-4 ${isUser ? 'bg-primary text-primary-foreground' : 'bg-card'}`}>
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </div>
        </Card>

        {/* Citations */}
        {!isUser && message.citations && message.citations.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {message.citations.map((citation, idx) => (
              <button
                key={idx}
                className="flex items-center gap-1 rounded-md border bg-card px-2 py-1 text-xs hover:bg-accent transition-colors"
                onClick={() => {
                  // TODO: Scroll to citation in document viewer
                  console.log('Navigate to citation:', citation)
                }}
              >
                <FileText className="h-3 w-3 text-primary" />
                <span className="font-medium">{citation.subset}</span>
                {citation.section && (
                  <>
                    <span className="text-muted-foreground">§</span>
                    <span>{citation.section}</span>
                  </>
                )}
                {citation.page && (
                  <>
                    <span className="text-muted-foreground">, p.</span>
                    <span>{citation.page}</span>
                  </>
                )}
                {citation.paragraph && (
                  <>
                    <span className="text-muted-foreground">, ¶</span>
                    <span>{citation.paragraph}</span>
                  </>
                )}
              </button>
            ))}
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-muted">
          <User className="h-4 w-4" />
        </div>
      )}
    </div>
  )
}
