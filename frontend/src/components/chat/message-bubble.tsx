"use client"

import { Card } from "@/components/ui/card"
import { Citation } from "@/types"
import { User, Bot, FileText } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { useDocument } from "@/contexts/document-context"

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
  const { setSelectedDocument } = useDocument()

  const handleCitationClick = (citation: Citation) => {
    // Find the PDF filename from the subset
    // Format: "SUBSET-026-3 v360" -> "SUBSET-026-3 v360.pdf"
    const filename = `${citation.subset}.pdf`
    const page = citation.page || 1
    setSelectedDocument(filename, page)
  }

  // Parse inline citations and make them clickable
  const handleInlineCitationClick = (citationText: string) => {
    // Extract page number and subset from citation text
    // Format: [Subset-026, §3.4.2, p.42, ¶5]
    const pageMatch = citationText.match(/p\.(\d+)/)
    const subsetMatch = citationText.match(/(Subset-[\w-]+)/)

    if (subsetMatch) {
      const page = pageMatch ? parseInt(pageMatch[1]) : 1
      const filename = `${subsetMatch[1]}.pdf`
      setSelectedDocument(filename, page)
    }
  }

  // Component to render content with clickable inline citations
  const ContentWithCitations = ({ content }: { content: string }) => {
    // Pattern to match citations like [Subset-026, §3.4.2, p.42, ¶5]
    const citationPattern = /\[(Subset-[^\]]+)\]/g
    const parts: (string | JSX.Element)[] = []
    let lastIndex = 0
    let match

    while ((match = citationPattern.exec(content)) !== null) {
      // Add text before citation
      if (match.index > lastIndex) {
        parts.push(content.substring(lastIndex, match.index))
      }

      // Add clickable citation
      const citationText = match[1]
      parts.push(
        <button
          key={match.index}
          onClick={() => handleInlineCitationClick(match[0])}
          className="inline-flex items-center gap-0.5 rounded bg-primary/10 px-1.5 py-0.5 text-xs font-medium text-primary hover:bg-primary/20 transition-colors cursor-pointer border border-primary/20"
          title="Click to view in PDF"
        >
          [{citationText}]
        </button>
      )

      lastIndex = match.index + match[0].length
    }

    // Add remaining text
    if (lastIndex < content.length) {
      parts.push(content.substring(lastIndex))
    }

    // If no citations found, return markdown as before
    if (parts.length === 0) {
      return (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      )
    }

    return (
      <div className="prose prose-sm dark:prose-invert max-w-none whitespace-pre-wrap">
        {parts}
      </div>
    )
  }

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
            <ContentWithCitations content={message.content} />
          </div>
        </Card>

        {/* Citations */}
        {!isUser && message.citations && message.citations.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {message.citations.map((citation, idx) => (
              <button
                key={idx}
                className="flex items-center gap-1 rounded-md border bg-card px-2 py-1 text-xs hover:bg-accent transition-colors cursor-pointer"
                onClick={() => handleCitationClick(citation)}
                title={`Open ${citation.subset} at page ${citation.page || 1}`}
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
