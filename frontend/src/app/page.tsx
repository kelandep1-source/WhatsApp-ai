"use client"

import { useState, useEffect } from "react"
import { Sidebar } from "@/components/sidebar"
import { StatsCards } from "@/components/stats-cards"
import { ActivityChart } from "@/components/activity-chart"
import { ConversationsList } from "@/components/conversations-list"
import { LogsViewer } from "@/components/logs-viewer"
import { SettingsPanel } from "@/components/settings-panel"
import { UsersManagement } from "@/components/users-management"
import { ProvidersStatus } from "@/components/providers-status"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { formatNumber } from "@/lib/utils"
import { 
  Users, 
  MessageCircle, 
  TrendingUp, 
  Clock,
  Globe,
  Smartphone,
  Bot,
  Shield,
  Zap
} from "lucide-react"

type Tab = "overview" | "conversations" | "analytics" | "logs" | "settings" | "users"

// Demo data
const demoStats = {
  totalMessages: 1247,
  totalUsers: 89,
  successRate: 98.5,
  blockedRequests: 12
}

const demoActivity = [
  { date: "Mon", messages: 45, users: 12 },
  { date: "Tue", messages: 78, users: 18 },
  { date: "Wed", messages: 120, users: 25 },
  { date: "Thu", messages: 95, users: 20 },
  { date: "Fri", messages: 140, users: 30 },
  { date: "Sat", messages: 85, users: 15 },
  { date: "Sun", messages: 60, users: 10 },
]

const demoConversations = [
  {
    id: "1",
    phone_number: "+509 34XX XXXX",
    name: "Jean Pierre",
    last_message: "Mesi anpil pou ed ou a!",
    last_message_time: "2026-04-21T14:30:00Z",
    message_count: 24,
    is_group: false
  },
  {
    id: "2", 
    phone_number: "+1 305 XXX XXXX",
    name: "Maria Santos",
    last_message: "How do I reset my password?",
    last_message_time: "2026-04-21T13:15:00Z",
    message_count: 8,
    is_group: false
  },
  {
    id: "3",
    phone_number: "+509 31XX XXXX",
    name: "Family Group",
    last_message: "@HaitianBot what is the weather?",
    last_message_time: "2026-04-21T12:00:00Z",
    message_count: 156,
    is_group: true
  }
]

const demoLogs = [
  {
    id: "1",
    timestamp: "2026-04-21T14:30:00Z",
    level: "info" as const,
    message: "Message processed successfully",
    details: "Provider: groq, Model: llama-4",
    phone_number: "+509 34XX XXXX"
  },
  {
    id: "2",
    timestamp: "2026-04-21T14:25:00Z",
    level: "blocked" as const,
    message: "Medical advice request blocked",
    details: "Category: medical",
    phone_number: "+1 305 XXX XXXX"
  },
  {
    id: "3",
    timestamp: "2026-04-21T14:20:00Z",
    level: "warning" as const,
    message: "Groq rate limited, fallback to Gemini",
    details: "Retry after: 30s"
  },
  {
    id: "4",
    timestamp: "2026-04-21T14:15:00Z",
    level: "error" as const,
    message: "Failed to send message",
    details: "WhatsApp API error: 400",
    phone_number: "+509 31XX XXXX"
  }
]

const demoSettings = {
  bot_name: "HaitianBot",
  personality: "You are HaitianBot, a warm, playful, and intelligent AI assistant...",
  max_history: 20,
  enable_memory: true,
  enable_images: true,
  enable_safety: true
}

const demoUsers = [
  {
    id: "1",
    phone_number: "+509 34XX XXXX",
    name: "Jean Pierre",
    message_count: 24,
    first_seen: "2026-04-15T10:00:00Z",
    last_active: "2026-04-21T14:30:00Z",
    is_blocked: false,
    country: "HT"
  },
  {
    id: "2",
    phone_number: "+1 305 XXX XXXX",
    name: "Maria Santos",
    message_count: 8,
    first_seen: "2026-04-18T15:00:00Z",
    last_active: "2026-04-21T13:15:00Z",
    is_blocked: false,
    country: "US"
  },
  {
    id: "3",
    phone_number: "+509 31XX XXXX",
    name: "Spam User",
    message_count: 156,
    first_seen: "2026-04-10T08:00:00Z",
    last_active: "2026-04-21T12:00:00Z",
    is_blocked: true,
    country: "HT"
  }
]

const demoProviders = [
  {
    name: "Groq",
    status: "online" as const,
    model: "Llama 4 Maverick",
    last_used: "2 min ago",
    success_rate: 99.2,
    avg_response_time: "1.2s"
  },
  {
    name: "Gemini",
    status: "online" as const,
    model: "Gemini 2.5 Pro",
    last_used: "15 min ago",
    success_rate: 98.8,
    avg_response_time: "2.1s"
  },
  {
    name: "OpenAI",
    status: "degraded" as const,
    model: "GPT-4o",
    last_used: "1 hour ago",
    success_rate: 95.5,
    avg_response_time: "3.5s"
  }
]

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<Tab>("overview")
  const [stats, setStats] = useState(demoStats)

  const renderContent = () => {
    switch (activeTab) {
      case "overview":
        return (
          <div className="space-y-6">
            <StatsCards stats={stats} />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    Activity (Last 7 Days)
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ActivityChart data={demoActivity} />
                </CardContent>
              </Card>

              <ProvidersStatus providers={demoProviders} />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ConversationsList conversations={demoConversations} />
              <LogsViewer logs={demoLogs.slice(0, 3)} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="flex items-center gap-4 py-6">
                  <Clock className="w-8 h-8 text-blue-500" />
                  <div>
                    <p className="text-sm text-gray-600">Avg Response Time</p>
                    <p className="text-2xl font-bold">2.3s</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="flex items-center gap-4 py-6">
                  <Globe className="w-8 h-8 text-purple-500" />
                  <div>
                    <p className="text-sm text-gray-600">Countries</p>
                    <p className="text-2xl font-bold">4</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="flex items-center gap-4 py-6">
                  <Smartphone className="w-8 h-8 text-orange-500" />
                  <div>
                    <p className="text-sm text-gray-600">Group Chats</p>
                    <p className="text-2xl font-bold">12</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="flex items-center gap-4 py-6">
                  <Shield className="w-8 h-8 text-red-500" />
                  <div>
                    <p className="text-sm text-gray-600">Blocked Today</p>
                    <p className="text-2xl font-bold">3</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )

      case "conversations":
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">All Conversations</h2>
            <ConversationsList conversations={[...demoConversations, ...demoConversations]} />
          </div>
        )

      case "analytics":
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Analytics</h2>
            <StatsCards stats={stats} />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Messages Over Time</CardTitle>
                </CardHeader>
                <CardContent>
                  <ActivityChart data={demoActivity} />
                </CardContent>
              </Card>
              <ProvidersStatus providers={demoProviders} />
            </div>
          </div>
        )

      case "logs":
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">System Logs</h2>
            <LogsViewer logs={demoLogs} />
          </div>
        )

      case "settings":
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Bot Settings</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="max-w-2xl">
                <SettingsPanel 
                  currentSettings={demoSettings} 
                  onSave={(s) => console.log("Save:", s)} 
                />
              </div>
              <ProvidersStatus providers={demoProviders} />
            </div>
          </div>
        )

      case "users":
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">User Management</h2>
            <UsersManagement users={demoUsers} />
          </div>
        )
    }
  }

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="flex-1 p-8 overflow-auto">
        {renderContent()}
      </main>
    </div>
  )
}
