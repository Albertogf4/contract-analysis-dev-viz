"use client"

import { useRef, useState } from "react"
import { Upload, FileText, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import { DocumentList } from "./document-list"
import { UploadZone } from "./upload-zone"
import { DocumentInfo } from "./document-info"
import type { UploadedDocument } from "./document-qa-app"

interface DocumentPanelProps {
  documents: UploadedDocument[]
  activeDocId: string | null
  onSelectDocument: (docId: string) => void
  onDocumentUpload: (doc: UploadedDocument) => void
  onStatusUpdate: (docId: string, status: UploadedDocument["status"]) => void
  uploadingFileId: string | null
  onUploadingChange: (fileId: string | null) => void
}

export function DocumentPanel({
  documents,
  activeDocId,
  onSelectDocument,
  onDocumentUpload,
  onStatusUpdate,
  uploadingFileId,
  onUploadingChange,
}: DocumentPanelProps) {
  const { toast } = useToast()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isCheckingHealth, setIsCheckingHealth] = useState(false)

  const handleCheckHealth = async () => {
    setIsCheckingHealth(true)
    try {
      const response = await fetch(`${process.env.BACKEND_API_URL || "http://localhost:5328"}/api/health`, {
        method: "GET",
      })

      if (!response.ok) {
        throw new Error("API health check failed")
      }

      const data = await response.json()

      if (data.status === "ok") {
        toast({
          title: "API Connected",
          description: "Backend API is working correctly.",
        })
      } else {
        throw new Error("Unexpected response from API")
      }
    } catch (error) {
      toast({
        title: "API Connection Failed",
        description: error instanceof Error ? error.message : "Unable to connect to backend API",
        variant: "destructive",
      })
    } finally {
      setIsCheckingHealth(false)
    }
  }

  const handleFileSelect = async (file: File) => {
    if (!file.type.includes("pdf")) {
      toast({
        title: "Invalid file type",
        description: "Please upload a PDF file.",
        variant: "destructive",
      })
      return
    }

    const fileId = Math.random().toString(36).substring(7)
    onUploadingChange(fileId)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Upload failed")
      }

      const data = await response.json()
      const newDoc: UploadedDocument = {
        document_id: data.document_id,
        filename: data.filename,
        uploaded_at: new Date().toLocaleString(),
        status: "Processing",
        size: file.size,
      }

      onDocumentUpload(newDoc)
      onUploadingChange(null)

      // Simulate status update to Ready after a brief delay
      setTimeout(() => {
        onStatusUpdate(data.document_id, "Ready")
      }, 3000)

      toast({
        title: "Upload successful",
        description: `${file.name} is now being processed.`,
      })
    } catch (error) {
      onUploadingChange(null)
      onStatusUpdate(fileId, "Error")
      toast({
        title: "Upload failed",
        description: error instanceof Error ? error.message : "An error occurred",
        variant: "destructive",
      })
    }
  }

  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  const handleDeleteDocument = (docId: string) => {
    // TODO: Implement API call to delete document
  }

  const activeDoc = documents.find((d) => d.document_id === activeDocId)

  return (
    <div className="w-96 border-r border-border flex flex-col bg-card">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            <h1 className="text-lg font-semibold">Documents</h1>
          </div>
          <Button
            size="sm"
            variant="ghost"
            onClick={handleCheckHealth}
            disabled={isCheckingHealth}
            title="Test API connection"
          >
            <Zap className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Upload Zone */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4">
          <UploadZone
            onFileSelect={handleFileSelect}
            isUploading={uploadingFileId !== null}
            uploadingFileId={uploadingFileId}
          />

          {/* Fallback Upload Button */}
          <div className="mt-4">
            <Button
              onClick={handleUploadClick}
              variant="outline"
              className="w-full bg-transparent"
              disabled={uploadingFileId !== null}
            >
              <Upload className="w-4 h-4 mr-2" />
              Choose File
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={(e) => {
                const file = e.currentTarget.files?.[0]
                if (file) handleFileSelect(file)
              }}
              className="hidden"
            />
          </div>

          {/* Document List */}
          <div className="mt-6">
            <h2 className="text-sm font-medium text-muted-foreground mb-3">Uploaded Documents</h2>
            <DocumentList
              documents={documents}
              activeDocId={activeDocId}
              onSelectDocument={onSelectDocument}
              onDeleteDocument={handleDeleteDocument}
            />
          </div>
        </div>
      </div>

      {/* Document Info */}
      {activeDoc && (
        <div className="p-4 border-t border-border">
          <DocumentInfo document={activeDoc} />
        </div>
      )}
    </div>
  )
}
