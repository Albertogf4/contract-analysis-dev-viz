import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get("file") as File

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 })
    }

    // Forward to backend API
    const backendFormData = new FormData()
    backendFormData.append("file", file)

    const backendResponse = await fetch(`${process.env.BACKEND_API_URL || "http://localhost:5328"}/api/upload`, {
      method: "POST",
      body: backendFormData,
    })

    if (!backendResponse.ok) {
      throw new Error("Backend upload failed")
    }

    const data = await backendResponse.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Upload error:", error)
    return NextResponse.json({ error: error instanceof Error ? error.message : "Upload failed" }, { status: 500 })
  }
}
