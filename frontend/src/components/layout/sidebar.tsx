"use client"

import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { MessageSquare, Plus, Bookmark, History, FileText } from "lucide-react"
import { useState, useEffect } from "react"
import { apiClient } from "@/lib/api-client"

export function Sidebar() {
  const [activeTab, setActiveTab] = useState<'conversations' | 'bookmarks' | 'documents'>('conversations')
  const [documents, setDocuments] = useState<any[]>([])
  const [isLoadingDocs, setIsLoadingDocs] = useState(false)

  // Fetch documents when Documents tab is active
  useEffect(() => {
    if (activeTab === 'documents' && documents.length === 0) {
      fetchDocuments()
    }
  }, [activeTab])

  const fetchDocuments = async () => {
    try {
      setIsLoadingDocs(true)
      const docs = await apiClient.getDocuments()
      setDocuments(docs)
    } catch (error) {
      console.error('Error fetching documents:', error)
    } finally {
      setIsLoadingDocs(false)
    }
  }

  return (
    <aside className="flex w-80 flex-col border-r bg-card">
      {/* New Conversation Button */}
      <div className="border-b p-4">
        <Button className="w-full" size="lg">
          <Plus className="mr-2 h-4 w-4" />
          New Conversation
        </Button>
      </div>

      {/* Tabs */}
      <div className="flex border-b">
        <button
          onClick={() => setActiveTab('conversations')}
          className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors ${
            activeTab === 'conversations'
              ? 'border-b-2 border-primary text-primary'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <MessageSquare className="h-4 w-4" />
          Chats
        </button>
        <button
          onClick={() => setActiveTab('bookmarks')}
          className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors ${
            activeTab === 'bookmarks'
              ? 'border-b-2 border-primary text-primary'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <Bookmark className="h-4 w-4" />
          Saved
        </button>
        <button
          onClick={() => setActiveTab('documents')}
          className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors ${
            activeTab === 'documents'
              ? 'border-b-2 border-primary text-primary'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <FileText className="h-4 w-4" />
          Docs
        </button>
      </div>

      {/* Content */}
      <ScrollArea className="flex-1">
        <div className="p-4">
          {activeTab === 'conversations' && (
            <div className="space-y-3">
              <p className="text-sm text-muted-foreground">Active Session</p>
              <div className="rounded-lg border border-dashed p-4 text-center">
                <MessageSquare className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                <p className="text-sm font-medium mb-1">Demo Mode</p>
                <p className="text-xs text-muted-foreground">
                  Start chatting! Your conversation will be active during this session.
                  (History saved temporarily)
                </p>
              </div>
            </div>
          )}

          {activeTab === 'bookmarks' && (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Bookmarks</p>
              <div className="rounded-lg border border-dashed p-4 text-center">
                <Bookmark className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                <p className="text-xs text-muted-foreground">
                  Bookmark feature coming in Phase 3
                </p>
              </div>
            </div>
          )}

          {activeTab === 'documents' && (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">ETCS Documents</p>
              {isLoadingDocs ? (
                <div className="rounded-lg border border-dashed p-4 text-center">
                  <p className="text-xs text-muted-foreground">Loading documents...</p>
                </div>
              ) : documents.length > 0 ? (
                <div className="space-y-1">
                  {documents.map((doc, idx) => (
                    <div key={idx} className="flex items-center gap-2 rounded-lg border p-2 text-sm hover:bg-accent cursor-pointer">
                      <FileText className="h-4 w-4 text-primary" />
                      <span className="truncate">{doc.subset}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="rounded-lg border border-dashed p-4 text-center">
                  <FileText className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                  <p className="text-xs text-muted-foreground">
                    No documents found. Run init_documents.py to load PDFs.
                  </p>
                </div>
              )}
              <p className="text-xs text-muted-foreground pt-2">
                {documents.length} document{documents.length !== 1 ? 's' : ''} loaded
              </p>
            </div>
          )}
        </div>
      </ScrollArea>
    </aside>
  )
}
