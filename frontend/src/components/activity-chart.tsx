"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

interface ActivityChartProps {
  data: Array<{
    date: string
    messages: number
    users: number
  }>
}

export function ActivityChart({ data }: ActivityChartProps) {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="date" stroke="#888" fontSize={12} />
          <YAxis stroke="#888" fontSize={12} />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: "white", 
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
              boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)"
            }} 
          />
          <Line 
            type="monotone" 
            dataKey="messages" 
            stroke="#22c55e" 
            strokeWidth={2}
            dot={{ fill: "#22c55e", strokeWidth: 2 }}
            name="Messages"
          />
          <Line 
            type="monotone" 
            dataKey="users" 
            stroke="#3b82f6" 
            strokeWidth={2}
            dot={{ fill: "#3b82f6", strokeWidth: 2 }}
            name="Users"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
