"use client"

import { createContext, useContext, useState, ReactNode } from 'react'

interface DocumentContextType {
  selectedDocument: string | null
  selectedPage: number | null
  setSelectedDocument: (filename: string | null, page?: number) => void
}

const DocumentContext = createContext<DocumentContextType | undefined>(undefined)

export function DocumentProvider({ children }: { children: ReactNode }) {
  const [selectedDocument, setDocument] = useState<string | null>(null)
  const [selectedPage, setPage] = useState<number | null>(null)

  const setSelectedDocument = (filename: string | null, page?: number) => {
    setDocument(filename)
    setPage(page || null)
  }

  return (
    <DocumentContext.Provider value={{ selectedDocument, selectedPage, setSelectedDocument }}>
      {children}
    </DocumentContext.Provider>
  )
}

export function useDocument() {
  const context = useContext(DocumentContext)
  if (context === undefined) {
    throw new Error('useDocument must be used within a DocumentProvider')
  }
  return context
}
