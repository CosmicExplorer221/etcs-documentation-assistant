import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "@/styles/globals.css"
import { Providers } from "./providers"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "ETCS Documentation Assistant",
  description: "AI-powered platform for railway engineers to interact with ETCS technical documentation",
  keywords: ["ETCS", "Railway", "Documentation", "AI Assistant", "Engineering"],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
