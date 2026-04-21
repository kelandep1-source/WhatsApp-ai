"use client"

import { Card, CardHeader, CardTitle, CardContent } from "./ui/card"
import { formatDate } from "@/lib/utils"
import { User, Ban, CheckCircle, MessageSquare, Clock } from "lucide-react"

interface UserData {
  id: string
  phone_number: string
  name: string
  message_count: number
  first_seen: string
  last_active: string
  is_blocked: boolean
  country: string
}

interface UsersManagementProps {
  users: UserData[]
}

export function UsersManagement({ users }: UsersManagementProps) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="flex items-center gap-4 py-6">
            <User className="w-8 h-8 text-blue-500" />
            <div>
              <p className="text-sm text-gray-600">Total Users</p>
              <p className="text-2xl font-bold">{users.length}</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-4 py-6">
            <CheckCircle className="w-8 h-8 text-green-500" />
            <div>
              <p className="text-sm text-gray-600">Active</p>
              <p className="text-2xl font-bold">{users.filter(u => !u.is_blocked).length}</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-4 py-6">
            <Ban className="w-8 h-8 text-red-500" />
            <div>
              <p className="text-sm text-gray-600">Blocked</p>
              <p className="text-2xl font-bold">{users.filter(u => u.is_blocked).length}</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-4 py-6">
            <Clock className="w-8 h-8 text-purple-500" />
            <div>
              <p className="text-sm text-gray-600">New Today</p>
              <p className="text-2xl font-bold">{users.filter(u => {
                const today = new Date().toISOString().split('T')[0]
                return u.first_seen.startsWith(today)
              }).length}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Users</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">User</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Phone</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Messages</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">First Seen</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Last Active</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Status</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                          <User className="w-4 h-4 text-blue-600" />
                        </div>
                        <span className="font-medium text-gray-900">{user.name}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-600">{user.phone_number}</td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center gap-1 text-sm">
                        <MessageSquare className="w-4 h-4 text-gray-400" />
                        {user.message_count}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-500">{formatDate(user.first_seen)}</td>
                    <td className="py-3 px-4 text-sm text-gray-500">{formatDate(user.last_active)}</td>
                    <td className="py-3 px-4">
                      {user.is_blocked ? (
                        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-red-100 text-red-700">
                          <Ban className="w-3 h-3" />
                          Blocked
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-green-100 text-green-700">
                          <CheckCircle className="w-3 h-3" />
                          Active
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                        {user.is_blocked ? "Unblock" : "Block"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
