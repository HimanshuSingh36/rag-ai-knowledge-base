"use client";

import { ArrowUp, Paperclip } from "lucide-react";

export default function ChatWindow() {
  return (
    <section className="flex min-w-0 flex-1 flex-col">
      {/* Header */}
      <header className="flex h-16 shrink-0 items-center border-b border-white/[0.08] px-6">
        <div>
          <p className="text-sm font-medium text-white">
            New conversation
          </p>

          <p className="mt-0.5 text-xs text-neutral-600">
            Ask questions about your knowledge base
          </p>
        </div>
      </header>

      {/* Empty state */}
      <div className="flex flex-1 items-center justify-center px-6">
        <div className="w-full max-w-2xl">
          <div className="text-center">
            <p className="text-xs uppercase tracking-[0.3em] text-neutral-600">
              AI Knowledge Base
            </p>

            <h1 className="mt-4 text-3xl font-semibold tracking-tight md:text-4xl">
              What would you like to know?
            </h1>

            <p className="mx-auto mt-4 max-w-lg text-sm leading-6 text-neutral-500">
              Ask a question about your documents and get an
              answer grounded in your knowledge base.
            </p>
          </div>

          {/* Input */}
          <div className="mt-8 rounded-2xl border border-white/10 bg-white/[0.03] p-2 transition focus-within:border-white/20">
            <div className="flex items-end gap-2">
              <button
                type="button"
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-neutral-500 transition hover:bg-white/[0.05] hover:text-white"
                aria-label="Attach document"
              >
                <Paperclip className="h-4 w-4" />
              </button>

              <textarea
                rows={1}
                placeholder="Ask anything about your documents..."
                className="max-h-32 min-h-10 flex-1 resize-none bg-transparent px-1 py-2.5 text-sm text-white outline-none placeholder:text-neutral-600"
              />

              <button
                type="button"
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-black transition hover:bg-neutral-200"
                aria-label="Send message"
              >
                <ArrowUp className="h-4 w-4" />
              </button>
            </div>
          </div>

          <p className="mt-3 text-center text-xs text-neutral-700">
            Answers are generated from your connected knowledge base.
          </p>
        </div>
      </div>
    </section>
  );
}