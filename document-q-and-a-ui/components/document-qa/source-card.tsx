"use client"

import { ChevronDown, BookOpen } from "lucide-react"
import type { Context } from "./document-qa-app"

interface SourceCardProps {
  context: Context
  isExpanded: boolean
  onToggleExpand: () => void
}

export function SourceCard({ context, isExpanded, onToggleExpand }: SourceCardProps) {
  return (
    <div className="border border-border rounded-md bg-background hover:bg-card transition-colors">
      <button
        onClick={onToggleExpand}
        className="w-full p-2 text-left flex items-center justify-between hover:bg-muted transition-colors"
      >
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <BookOpen className="w-3 h-3 text-muted-foreground flex-shrink-0" />
            <span className="text-xs font-medium truncate">{context.filename}</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>Page {context.page_number}</span>
            <span>•</span>
            <span>
              Chars {context.start_char}-{context.end_char}
            </span>
            <span>•</span>
            <span className="text-blue-600 font-medium">{(context.score * 100).toFixed(0)}%</span>
          </div>
        </div>
        <ChevronDown
          className={`w-4 h-4 text-muted-foreground flex-shrink-0 transition-transform ${
            isExpanded ? "rotate-180" : ""
          }`}
        />
      </button>

      {isExpanded && (
        <div className="border-t border-border p-2 bg-muted/50">
          <p className="text-xs text-foreground leading-relaxed">{context.text}</p>
        </div>
      )}
    </div>
  )
}
