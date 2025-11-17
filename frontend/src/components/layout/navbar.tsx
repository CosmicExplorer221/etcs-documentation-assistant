"use client"

import { Button } from "@/components/ui/button"
import { Menu, Search, Settings, User } from "lucide-react"

interface NavbarProps {
  onToggleSidebar: () => void
}

export function Navbar({ onToggleSidebar }: NavbarProps) {
  return (
    <nav className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
        >
          <Menu className="h-5 w-5" />
        </Button>

        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <span className="text-lg font-bold">E</span>
          </div>
          <div>
            <h1 className="text-lg font-semibold">ETCS Documentation Assistant</h1>
            <p className="text-xs text-muted-foreground">AI-Powered Railway Engineering Platform</p>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" aria-label="Search">
          <Search className="h-5 w-5" />
        </Button>

        <Button variant="ghost" size="icon" aria-label="Settings">
          <Settings className="h-5 w-5" />
        </Button>

        <Button variant="ghost" size="icon" aria-label="User profile">
          <User className="h-5 w-5" />
        </Button>
      </div>
    </nav>
  )
}
