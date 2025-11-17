"use client"

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { ConversationStyle, CONVERSATION_STYLES } from "@/types"

interface StyleSelectorProps {
  value: ConversationStyle
  onChange: (value: ConversationStyle) => void
}

export function StyleSelector({ value, onChange }: StyleSelectorProps) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-muted-foreground">Style:</span>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="w-[180px]">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {CONVERSATION_STYLES.map((style) => (
            <SelectItem key={style.value} value={style.value}>
              <div className="flex flex-col">
                <span className="font-medium">{style.label}</span>
                <span className="text-xs text-muted-foreground">{style.description}</span>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
