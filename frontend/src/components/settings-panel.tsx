"use client"

import { Card, CardHeader, CardTitle, CardContent } from "./ui/card"
import { useState } from "react"
import { Settings, Save, Bot, Brain, Image, Shield } from "lucide-react"

interface BotSettings {
  bot_name: string
  personality: string
  max_history: number
  enable_memory: boolean
  enable_images: boolean
  enable_safety: boolean
}

interface SettingsPanelProps {
  currentSettings: BotSettings
  onSave: (settings: BotSettings) => void
}

export function SettingsPanel({ currentSettings, onSave }: SettingsPanelProps) {
  const [settings, setSettings] = useState(currentSettings)
  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    onSave(settings)
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Settings className="w-5 h-5 text-gray-600" />
          Bot Settings
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Bot Name */}
          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
              <Bot className="w-4 h-4" />
              Bot Name
            </label>
            <input
              type="text"
              value={settings.bot_name}
              onChange={(e) => setSettings({ ...settings, bot_name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
            <p className="text-xs text-gray-500 mt-1">
              Used for @mentions in groups. Example: @{settings.bot_name}
            </p>
          </div>

          {/* Personality */}
          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
              <Brain className="w-4 h-4" />
              Personality / System Prompt
            </label>
            <textarea
              value={settings.personality}
              onChange={(e) => setSettings({ ...settings, personality: e.target.value })}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>

          {/* Max History */}
          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">
              Conversation Memory (messages)
            </label>
            <input
              type="number"
              min={5}
              max={50}
              value={settings.max_history}
              onChange={(e) => setSettings({ ...settings, max_history: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>

          {/* Toggles */}
          <div className="space-y-3">
            <label className="flex items-center justify-between p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
              <div className="flex items-center gap-2">
                <Brain className="w-4 h-4 text-blue-500" />
                <span className="text-sm font-medium">Long-term Memory</span>
              </div>
              <input
                type="checkbox"
                checked={settings.enable_memory}
                onChange={(e) => setSettings({ ...settings, enable_memory: e.target.checked })}
                className="w-5 h-5 text-green-600 rounded focus:ring-green-500"
              />
            </label>

            <label className="flex items-center justify-between p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
              <div className="flex items-center gap-2">
                <Image className="w-4 h-4 text-purple-500" />
                <span className="text-sm font-medium">Image Generation</span>
              </div>
              <input
                type="checkbox"
                checked={settings.enable_images}
                onChange={(e) => setSettings({ ...settings, enable_images: e.target.checked })}
                className="w-5 h-5 text-green-600 rounded focus:ring-green-500"
              />
            </label>

            <label className="flex items-center justify-between p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-red-500" />
                <span className="text-sm font-medium">Safety Filtering</span>
              </div>
              <input
                type="checkbox"
                checked={settings.enable_safety}
                onChange={(e) => setSettings({ ...settings, enable_safety: e.target.checked })}
                className="w-5 h-5 text-green-600 rounded focus:ring-green-500"
              />
            </label>
          </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
              saved
                ? "bg-green-500 text-white"
                : "bg-gray-900 text-white hover:bg-gray-800"
            }`}
          >
            <span className="flex items-center justify-center gap-2">
              <Save className="w-4 h-4" />
              {saved ? "Saved!" : "Save Settings"}
            </span>
          </button>
        </div>
      </CardContent>
    </Card>
  )
}
