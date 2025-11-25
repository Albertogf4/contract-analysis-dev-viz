"use client"

import { motion } from "framer-motion"
import { useState, useEffect } from "react"

const steps = ["Parsing document…", "Chunking text…", "Generating embeddings…", "Building vector index…"]

interface ProcessingAnimationProps {
  fileId: string | null
}

export function ProcessingAnimation({ fileId }: ProcessingAnimationProps) {
  const [activeStep, setActiveStep] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % steps.length)
    }, 1500)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="border-2 border-dashed border-primary rounded-lg p-8 bg-primary/5 min-h-60 flex items-center justify-center">
      <div className="w-full max-w-xs">
        {/* Neural Network Animation */}
        <div className="relative h-32 mb-6 flex items-center justify-center">
          <svg className="w-full h-full" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
            {/* Background nodes */}
            {[
              { cx: 30, cy: 30, r: 4 },
              { cx: 170, cy: 30, r: 4 },
              { cx: 100, cy: 60, r: 4 },
              { cx: 30, cy: 90, r: 4 },
              { cx: 170, cy: 90, r: 4 },
            ].map((node, i) => (
              <circle key={i} cx={node.cx} cy={node.cy} r={node.r} fill="currentColor" className="text-primary/30" />
            ))}

            {/* Animated connections */}
            {[
              { x1: 30, y1: 30, x2: 100, y2: 60 },
              { x1: 170, y1: 30, x2: 100, y2: 60 },
              { x1: 100, y1: 60, x2: 30, y2: 90 },
              { x1: 100, y1: 60, x2: 170, y2: 90 },
            ].map((line, i) => (
              <motion.line
                key={i}
                x1={line.x1}
                y1={line.y1}
                x2={line.x2}
                y2={line.y2}
                stroke="currentColor"
                strokeWidth="2"
                className="text-primary"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{
                  pathLength: [0, 1, 0],
                  opacity: [0, 1, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Number.POSITIVE_INFINITY,
                  delay: i * 0.4,
                }}
              />
            ))}

            {/* Central animated node */}
            <motion.circle
              cx="100"
              cy="60"
              r="6"
              fill="currentColor"
              className="text-primary"
              animate={{
                r: [6, 8, 6],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 1.5,
                repeat: Number.POSITIVE_INFINITY,
              }}
            />
          </svg>
        </div>

        {/* Step Indicators */}
        <div className="space-y-2">
          {steps.map((step, i) => (
            <motion.div
              key={step}
              className="flex items-center gap-3"
              animate={{
                opacity: activeStep === i ? 1 : 0.4,
                x: activeStep === i ? 4 : 0,
              }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                className={`w-2 h-2 rounded-full ${activeStep >= i ? "bg-primary" : "bg-border"}`}
                animate={{
                  scale: activeStep === i ? 1.3 : 1,
                }}
                transition={{ duration: 0.2 }}
              />
              <span className="text-sm font-medium text-foreground">{step}</span>
            </motion.div>
          ))}
        </div>

        {/* Progress bar */}
        <motion.div
          className="mt-4 h-1 bg-border rounded-full overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <motion.div
            className="h-full bg-primary rounded-full"
            animate={{ width: "100%" }}
            transition={{
              duration: 6,
              repeat: Number.POSITIVE_INFINITY,
              ease: "linear",
            }}
            initial={{ width: "0%" }}
          />
        </motion.div>
      </div>
    </div>
  )
}
