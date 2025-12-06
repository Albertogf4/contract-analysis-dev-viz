"use client"

import {
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  WheelEvent,
} from "react"
import type { KnowledgeGraphNode, KnowledgeGraphEdge } from "@/lib/types/knowledge-graph"
import { cn } from "@/lib/utils" // if you don't have cn, you can remove it and inline classNames

interface KnowledgeGraphViewProps {
  nodes: KnowledgeGraphNode[]
  edges: KnowledgeGraphEdge[]
  selectedNodeId: string | null
  onNodeClick: (id: string) => void
  isLoading?: boolean
}

type PositionedNode = KnowledgeGraphNode & {
  x: number
  y: number
}

const MIN_SCALE = 0.4
const MAX_SCALE = 2.5

function clampScale(s: number) {
  return Math.min(MAX_SCALE, Math.max(MIN_SCALE, s))
}

export function KnowledgeGraphView({
  nodes,
  edges,
  selectedNodeId,
  onNodeClick,
  isLoading,
}: KnowledgeGraphViewProps) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 })
  const [layoutNodes, setLayoutNodes] = useState<PositionedNode[]>([])
  const [scale, setScale] = useState(0.9) // start slightly zoomed out

  // Measure container
  useLayoutEffect(() => {
    if (!containerRef.current) return

    const el = containerRef.current
    const update = () => {
      const rect = el.getBoundingClientRect()
      setDimensions({ width: rect.width, height: rect.height })
    }

    update()
    const observer = new ResizeObserver(update)
    observer.observe(el)

    return () => observer.disconnect()
  }, [])

  // Degree map (to find central node)
  const degreeMap = useMemo(() => {
    const map = new Map<string, number>()
    edges.forEach((e) => {
      map.set(e.source, (map.get(e.source) ?? 0) + 1)
      map.set(e.target, (map.get(e.target) ?? 0) + 1)
    })
    nodes.forEach((n) => {
      if (!map.has(n.id)) map.set(n.id, 0)
    })
    return map
  }, [nodes, edges])

  // Layout: central hub + multiple rings, fewer nodes per ring
  useEffect(() => {
    if (!dimensions.width || !dimensions.height || nodes.length === 0) {
      setLayoutNodes([])
      return
    }

    const centerX = dimensions.width / 2
    const centerY = dimensions.height / 2
    const maxRadius = Math.min(centerX, centerY) * 0.9

    const sorted = [...nodes].sort(
      (a, b) => (degreeMap.get(b.id) ?? 0) - (degreeMap.get(a.id) ?? 0)
    )

    const [centerNode, ...rest] = sorted
    const layout: PositionedNode[] = []

    if (centerNode) {
      layout.push({
        ...centerNode,
        x: centerX,
        y: centerY,
      })
    }

    const maxPerRing = 6
    const layers = Math.max(1, Math.ceil(rest.length / maxPerRing))
    const ringSpacing = maxRadius / (layers + 1)

    let idx = 0
    for (let layer = 0; layer < layers; layer++) {
      const layerNodes = rest.slice(idx, idx + maxPerRing)
      idx += maxPerRing

      const r = ringSpacing * (layer + 1)
      const step = (2 * Math.PI) / Math.max(layerNodes.length, 1)
      const offset = (layer % 2) * (step / 2) // offset each ring a bit

      layerNodes.forEach((node, i) => {
        const angle = i * step + offset
        layout.push({
          ...node,
          x: centerX + r * Math.cos(angle),
          y: centerY + r * Math.sin(angle),
        })
      })
    }

    setLayoutNodes(layout)
  }, [nodes, degreeMap, dimensions])

  const nodeById = useMemo(() => {
    const map = new Map<string, PositionedNode>()
    layoutNodes.forEach((n) => map.set(n.id, n))
    return map
  }, [layoutNodes])

  const neighborIds = useMemo(() => {
    if (!selectedNodeId) return new Set<string>()
    const neighbors = new Set<string>()
    edges.forEach((e) => {
      if (e.source === selectedNodeId) neighbors.add(e.target)
      if (e.target === selectedNodeId) neighbors.add(e.source)
    })
    return neighbors
  }, [edges, selectedNodeId])

  const hasData = nodes.length > 0
  const width = dimensions.width || 400
  const height = dimensions.height || 256
  const centerX = width / 2
  const centerY = height / 2

  const handleWheel = (event: WheelEvent<HTMLDivElement>) => {
    if (!hasData) return
    event.preventDefault()
    const direction = event.deltaY > 0 ? -1 : 1
    setScale((prev) => clampScale(prev * (direction > 0 ? 1.1 : 0.9)))
  }

  return (
    <div
      ref={containerRef}
      onWheel={handleWheel}
      className={cn(
        "w-full h-64 sm:h-80 rounded-xl border border-border relative overflow-hidden",
        "bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900"
      )}
    >
      {/* Zoom controls */}
      {hasData && (
        <div className="absolute top-2 right-2 z-20 flex flex-col gap-1">
          <button
            type="button"
            onClick={() => setScale((s) => clampScale(s * 1.15))}
            className="h-7 w-7 rounded-full bg-slate-800/80 text-slate-100 text-sm flex items-center justify-center hover:bg-slate-700"
          >
            +
          </button>
          <button
            type="button"
            onClick={() => setScale((s) => clampScale(s * 0.85))}
            className="h-7 w-7 rounded-full bg-slate-800/80 text-slate-100 text-sm flex items-center justify-center hover:bg-slate-700"
          >
            –
          </button>
          <button
            type="button"
            onClick={() => setScale(0.9)}
            className="h-7 w-7 rounded-full bg-slate-800/80 text-slate-100 text-[11px] flex items-center justify-center hover:bg-slate-700"
          >
            ⟳
          </button>
        </div>
      )}

      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-background/40 backdrop-blur-sm z-10">
          <div className="h-10 w-10 rounded-full border-2 border-slate-500 border-t-sky-400 animate-spin" />
          <p className="mt-2 text-xs text-muted-foreground">Building knowledge graph…</p>
        </div>
      )}

      {/* Empty state */}
      {!isLoading && !hasData && (
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4">
          <p className="text-sm text-muted-foreground">
            No knowledge graph data for this document yet.
          </p>
          <p className="mt-1 text-xs text-muted-foreground/80">
            Upload a document and wait for processing to complete.
          </p>
        </div>
      )}

      {/* Graph */}
      {hasData && (
        <svg className="w-full h-full" viewBox={`0 0 ${width} ${height}`}>
          <g
            transform={`
              translate(${centerX}, ${centerY})
              scale(${scale})
              translate(${-centerX}, ${-centerY})
            `}
          >
            {/* Edges */}
            {edges.map((e) => {
              const source = nodeById.get(e.source)
              const target = nodeById.get(e.target)
              if (!source || !target) return null

              const isActive =
                selectedNodeId &&
                (e.source === selectedNodeId || e.target === selectedNodeId)

              return (
                <g key={e.id}>
                  <line
                    x1={source.x}
                    y1={source.y}
                    x2={target.x}
                    y2={target.y}
                    stroke={isActive ? "#38bdf8" : "#4b5563"}
                    strokeWidth={isActive ? 2 : 1}
                    strokeOpacity={isActive ? 0.9 : 0.5}
                  />
                </g>
              )
            })}

            {/* Nodes */}
            {layoutNodes.map((node) => {
              const isSelected = node.id === selectedNodeId
              const isNeighbor = neighborIds.has(node.id)

              const fill = isSelected
                ? "#38bdf8"
                : isNeighbor
                ? "#a5b4fc"
                : "#e5e7eb"

              const stroke = isSelected ? "#0ea5e9" : "#1f2937"

              return (
                <g
                  key={node.id}
                  transform={`translate(${node.x}, ${node.y})`}
                  onClick={() => onNodeClick(node.id)}
                  className="cursor-pointer"
                >
                  <circle
                    r={isSelected ? 12 : 9}
                    fill={fill}
                    stroke={stroke}
                    strokeWidth={2}
                    className="transition-all duration-150"
                  />
                  {/* Label background */}
                  <rect
                    x={14}
                    y={-10}
                    rx={4}
                    ry={4}
                    height={20}
                    width={Math.min(120, 8 * (node.label?.length ?? 8))}
                    fill="rgba(15,23,42,0.85)"
                    stroke="rgba(148,163,184,0.6)"
                    strokeWidth={0.5}
                  />
                  {/* Label text */}
                  <text
                    x={18}
                    y={5}
                    fontSize={10}
                    fill="#e5e7eb"
                    className="select-none"
                  >
                    {truncate(node.label, 18)}
                  </text>
                </g>
              )
            })}
          </g>
        </svg>
      )}

      {/* Footer hint */}
      <div className="absolute bottom-2 left-0 right-0 text-center text-[11px] text-slate-300/80 pointer-events-none">
        Scroll to zoom · Click nodes to view details
      </div>
    </div>
  )
}

function truncate(text: string | undefined, max: number): string {
  if (!text) return ""
  if (text.length <= max) return text
  return text.slice(0, max - 1) + "…"
}
