export async function GET(request: Request, { params }: { params: Promise<{ documentId: string; nodeId: string }> }) {
  const { documentId, nodeId } = await params
  const backendUrl = process.env.BACKEND_API_URL || "http://localhost:5328"

  try {
    const response = await fetch(`${backendUrl}/api/graph/${documentId}/node/${nodeId}`)

    if (!response.ok) {
      return Response.json({ error: "Failed to fetch node details" }, { status: response.status })
    }

    const data = await response.json()
    return Response.json(data)
  } catch (error) {
    console.error("[v0] Error fetching node details:", error)
    return Response.json({ error: "Failed to fetch node details" }, { status: 500 })
  }
}
