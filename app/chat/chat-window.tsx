"use client";

import { useRef, useState } from "react";
import { ArrowUp, Paperclip } from "lucide-react";
import ChatMessage from "./chat-message";

export default function ChatWindow() {
  type Message = {
    id: string;
    role: "user" | "assistant";
    content: string;
  };
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const typeAssistantMessage = (content: string, messageId: string) => {
    let index = 0;

    setMessages((currentMessages) => [
      ...currentMessages,
      {
        id: messageId,
        role: "assistant",
        content: "",
      },
    ]);

    const interval = setInterval(() => {
      index++;

      setMessages((currentMessages) =>
        currentMessages.map((message) =>
          message.id === messageId
            ? {
                ...message,
                content: content.slice(0, index),
              }
            : message,
        ),
      );

      if (index >= content.length) {
        clearInterval(interval);
        setIsLoading(false);
      }
    }, 15);
  };

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      alert("Only PDF files are currently supported.");
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/documents`,
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        throw new Error(`Upload failed with status ${response.status}`);
      }

      const data = await response.json();

      console.log("Document uploaded:", data);

      setDocumentId(data.document_id);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: `${file.name} uploaded successfully. You can now ask questions about this document.`,
        },
      ]);
    } catch (error) {
      console.error("Document upload failed:", error);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            error instanceof Error
              ? `Upload failed: ${error.message}`
              : "Document upload failed.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = async () => {
    const message = input.trim();

    if (!message || isLoading) return;

    const newMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    };

    setMessages((currentMessages) => [...currentMessages, newMessage]);

    setInput("");
    setIsLoading(true);

    try {
      console.log("API URL:", `${process.env.NEXT_PUBLIC_API_URL}/api/chat`);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message,
            document_id: documentId,
          }),
        },
      );

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();

      typeAssistantMessage(data.response, crypto.randomUUID());
    } catch (error) {
      console.error("Chat request failed:", error);

      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          error instanceof Error
            ? `Request failed: ${error.message}`
            : "Request failed. Please try again.",
      };

      setMessages((currentMessages) => [...currentMessages, errorMessage]);

      setIsLoading(false);
    }
  };

  return (
    <section className="flex min-w-0 flex-1 flex-col">
      {/* Header */}
      <header className="flex h-16 shrink-0 items-center border-b border-white/[0.08] px-6">
        <div>
          <p className="text-sm font-medium text-white">New conversation</p>

          <p className="mt-0.5 text-xs text-neutral-600">
            Ask questions about your knowledge base
          </p>
        </div>
      </header>

      {/* Chat content */}
      <div className="flex min-h-0 flex-1 flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-8">
          <div className="mx-auto max-w-3xl space-y-6">
            {messages.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <div className="w-full max-w-2xl text-center">
                  <p className="text-xs uppercase tracking-[0.3em] text-neutral-600">
                    AI Knowledge Base
                  </p>

                  <h1 className="mt-4 text-3xl font-semibold tracking-tight md:text-4xl">
                    What would you like to know?
                  </h1>

                  <p className="mx-auto mt-4 max-w-lg text-sm leading-6 text-neutral-500">
                    Ask a question about your documents and get an answer
                    grounded in your knowledge base.
                  </p>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  role={message.role}
                  content={message.content}
                />
              ))
            )}

            {isLoading && (
              <div className="flex justify-start">
                <div className="rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3 text-sm text-neutral-500">
                  Thinking...
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Input */}
        <div className="border-t border-white/[0.08] p-4">
          <div className="mx-auto max-w-3xl">
            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-2 transition focus-within:border-white/20">
              <div className="flex items-end gap-2">
                <label
                  className="flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-xl text-neutral-500 transition hover:bg-white/[0.05] hover:text-white"
                  aria-label="Attach document"
                >
                  <Paperclip className="h-4 w-4" />

                  <input
                    type="file"
                    accept="application/pdf"
                    className="hidden"
                    onChange={handleUpload}
                  />
                </label>

                <textarea
                  rows={1}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  placeholder="Ask anything about your documents..."
                  className="max-h-32 min-h-10 flex-1 resize-none bg-transparent px-1 py-2.5 text-sm text-white outline-none placeholder:text-neutral-600"
                />

                <button
                  type="button"
                  onClick={handleSend}
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
      </div>
    </section>
  );
}
