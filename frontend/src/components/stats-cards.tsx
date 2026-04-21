"use client"

import { Card, CardContent } from "./ui/card"
import { MessageSquare, Users, TrendingUp, Shield } from "lucide-react"

interface StatsCardsProps {
  stats: {
    totalMessages: number
    totalUsers: number
    successRate: number
    blockedRequests: number
  }
}

export function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      title: "Total Messages",
      value: stats.totalMessages,
      icon: MessageSquare,
      color: "text-blue-600",
      bg: "bg-blue-50",
    },
    {
      title: "Active Users",
      value: stats.totalUsers,
      icon: Users,
      color: "text-green-600",
      bg: "bg-green-50",
    },
    {
      title: "Success Rate",
      value: `${stats.successRate}%`,
      icon: TrendingUp,
      color: "text-purple-600",
      bg: "bg-purple-50",
    },
    {
      title: "Blocked Requests",
      value: stats.blockedRequests,
      icon: Shield,
      color: "text-red-600",
      bg: "bg-red-50",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <Card key={card.title}>
          <CardContent className="flex items-center gap-4 py-6">
            <div className={`p-3 rounded-lg ${card.bg}`}>
              <card.icon className={`w-6 h-6 ${card.color}`} />
            </div>
            <div>
              <p className="text-sm text-gray-600">{card.title}</p>
              <p className="text-2xl font-bold text-gray-900">{card.value}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
