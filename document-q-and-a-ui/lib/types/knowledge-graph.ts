export interface KnowledgeGraphNode {
  id: string
  label: string
  type: string
  description: string | null
}

export interface KnowledgeGraphEdge {
  id: string
  source: string
  target: string
  relation: string
}

export interface KnowledgeGraphResponse {
  document_id: string
  nodes: KnowledgeGraphNode[]
  edges: KnowledgeGraphEdge[]
}

export interface NodeDetailsResponse {
  document_id: string
  center: KnowledgeGraphNode
  neighbors: KnowledgeGraphNode[]
  edges: KnowledgeGraphEdge[]
}
