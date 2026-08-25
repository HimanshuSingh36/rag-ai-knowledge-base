"use client";

import { Menu } from "lucide-react";
import ChatSidebar from "./chat-sidebar";
import ChatWindow from "./chat-window";


export default function ChatPage() {
  return (
    <main className="flex h-screen overflow-hidden bg-black text-white">
      <ChatSidebar/>
      <ChatWindow/>
    </main>
  );
}