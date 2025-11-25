"use client"

import { FileText, Trash2, Loader2, AlertCircle, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { UploadedDocument } from "./document-qa-app"

interface DocumentListProps {
  documents: UploadedDocument[]
  activeDocId: string | null
  onSelectDocument: (docId: string) => void
  onDeleteDocument: (docId: string) => void
}

const statusConfig = {
  Uploaded: { icon: FileText, color: "text-blue-500", bg: "bg-blue-50" },
  Processing: { icon: Loader2, color: "text-yellow-500", bg: "bg-yellow-50" },
  Ready: { icon: Check, color: "text-green-500", bg: "bg-green-50" },
  Error: { icon: AlertCircle, color: "text-red-500", bg: "bg-red-50" },
}

export function DocumentList({ documents, activeDocId, onSelectDocument, onDeleteDocument }: DocumentListProps) {
  if (documents.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <FileText className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm">No documents uploaded yet</p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {documents.map((doc) => {
        const config = statusConfig[doc.status]
        const StatusIcon = config.icon
        const isActive = doc.document_id === activeDocId

        return (
          <button
            key={doc.document_id}
            onClick={() => onSelectDocument(doc.document_id)}
            className={`w-full p-3 rounded-lg border transition-all text-left ${
              isActive ? "border-primary bg-primary/10" : "border-border hover:border-primary/50 hover:bg-primary/5"
            }`}
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <StatusIcon
                    className={`w-4 h-4 flex-shrink-0 ${config.color} ${
                      doc.status === "Processing" ? "animate-spin" : ""
                    }`}
                  />
                  <p className="text-sm font-medium truncate">{doc.filename}</p>
                </div>
                <p className="text-xs text-muted-foreground truncate">{doc.uploaded_at}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-xs px-2 py-1 rounded ${config.bg}`}>{doc.status}</span>
                  <span className="text-xs text-muted-foreground">ID: {doc.document_id.substring(0, 8)}...</span>
                </div>
              </div>
              <Button
                size="sm"
                variant="ghost"
                onClick={(e) => {
                  e.stopPropagation()
                  onDeleteDocument(doc.document_id)
                }}
                className="opacity-0 group-hover:opacity-100"
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          </button>
        )
      })}
    </div>
  )
}
