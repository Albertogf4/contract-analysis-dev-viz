"use client"

import { X } from "lucide-react"
import type { KnowledgeGraphNode } from "@/lib/types/knowledge-graph"

interface NodeDetailsProps {
  node: KnowledgeGraphNode | null
  neighbors: KnowledgeGraphNode[]
  onClose: () => void
}

export function NodeDetails({ node, neighbors, onClose }: NodeDetailsProps) {
  if (!node) return null

  return (
    <div className="border-t border-border p-4 bg-muted/30">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">Node Details</h3>
        <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors">
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="space-y-3">
        <div>
          <p className="text-xs font-medium text-muted-foreground uppercase">Label</p>
          <p className="text-sm font-semibold text-foreground">{node.label}</p>
        </div>

        <div>
          <p className="text-xs font-medium text-muted-foreground uppercase">Type</p>
          <p className="text-sm text-foreground">{node.type}</p>
        </div>

        {node.description && (
          <div>
            <p className="text-xs font-medium text-muted-foreground uppercase">Description</p>
            <p className="text-sm text-foreground">{node.description}</p>
          </div>
        )}

        {neighbors.length > 0 && (
          <div>
            <p className="text-xs font-medium text-muted-foreground uppercase mb-2">
              Connected Nodes ({neighbors.length})
            </p>
            <div className="space-y-1">
              {neighbors.map((neighbor) => (
                <div
                  key={neighbor.id}
                  className="text-xs p-2 rounded bg-background border border-border text-foreground"
                >
                  {neighbor.label}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
