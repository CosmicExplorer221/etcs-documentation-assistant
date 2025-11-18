"use client"

import { Card } from "@/components/ui/card"
import { Citation } from "@/types"
import { User, Bot, FileText, Info } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { useDocument } from "@/contexts/document-context"
import * as Tooltip from "@radix-ui/react-tooltip"

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

  // Find citation object from citation text
  const findCitationByText = (citationText: string): Citation | undefined => {
    if (!message.citations) return undefined

    // Extract subset and page from citation text
    const subsetMatch = citationText.match(/(?:Subset-[\w-]+(?:\s+v\d+)?)/i)
    const pageMatch = citationText.match(/p\.(\d+)/)

    if (!subsetMatch) return undefined

    const subset = subsetMatch[0]
    const page = pageMatch ? parseInt(pageMatch[1]) : undefined

    // Find matching citation in the citations array
    return message.citations.find(c => {
      const subsetMatches = c.subset === subset
      const pageMatches = !page || c.page === page
      return subsetMatches && pageMatches
    })
  }

  // Parse inline citations and make them clickable
  const handleInlineCitationClick = (citationText: string) => {
    // Extract page number and subset from citation text
    const pageMatch = citationText.match(/p\.(\d+)/)
    const subsetMatch = citationText.match(/(?:Subset-[\w-]+(?:\s+v\d+)?)/i)

    if (subsetMatch) {
      const page = pageMatch ? parseInt(pageMatch[1]) : 1
      const filename = `${subsetMatch[0]}.pdf`
      setSelectedDocument(filename, page)
    }
  }

  // Component to render content with clickable inline citations
  const ContentWithCitations = ({ content }: { content: string }) => {
    // Broader pattern to match various citation formats
    // Matches: [Subset-026, ...], [Subset-026-3 v360, ...], etc.
    const citationPattern = /\[((?:Subset-[\w-]+(?:\s+v\d+)?)[^\]]*)\]/gi
    const parts: (string | JSX.Element)[] = []
    let lastIndex = 0
    let match
    let citationIndex = 0

    while ((match = citationPattern.exec(content)) !== null) {
      // Add text before citation
      if (match.index > lastIndex) {
        const textBefore = content.substring(lastIndex, match.index)
        parts.push(<span key={`text-${lastIndex}`}>{textBefore}</span>)
      }

      // Find the full citation object to get the referenced text
      const citationText = match[1]
      const citationObj = findCitationByText(match[0])

      // Add clickable citation with tooltip
      parts.push(
        <Tooltip.Provider key={`citation-${citationIndex}`}>
          <Tooltip.Root delayDuration={200}>
            <Tooltip.Trigger asChild>
              <button
                onClick={() => handleInlineCitationClick(match[0])}
                className="inline-flex items-center gap-1 rounded bg-amber-100 dark:bg-amber-900/30 px-2 py-0.5 text-xs font-medium text-amber-900 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-amber-900/50 transition-colors cursor-pointer border border-amber-300 dark:border-amber-700 shadow-sm"
              >
                <Info className="h-3 w-3" />
                [{citationText}]
              </button>
            </Tooltip.Trigger>
            {citationObj && citationObj.text && (
              <Tooltip.Portal>
                <Tooltip.Content
                  className="max-w-md rounded-lg border bg-popover px-4 py-3 text-sm text-popover-foreground shadow-lg z-50"
                  sideOffset={5}
                >
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-xs font-semibold text-primary">
                      <FileText className="h-3 w-3" />
                      <span>{citationObj.subset}</span>
                      {citationObj.page && <span>• Page {citationObj.page}</span>}
                    </div>
                    <p className="text-xs leading-relaxed italic border-l-2 border-primary/30 pl-3">
                      "{citationObj.text}"
                    </p>
                    <p className="text-[10px] text-muted-foreground">
                      Click citation to view in PDF
                    </p>
                  </div>
                  <Tooltip.Arrow className="fill-popover" />
                </Tooltip.Content>
              </Tooltip.Portal>
            )}
          </Tooltip.Root>
        </Tooltip.Provider>
      )

      lastIndex = match.index + match[0].length
      citationIndex++
    }

    // Add remaining text
    if (lastIndex < content.length) {
      const remainingText = content.substring(lastIndex)
      parts.push(<span key={`text-${lastIndex}`}>{remainingText}</span>)
    }

    // If no citations found, return markdown as before
    if (citationIndex === 0) {
      return (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      )
    }

    return (
      <div className="prose prose-sm dark:prose-invert max-w-none">
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
