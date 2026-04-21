"use client"

import { Card, CardHeader, CardTitle, CardContent } from "./ui/card"
import { formatDate } from "@/lib/utils"
import { MessageCircle, User, Bot } from "lucide-react"

interface Conversation {
  id: string
  phone_number: string
  name: string
  last_message: string
  last_message_time: string
  message_count: number
  is_group: boolean
}

interface ConversationsListProps {
  conversations: Conversation[]
}

export function ConversationsList({ conversations }: ConversationsListProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="w-5 h-5 text-blue-600" />
          Recent Conversations
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-[400px] overflow-y-auto">
          {conversations.map((conv) => (
            <div 
              key={conv.id} 
              className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer border border-gray-100"
            >
              <div className={`p-2 rounded-full ${conv.is_group ? 'bg-purple-100' : 'bg-blue-100'}`}>
                {conv.is_group ? (
                  <User className="w-4 h-4 text-purple-600" />
                ) : (
                  <User className="w-4 h-4 text-blue-600" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="font-medium text-gray-900 truncate">
                    {conv.name || conv.phone_number}
                    {conv.is_group && (
                      <span className="ml-2 text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">
                        Group
                      </span>
                    )}
                  </p>
                  <span className="text-xs text-gray-500">
                    {formatDate(conv.last_message_time)}
                  </span>
                </div>
                <p className="text-sm text-gray-600 truncate mt-1">
                  {conv.last_message}
                </p>
                <div className="flex items-center gap-2 mt-2">
                  <span className="text-xs text-gray-500">
                    {conv.message_count} messages
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
