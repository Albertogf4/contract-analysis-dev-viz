import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { question, document_id } = body

    if (!question || !document_id) {
      return NextResponse.json({ error: "Missing question or document_id" }, { status: 400 })
    }

    // Forward to backend API
    const backendResponse = await fetch(`${process.env.BACKEND_API_URL || "http://localhost:5328"}/api/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question, document_id }),
    })

    if (!backendResponse.ok) {
      throw new Error("Backend query failed")
    }

    const data = await backendResponse.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Query error:", error)
    return NextResponse.json({ error: error instanceof Error ? error.message : "Query failed" }, { status: 500 })
  }
}
