export async function GET(request: Request, { params }: { params: Promise<{ documentId: string }> }) {
  const { documentId } = await params
  const backendUrl = process.env.BACKEND_API_URL || "http://localhost:5328"

  try {
    const response = await fetch(`${backendUrl}/api/graph/${documentId}`)

    if (!response.ok) {
      return Response.json({ error: "Failed to fetch knowledge graph" }, { status: response.status })
    }

    const data = await response.json()
    return Response.json(data)
  } catch (error) {
    console.error("[v0] Error fetching knowledge graph:", error)
    return Response.json({ error: "Failed to fetch knowledge graph" }, { status: 500 })
  }
}