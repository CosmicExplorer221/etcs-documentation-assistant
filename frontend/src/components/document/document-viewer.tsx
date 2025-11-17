"use client"

import { Card } from "@/components/ui/card"
import { FileText, ZoomIn, ZoomOut, Download } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useState } from "react"

export function DocumentViewer() {
  const [zoom, setZoom] = useState(100)
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null)

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="border-b p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Document Viewer</h2>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => setZoom(Math.max(50, zoom - 10))}
              disabled={!selectedDocument}
            >
              <ZoomOut className="h-4 w-4" />
            </Button>
            <span className="text-sm text-muted-foreground w-12 text-center">
              {zoom}%
            </span>
            <Button
              variant="outline"
              size="icon"
              onClick={() => setZoom(Math.min(200, zoom + 10))}
              disabled={!selectedDocument}
            >
              <ZoomIn className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon" disabled={!selectedDocument}>
              <Download className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Document Display Area */}
      <div className="flex-1 overflow-auto bg-muted/20 p-4">
        {selectedDocument ? (
          <Card className="mx-auto max-w-4xl p-8">
            {/* Placeholder for PDF viewer - will be implemented in Phase 3 */}
            <div className="space-y-4">
              <h3 className="text-xl font-bold">Subset-026: System Requirements Specification</h3>
              <p className="text-sm text-muted-foreground">Version 4.0.0</p>

              <div className="mt-8 space-y-4">
                <div className="rounded-md border p-4">
                  <h4 className="font-semibold mb-2">3.4.2 Data Communication</h4>
                  <p className="text-sm leading-relaxed">
                    The onboard equipment shall be able to establish and maintain
                    communication with the Radio Block Centre (RBC) using the GSM-R
                    network. The communication shall follow the protocols defined in
                    Subset-037 and Subset-026-7.
                  </p>
                </div>

                <div className="rounded-md border p-4">
                  <h4 className="font-semibold mb-2">3.4.3 Movement Authority</h4>
                  <p className="text-sm leading-relaxed">
                    The movement authority (MA) defines the distance that a train is
                    permitted to travel. The onboard equipment shall continuously
                    supervise the train's movement against the MA and apply brakes
                    if necessary.
                  </p>
                </div>
              </div>

              <div className="mt-8 text-center text-sm text-muted-foreground">
                <p>PDF viewer will be integrated in Phase 3</p>
                <p>with auto-scroll and paragraph highlighting</p>
              </div>
            </div>
          </Card>
        ) : (
          <div className="flex h-full items-center justify-center">
            <div className="text-center">
              <FileText className="mx-auto h-16 w-16 text-muted-foreground" />
              <h3 className="mt-4 text-lg font-semibold">No Document Selected</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                Citations from chat messages will appear here
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
