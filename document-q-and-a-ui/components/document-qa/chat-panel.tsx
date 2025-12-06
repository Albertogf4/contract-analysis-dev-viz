"use client"

import { useState } from "react"
import { AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ChatMessages } from "./chat-messages"
import { QuestionInput } from "./question-input"
import { KnowledgeGraphButton } from "./knowledge-graph-button"
import { KnowledgeGraphDrawer } from "./knowledge-graph-drawer"
import type { UploadedDocument, Message } from "./document-qa-app"
import { useToast } from "@/hooks/use-toast"

interface ChatPanelProps {
  activeDoc: UploadedDocument | undefined
  messages: Message[]
  onAddMessage: (message: Message) => void
  onClearMessages: () => void
}

export function ChatPanel({ activeDoc, messages, onAddMessage, onClearMessages }: ChatPanelProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [isGraphOpen, setIsGraphOpen] = useState(false)
  const { toast } = useToast()

  const isDocProcessing = activeDoc?.status !== "Ready"
  const isDisabled = !activeDoc || isDocProcessing || isLoading
  const isGraphEnabled = activeDoc?.status === "Ready"

  const handleSendQuestion = async (question: string) => {
    if (!activeDoc || !question.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Math.random().toString(36).substring(7),
      type: "user",
      content: question,
      timestamp: new Date().toISOString(),
    }

    onAddMessage(userMessage)
    setIsLoading(true)

    try {
      const response = await fetch("/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          document_id: activeDoc.document_id,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to get answer")
      }

      const data = await response.json()

      const assistantMessage: Message = {
        id: Math.random().toString(36).substring(7),
        type: "assistant",
        content: data.answer,
        contexts: data.contexts,
        timestamp: new Date().toISOString(),
      }

      onAddMessage(assistantMessage)
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to get answer",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex-1 flex flex-col bg-background">
      {/* Header */}
      <div className="border-b border-border p-4 flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Current Document</p>
          <h2 className="text-lg font-semibold">{activeDoc ? activeDoc.filename : "No document selected"}</h2>
          {activeDoc && <p className="text-xs text-muted-foreground mt-1">Status: {activeDoc.status}</p>}
        </div>
        <div className="flex items-center gap-2">
          <KnowledgeGraphButton
            isEnabled={isGraphEnabled}
            isOpen={isGraphOpen}
            onClick={() => setIsGraphOpen(!isGraphOpen)}
          />
        {messages.length > 0 && (
          <Button variant="outline" size="sm" onClick={onClearMessages}>
            Clear
          </Button>
        )}
        </div>
      </div>

      {/* Messages */}
      <ChatMessages messages={messages} isLoading={isLoading} />

      {/* Helper Messages */}
      {!activeDoc && (
        <div className="mx-4 p-4 bg-blue-50 border border-blue-200 rounded-lg flex gap-3">
          <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-blue-900">No document selected</p>
            <p className="text-sm text-blue-800">Upload or select a document to start asking questions.</p>
          </div>
        </div>
      )}

      {activeDoc && isDocProcessing && (
        <div className="mx-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg flex gap-3">
          <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-yellow-900">Document is processing</p>
            <p className="text-sm text-yellow-800">Please wait until the document is ready before asking questions.</p>
          </div>
        </div>
      )}

      {/* Input */}
      <div className="border-t border-border p-4">
        <QuestionInput
          onSubmit={handleSendQuestion}
          isDisabled={isDisabled}
          isLoading={isLoading}
          placeholder={
            !activeDoc
              ? "Select a document to ask questions"
              : isDocProcessing
                ? "Document is processing..."
                : "Ask a question about the selected document…"
          }
        />
      </div>


      {/* Knowledge Graph Drawer */}
      {activeDoc && (
        <KnowledgeGraphDrawer
          isOpen={isGraphOpen}
          onClose={() => setIsGraphOpen(false)}
          documentId={activeDoc.document_id}
          documentName={activeDoc.filename}
        />
      )}
    </div>
  )
}
