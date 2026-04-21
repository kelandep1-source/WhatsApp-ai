"use client"

import { Card, CardHeader, CardTitle, CardContent } from "./ui/card"
import { formatDate } from "@/lib/utils"
import { ScrollText, AlertTriangle, Ban, CheckCircle } from "lucide-react"

interface LogEntry {
  id: string
  timestamp: string
  level: "info" | "warning" | "error" | "blocked"
  message: string
  details?: string
  phone_number?: string
}

interface LogsViewerProps {
  logs: LogEntry[]
}

export function LogsViewer({ logs }: LogsViewerProps) {
  const getIcon = (level: string) => {
    switch (level) {
      case "error":
        return <AlertTriangle className="w-4 h-4 text-red-500" />
      case "warning":
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />
      case "blocked":
        return <Ban className="w-4 h-4 text-orange-500" />
      default:
        return <CheckCircle className="w-4 h-4 text-green-500" />
    }
  }

  const getBgColor = (level: string) => {
    switch (level) {
      case "error":
        return "bg-red-50 border-red-200"
      case "warning":
        return "bg-yellow-50 border-yellow-200"
      case "blocked":
        return "bg-orange-50 border-orange-200"
      default:
        return "bg-gray-50 border-gray-200"
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <ScrollText className="w-5 h-5 text-gray-600" />
          System Logs
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 max-h-[400px] overflow-y-auto">
          {logs.map((log) => (
            <div 
              key={log.id} 
              className={`flex items-start gap-3 p-3 rounded-lg border ${getBgColor(log.level)}`}
            >
              {getIcon(log.level)}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium uppercase text-gray-500">
                    {log.level}
                  </span>
                  <span className="text-xs text-gray-400">
                    {formatDate(log.timestamp)}
                  </span>
                </div>
                <p className="text-sm text-gray-800 mt-1">{log.message}</p>
                {log.details && (
                  <p className="text-xs text-gray-500 mt-1 font-mono">
                    {log.details}
                  </p>
                )}
                {log.phone_number && (
                  <p className="text-xs text-gray-400 mt-1">
                    From: {log.phone_number}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
