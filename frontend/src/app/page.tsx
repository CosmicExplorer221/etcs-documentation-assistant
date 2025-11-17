"use client"

import { MainLayout } from "@/components/layout/main-layout"
import { ChatInterface } from "@/components/chat/chat-interface"
import { DocumentViewer } from "@/components/document/document-viewer"

export default function HomePage() {
  return (
    <MainLayout>
      <div className="flex h-full w-full">
        {/* Chat Interface - Left Side */}
        <div className="flex-1 border-r">
          <ChatInterface />
        </div>

        {/* Document Viewer - Right Side */}
        <div className="w-1/2">
          <DocumentViewer />
        </div>
      </div>
    </MainLayout>
  )
}
