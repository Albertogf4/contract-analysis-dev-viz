"use client"

import { useState } from "react"
import { DocumentPanel } from "./document-panel"
import { ChatPanel } from "./chat-panel"
import { Toaster } from "@/components/ui/toaster"

export interface UploadedDocument {
  document_id: string
  filename: string
  uploaded_at: string
  status: "Uploaded" | "Processing" | "Ready" | "Error"
  size?: number
  pages?: number
}

export interface Message {
  id: string
  type: "user" | "assistant"
  content: string
  contexts?: Context[]
  timestamp: string
}

export interface Context {
  chunk_id: string
  document_id: string
  filename: string
  page_number: number
  start_char: number
  end_char: number
  score: number
  text: string
}

export function DocumentQAApp() {
  const [documents, setDocuments] = useState<UploadedDocument[]>([])
  const [activeDocId, setActiveDocId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [uploadingFileId, setUploadingFileId] = useState<string | null>(null)

  const activeDoc = documents.find((d) => d.document_id === activeDocId)

  const handleDocumentUpload = (doc: UploadedDocument) => {
    setDocuments((prev) => [...prev, doc])
    setActiveDocId(doc.document_id)
  }

  const handleStatusUpdate = (docId: string, status: UploadedDocument["status"]) => {
    setDocuments((prev) => prev.map((d) => (d.document_id === docId ? { ...d, status } : d)))
  }

  const handleUploadingChange = (fileId: string | null) => {
    setUploadingFileId(fileId)
  }

  const handleAddMessage = (message: Message) => {
    setMessages((prev) => [...prev, message])
  }

  const handleClearMessages = () => {
    setMessages([])
  }

  return (
    <div className="flex h-screen bg-background">
      <DocumentPanel
        documents={documents}
        activeDocId={activeDocId}
        onSelectDocument={setActiveDocId}
        onDocumentUpload={handleDocumentUpload}
        onStatusUpdate={handleStatusUpdate}
        uploadingFileId={uploadingFileId}
        onUploadingChange={handleUploadingChange}
      />
      <ChatPanel
        activeDoc={activeDoc}
        messages={messages}
        onAddMessage={handleAddMessage}
        onClearMessages={handleClearMessages}
      />
      <Toaster />
    </div>
  )
}
