"use client"

import { useState } from "react"
import type { Message } from "./document-qa-app"
import { SourceCard } from "./source-card"

interface ChatMessageProps {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const [expandedSources, setExpandedSources] = useState<string | null>(null)

  if (message.type === "user") {
    return (
      <div className="flex justify-end">
        <div className="bg-primary text-primary-foreground p-4 rounded-lg max-w-xs">
          <p className="text-sm">{message.content}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="bg-muted p-4 rounded-lg max-w-md w-full">
        <p className="text-sm text-foreground mb-4">{message.content}</p>

        {message.contexts && message.contexts.length > 0 && (
          <div>
            <p className="text-xs font-medium text-muted-foreground mb-2">Sources ({message.contexts.length})</p>
            <div className="space-y-2">
              {message.contexts.map((context) => (
                <SourceCard
                  key={context.chunk_id}
                  context={context}
                  isExpanded={expandedSources === context.chunk_id}
                  onToggleExpand={() =>
                    setExpandedSources(expandedSources === context.chunk_id ? null : context.chunk_id)
                  }
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
