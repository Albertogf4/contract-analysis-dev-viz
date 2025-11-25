"use client"

import type React from "react"

import { useState } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"

interface QuestionInputProps {
  onSubmit: (question: string) => void
  isDisabled: boolean
  isLoading: boolean
  placeholder?: string
}

export function QuestionInput({ onSubmit, isDisabled, isLoading, placeholder }: QuestionInputProps) {
  const [question, setQuestion] = useState("")

  const handleSubmit = () => {
    if (question.trim() && !isDisabled && !isLoading) {
      onSubmit(question)
      setQuestion("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !isDisabled && !isLoading) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="flex gap-3">
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={isDisabled || isLoading}
        rows={3}
        className="flex-1 p-3 border border-border rounded-lg resize-none bg-background text-foreground placeholder-muted-foreground disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-primary"
      />
      <Button
        onClick={handleSubmit}
        disabled={isDisabled || isLoading || !question.trim()}
        size="lg"
        className="self-end"
      >
        <Send className="w-4 h-4" />
      </Button>
    </div>
  )
}
