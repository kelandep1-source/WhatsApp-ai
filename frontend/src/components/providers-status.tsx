"use client"

import { Card, CardHeader, CardTitle, CardContent } from "./ui/card"
import { CheckCircle, XCircle, AlertTriangle, Zap } from "lucide-react"

interface Provider {
  name: string
  status: "online" | "offline" | "degraded"
  model: string
  last_used: string
  success_rate: number
  avg_response_time: string
}

interface ProvidersStatusProps {
  providers: Provider[]
}

export function ProvidersStatus({ providers }: ProvidersStatusProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case "online":
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case "degraded":
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />
      default:
        return <XCircle className="w-5 h-5 text-red-500" />
    }
  }

  const getStatusBg = (status: string) => {
    switch (status) {
      case "online":
        return "bg-green-50 border-green-200"
      case "degraded":
        return "bg-yellow-50 border-yellow-200"
      default:
        return "bg-red-50 border-red-200"
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-yellow-500" />
          AI Providers Status
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {providers.map((provider) => (
            <div 
              key={provider.name} 
              className={`flex items-center justify-between p-4 rounded-lg border ${getStatusBg(provider.status)}`}
            >
              <div className="flex items-center gap-4">
                {getStatusIcon(provider.status)}
                <div>
                  <p className="font-medium text-gray-900">{provider.name}</p>
                  <p className="text-sm text-gray-500">{provider.model}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-gray-700">{provider.success_rate}% success</p>
                <p className="text-xs text-gray-500">{provider.avg_response_time} avg response</p>
                <p className="text-xs text-gray-400">Last used: {provider.last_used}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
