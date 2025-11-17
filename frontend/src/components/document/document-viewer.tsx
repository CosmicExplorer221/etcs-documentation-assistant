"use client"

import { Card } from "@/components/ui/card"
import { FileText, ZoomIn, ZoomOut, Download, ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useState, useEffect } from "react"
import { Document, Page, pdfjs } from 'react-pdf'
import { useDocument } from "@/contexts/document-context"
import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import 'react-pdf/dist/esm/Page/TextLayer.css'

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export function DocumentViewer() {
  const { selectedDocument, selectedPage } = useDocument()
  const [zoom, setZoom] = useState(1.0)
  const [numPages, setNumPages] = useState<number>(0)
  const [pageNumber, setPageNumber] = useState<number>(1)

  // When selectedPage changes from citation click, scroll to that page
  useEffect(() => {
    if (selectedPage) {
      setPageNumber(selectedPage)
    }
  }, [selectedPage])

  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages)
    // If a specific page was requested, go to it
    if (selectedPage) {
      setPageNumber(selectedPage)
    } else {
      setPageNumber(1)
    }
  }

  const changePage = (offset: number) => {
    setPageNumber(prevPageNumber => {
      const newPage = prevPageNumber + offset
      return Math.min(Math.max(1, newPage), numPages)
    })
  }

  const previousPage = () => changePage(-1)
  const nextPage = () => changePage(1)

  const handleDownload = () => {
    if (selectedDocument) {
      const url = `${API_BASE_URL}/documents/pdf/${selectedDocument}`
      window.open(url, '_blank')
    }
  }

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="border-b p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold">Document Viewer</h2>
            {selectedDocument && (
              <span className="text-sm text-muted-foreground">
                {selectedDocument}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => setZoom(Math.max(0.5, zoom - 0.1))}
              disabled={!selectedDocument}
            >
              <ZoomOut className="h-4 w-4" />
            </Button>
            <span className="text-sm text-muted-foreground w-16 text-center">
              {Math.round(zoom * 100)}%
            </span>
            <Button
              variant="outline"
              size="icon"
              onClick={() => setZoom(Math.min(2.0, zoom + 0.1))}
              disabled={!selectedDocument}
            >
              <ZoomIn className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="icon"
              disabled={!selectedDocument}
              onClick={handleDownload}
            >
              <Download className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Document Display Area */}
      <div className="flex-1 overflow-auto bg-muted/20 p-4">
        {selectedDocument ? (
          <div className="mx-auto" style={{ maxWidth: `${800 * zoom}px` }}>
            <Document
              file={`${API_BASE_URL}/documents/pdf/${selectedDocument}`}
              onLoadSuccess={onDocumentLoadSuccess}
              loading={
                <div className="flex h-96 items-center justify-center">
                  <div className="text-center">
                    <FileText className="mx-auto h-16 w-16 animate-pulse text-muted-foreground" />
                    <p className="mt-4 text-sm text-muted-foreground">Loading PDF...</p>
                  </div>
                </div>
              }
              error={
                <div className="flex h-96 items-center justify-center">
                  <div className="text-center">
                    <FileText className="mx-auto h-16 w-16 text-destructive" />
                    <p className="mt-4 text-sm text-destructive">Failed to load PDF</p>
                  </div>
                </div>
              }
            >
              <Page
                pageNumber={pageNumber}
                scale={zoom}
                renderTextLayer={true}
                renderAnnotationLayer={true}
              />
            </Document>

            {/* Page Navigation */}
            {numPages > 0 && (
              <div className="mt-4 flex items-center justify-center gap-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={previousPage}
                  disabled={pageNumber <= 1}
                >
                  <ChevronLeft className="h-4 w-4 mr-1" />
                  Previous
                </Button>
                <span className="text-sm text-muted-foreground">
                  Page {pageNumber} of {numPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={nextPage}
                  disabled={pageNumber >= numPages}
                >
                  Next
                  <ChevronRight className="h-4 w-4 ml-1" />
                </Button>
              </div>
            )}
          </div>
        ) : (
          <div className="flex h-full items-center justify-center">
            <div className="text-center">
              <FileText className="mx-auto h-16 w-16 text-muted-foreground" />
              <h3 className="mt-4 text-lg font-semibold">No Document Selected</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                Click on citations or documents to view them here
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
