import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";

type ChatMessageProps = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatMessage({
  role,
  content,
}: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        "flex",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6",
          isUser
            ? "bg-white text-black"
            : "border border-white/10 bg-white/[0.04] text-neutral-200"
        )}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{content}</p>
        ) : (
          <div className="prose prose-invert max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => (
                  <h1 className="mb-4 mt-2 text-xl font-semibold text-white">
                    {children}
                  </h1>
                ),

                h2: ({ children }) => (
                  <h2 className="mb-3 mt-5 text-lg font-semibold text-white">
                    {children}
                  </h2>
                ),

                h3: ({ children }) => (
                  <h3 className="mb-2 mt-4 text-base font-semibold text-white">
                    {children}
                  </h3>
                ),

                p: ({ children }) => (
                  <p className="mb-3 last:mb-0">
                    {children}
                  </p>
                ),

                ul: ({ children }) => (
                  <ul className="mb-3 ml-5 list-disc space-y-1">
                    {children}
                  </ul>
                ),

                ol: ({ children }) => (
                  <ol className="mb-3 ml-5 list-decimal space-y-1">
                    {children}
                  </ol>
                ),

                li: ({ children }) => (
                  <li className="pl-1">
                    {children}
                  </li>
                ),

                strong: ({ children }) => (
                  <strong className="font-semibold text-white">
                    {children}
                  </strong>
                ),

                code: ({ children }) => (
                  <code className="rounded-md bg-black/40 px-1.5 py-0.5 text-[0.9em] text-neutral-200">
                    {children}
                  </code>
                ),

                pre: ({ children }) => (
                  <pre className="my-4 overflow-x-auto rounded-xl border border-white/10 bg-black/50 p-4 text-sm">
                    {children}
                  </pre>
                ),

                blockquote: ({ children }) => (
                  <blockquote className="my-3 border-l-2 border-white/20 pl-4 text-neutral-400">
                    {children}
                  </blockquote>
                ),

                a: ({ children, href }) => (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-white underline underline-offset-4 hover:text-neutral-300"
                  >
                    {children}
                  </a>
                ),
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}