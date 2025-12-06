"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
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
        <div className="text-sm text-foreground mb-4 prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              h1: ({ children }) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
              h2: ({ children }) => <h2 className="text-base font-bold mb-2">{children}</h2>,
              h3: ({ children }) => <h3 className="text-sm font-bold mb-2">{children}</h3>,
              ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
              li: ({ children }) => <li className="text-sm">{children}</li>,
              code: ({ children }) => (
                <code className="bg-background text-foreground px-2 py-1 rounded text-xs font-mono">{children}</code>
              ),
              pre: ({ children }) => (
                <pre className="bg-background text-foreground p-3 rounded-lg overflow-x-auto mb-2 text-xs">
                  {children}
                </pre>
              ),
              blockquote: ({ children }) => (
                <blockquote className="border-l-4 border-primary pl-4 italic text-muted-foreground mb-2">
                  {children}
                </blockquote>
              ),
              a: ({ href, children }) => (
                <a href={href} className="text-primary underline hover:opacity-80">
                  {children}
                </a>
              ),
              strong: ({ children }) => <strong className="font-bold">{children}</strong>,
              em: ({ children }) => <em className="italic">{children}</em>,
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

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
