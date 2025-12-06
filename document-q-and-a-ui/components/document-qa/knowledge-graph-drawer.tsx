"use client"

import { useEffect, useState, useRef } from "react"
import { X } from "lucide-react"
import { KnowledgeGraphView } from "./knowledge-graph-view"
import { NodeDetails } from "./node-details"
import { useKnowledgeGraph } from "@/hooks/use-knowledge-graph"
import type { KnowledgeGraphNode, KnowledgeGraphEdge, NodeDetailsResponse } from "@/lib/types/knowledge-graph"

interface KnowledgeGraphDrawerProps {
  isOpen: boolean
  onClose: () => void
  documentId: string
  documentName: string
}

export function KnowledgeGraphDrawer({ isOpen, onClose, documentId, documentName }: KnowledgeGraphDrawerProps) {
  const { fetchGraph, fetchNodeDetails, loading } = useKnowledgeGraph()
  const [nodes, setNodes] = useState<KnowledgeGraphNode[]>([])
  const [edges, setEdges] = useState<KnowledgeGraphEdge[]>([])
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null)
  const [nodeDetailsData, setNodeDetailsData] = useState<NodeDetailsResponse | null>(null)
  const [width, setWidth] = useState(384) // sm:w-96 = 384px
  const resizeRef = useRef<HTMLDivElement>(null)
  const isDraggingRef = useRef(false)

  useEffect(() => {
    const handleMouseDown = () => {
      isDraggingRef.current = true
    }

    const handleMouseMove = (e: MouseEvent) => {
      if (!isDraggingRef.current) return

      const container = resizeRef.current
      if (!container) return

      const rect = container.getBoundingClientRect()
      const newWidth = rect.right - e.clientX

      // Constrain width between 300px (min) and window width - 100px
      const minWidth = 300
      const maxWidth = window.innerWidth - 100
      if (newWidth >= minWidth && newWidth <= maxWidth) {
        setWidth(newWidth)
      }
    }

    const handleMouseUp = () => {
      isDraggingRef.current = false
    }

    document.addEventListener("mousemove", handleMouseMove)
    document.addEventListener("mouseup", handleMouseUp)
    const resizeHandle = resizeRef.current?.querySelector("[data-resize-handle]")
    resizeHandle?.addEventListener("mousedown", handleMouseDown)

    return () => {
      document.removeEventListener("mousemove", handleMouseMove)
      document.removeEventListener("mouseup", handleMouseUp)
      resizeHandle?.removeEventListener("mousedown", handleMouseDown)
    }
  }, [])

  // Fetch graph data when drawer opens
  useEffect(() => {
    if (!isOpen || !documentId) return

    const loadGraph = async () => {
      const data = await fetchGraph(documentId)
      if (data) {
        setNodes(data.nodes)
        setEdges(data.edges)
        setSelectedNodeId(null)
        setNodeDetailsData(null)
      }
    }

    loadGraph()
  }, [isOpen, documentId, fetchGraph])

  // Fetch node details when a node is selected
  useEffect(() => {
    if (!selectedNodeId || !documentId) return

    const loadNodeDetails = async () => {
      const data = await fetchNodeDetails(documentId, selectedNodeId)
      setNodeDetailsData(data)
    }

    loadNodeDetails()
  }, [selectedNodeId, documentId, fetchNodeDetails])

  if (!isOpen) return null

  return (
    <>
      {/* Overlay for mobile */}
      <div className="fixed inset-0 bg-black/50 lg:hidden z-40" onClick={onClose} />

      {/* Drawer */}
      <div
        ref={resizeRef}
        className={`fixed right-0 top-0 bottom-0 bg-background border-l border-border shadow-lg z-50 flex flex-col transition-transform duration-300 ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
        style={{ width: `${width}px` }}
      >
        <div
          data-resize-handle
          className="absolute left-0 top-0 bottom-0 w-1 bg-border hover:bg-primary cursor-col-resize hover:shadow-md transition-all"
        />

        {/* Header */}
        <div className="border-b border-border p-4 flex items-center justify-between">
          <div className="flex-1">
            <h2 className="font-semibold text-foreground">Knowledge Graph</h2>
            <p className="text-xs text-muted-foreground mt-1">{documentName}</p>
            <p className="text-xs text-muted-foreground">ID: {documentId.slice(0, 8)}...</p>
          </div>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors ml-2">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden flex flex-col">
          <div className="p-4 flex-1 overflow-hidden">
            <KnowledgeGraphView
              nodes={nodes}
              edges={edges}
              selectedNodeId={selectedNodeId}
              onNodeClick={setSelectedNodeId}
              isLoading={loading}
            />
          </div>

          {/* Node Details */}
          {nodeDetailsData && (
            <NodeDetails
              node={nodeDetailsData.center}
              neighbors={nodeDetailsData.neighbors}
              onClose={() => {
                setSelectedNodeId(null)
                setNodeDetailsData(null)
              }}
            />
          )}
        </div>
      </div>
    </>
  )
}
