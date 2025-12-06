"use client"

import { useState, useCallback } from "react"
import type { KnowledgeGraphResponse, NodeDetailsResponse } from "@/lib/types/knowledge-graph"

export function useKnowledgeGraph() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchGraph = useCallback(async (documentId: string): Promise<KnowledgeGraphResponse | null> => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`/api/graph/${documentId}`)

      if (response.status === 404) {
        setError("No knowledge graph available for this document yet.")
        return null
      }

      if (!response.ok) {
        throw new Error("Failed to fetch knowledge graph")
      }

      const data = await response.json()
      return data
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to fetch knowledge graph"
      setError(message)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchNodeDetails = useCallback(
    async (documentId: string, nodeId: string): Promise<NodeDetailsResponse | null> => {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(`/api/graph/${documentId}/node/${nodeId}`)

        if (!response.ok) {
          throw new Error("Failed to fetch node details")
        }

        const data = await response.json()
        return data
      } catch (err) {
        const message = err instanceof Error ? err.message : "Failed to fetch node details"
        setError(message)
        return null
      } finally {
        setLoading(false)
      }
    },
    [],
  )

  return { fetchGraph, fetchNodeDetails, loading, error }
}
