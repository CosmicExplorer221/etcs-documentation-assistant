"use client"

import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { MessageSquare, Plus, Bookmark, History, FileText } from "lucide-react"
import { useState } from "react"

export function Sidebar() {
  const [activeTab, setActiveTab] = useState<'conversations' | 'bookmarks' | 'documents'>('conversations')

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
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Recent Conversations</p>
              {/* Placeholder for conversation list */}
              <div className="flex items-center gap-3 rounded-lg border p-3 hover:bg-accent cursor-pointer">
                <MessageSquare className="h-4 w-4 text-muted-foreground" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">ETCS Level 2 System Overview</p>
                  <p className="text-xs text-muted-foreground truncate">What are the main components...</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'bookmarks' && (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Your Bookmarks</p>
              <p className="text-xs text-muted-foreground">No bookmarks yet</p>
            </div>
          )}

          {activeTab === 'documents' && (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Available Documents</p>
              <div className="space-y-1">
                <div className="flex items-center gap-2 rounded-lg border p-2 text-sm hover:bg-accent cursor-pointer">
                  <FileText className="h-4 w-4 text-primary" />
                  <span className="truncate">Subset-026 v4.0</span>
                </div>
                <div className="flex items-center gap-2 rounded-lg border p-2 text-sm hover:bg-accent cursor-pointer">
                  <FileText className="h-4 w-4 text-primary" />
                  <span className="truncate">Subset-023 v3.6</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>
    </aside>
  )
}
