"use client"

import { Eye } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { UploadedDocument } from "./document-qa-app"

interface DocumentInfoProps {
  document: UploadedDocument
}

export function DocumentInfo({ document }: DocumentInfoProps) {
  return (
    <div className="space-y-3">
      <div>
        <p className="text-xs font-medium text-muted-foreground mb-1">Document Name</p>
        <p className="text-sm font-semibold text-foreground truncate">{document.filename}</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-1">Size</p>
          <p className="text-sm text-foreground">{document.size ? `${(document.size / 1024).toFixed(1)} KB` : "-"}</p>
        </div>
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-1">Pages</p>
          <p className="text-sm text-foreground">{document.pages || "-"}</p>
        </div>
      </div>

      <div>
        <p className="text-xs font-medium text-muted-foreground mb-2">Status</p>
        <div className="inline-block px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
          {document.status}
        </div>
      </div>

      <Button className="w-full mt-2 bg-transparent" variant="outline" size="sm">
        <Eye className="w-4 h-4 mr-2" />
        View PDF
      </Button>
    </div>
  )
}
