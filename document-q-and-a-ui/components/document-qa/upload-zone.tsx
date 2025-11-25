"use client"

import { useDropzone } from "react-dropzone"
import { Upload } from "lucide-react"
import { ProcessingAnimation } from "./processing-animation"

interface UploadZoneProps {
  onFileSelect: (file: File) => void
  isUploading: boolean
  uploadingFileId: string | null
}

export function UploadZone({ onFileSelect, isUploading, uploadingFileId }: UploadZoneProps) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "application/pdf": [".pdf"],
    },
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0])
      }
    },
    disabled: isUploading,
  })

  if (isUploading) {
    return <ProcessingAnimation fileId={uploadingFileId} />
  }

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
        isDragActive ? "border-primary bg-primary/5" : "border-border hover:border-primary/50 hover:bg-primary/5"
      } ${isUploading ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
    >
      <input {...getInputProps()} />
      <Upload className="w-8 h-8 mx-auto mb-3 text-muted-foreground" />
      <p className="text-sm font-medium mb-1">Drag and drop your PDF here</p>
      <p className="text-xs text-muted-foreground">or click to browse from your computer</p>
      <p className="text-xs text-muted-foreground mt-3">PDF only for now</p>
    </div>
  )
}
