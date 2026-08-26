"use client";
import Link from "next/link";
import { Plus, Search } from "lucide-react";

type Chat = {
  id: string;
  title: string;
};

const recentChats: Chat[] = [
  {
    id: "1",
    title: "Project documentation",
  },
  {
    id: "2",
    title: "Research notes",
  },
  {
    id: "3",
    title: "Product requirements",
  },
];

export default function ChatSidebar() {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-white/[0.08] bg-white/[0.02] md:flex md:flex-col">
      {/* Logo */}
      <div className="flex h-16 items-center border-b border-white/[0.08] px-5">
        <Link
          href="/"
          className="font-semibold tracking-tight transition hover:text-neutral-300"
        >
          AI Knowledge Base
        </Link>
      </div>

      {/* New Chat */}
      <div className="p-4">
        <button className="flex w-full items-center gap-2 rounded-xl border border-white/10 bg-white/[0.04] px-4 py-3 text-sm font-medium transition hover:bg-white/[0.08]">
          <Plus className="h-4 w-4" />
          New Chat
        </button>
      </div>

      {/* Search */}
      <div className="px-4">
        <div className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/[0.02] px-3 py-2.5">
          <Search className="h-4 w-4 text-neutral-500" />

          <input
            type="text"
            placeholder="Search chats..."
            className="w-full bg-transparent text-sm text-white outline-none placeholder:text-neutral-600"
          />
        </div>
      </div>

      {/* Recent chats */}
      <div className="mt-6 flex-1 overflow-y-auto px-4">
        <p className="px-2 text-xs font-medium uppercase tracking-wider text-neutral-600">
          Recent
        </p>

        <div className="mt-3 space-y-1">
          {recentChats.map((chat) => (
            <button
              key={chat.id}
              className="w-full rounded-lg px-3 py-2.5 text-left text-sm text-neutral-400 transition hover:bg-white/[0.04] hover:text-white"
            >
              {chat.title}
            </button>
          ))}
        </div>
      </div>

      {/* Bottom */}
      <div className="border-t border-white/[0.08] p-4">
        <div className="rounded-xl bg-white/[0.03] p-3">
          <p className="text-xs text-neutral-500">Knowledge Base</p>

          <p className="mt-1 text-sm text-neutral-300">12 documents</p>
        </div>
      </div>
    </aside>
  );
}
