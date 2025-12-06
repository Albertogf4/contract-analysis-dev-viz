"use client"

import { Network } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface KnowledgeGraphButtonProps {
  isEnabled: boolean
  isOpen: boolean
  onClick: () => void
}

export function KnowledgeGraphButton({ isEnabled, isOpen, onClick }: KnowledgeGraphButtonProps) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant={isOpen ? "default" : "outline"}
            size="icon"
            onClick={onClick}
            disabled={!isEnabled}
            className="relative"
          >
            <Network className="w-4 h-4" />
          </Button>
        </TooltipTrigger>
        {!isEnabled && (
          <TooltipContent side="left">
            <p>Upload and process a document to view the Knowledge Graph</p>
          </TooltipContent>
        )}
      </Tooltip>
    </TooltipProvider>
  )
}
