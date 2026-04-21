"use client"

import { cn } from "@/lib/utils"
import { 
  LayoutDashboard, 
  MessageSquare, 
  BarChart3, 
  Settings, 
  Shield, 
  Users,
  Bot
} from "lucide-react"

type Tab = "overview" | "conversations" | "analytics" | "logs" | "settings" | "users"

interface SidebarProps {
  activeTab: Tab
  onTabChange: (tab: Tab) => void
}

const tabs = [
  { id: "overview" as Tab, label: "Overview", icon: LayoutDashboard },
  { id: "conversations" as Tab, label: "Conversations", icon: MessageSquare },
  { id: "analytics" as Tab, label: "Analytics", icon: BarChart3 },
  { id: "logs" as Tab, label: "System Logs", icon: Shield },
  { id: "users" as Tab, label: "Users", icon: Users },
  { id: "settings" as Tab, label: "Settings", icon: Settings },
]

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen flex flex-col">
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-green-500 rounded-lg">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg">HaitianBot</h1>
            <p className="text-xs text-gray-400">WhatsApp AI Dashboard</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <ul className="space-y-1">
          {tabs.map((tab) => (
            <li key={tab.id}>
              <button
                onClick={() => onTabChange(tab.id)}
                className={cn(
                  "w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                  activeTab === tab.id
                    ? "bg-green-600 text-white"
                    : "text-gray-400 hover:bg-gray-800 hover:text-white"
                )}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center gap-3 px-4 py-3">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-sm text-gray-400">Bot Online</span>
        </div>
      </div>
    </div>
  )
}
