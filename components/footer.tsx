"use client";
import Link from "next/link";

const productLinks = [
  { label: "Features", href: "#features" },
  { label: "How It Works", href: "#how-it-works" },
  { label: "Start Chatting", href: "/chat" },
];

const resourceLinks = [
  { label: "Documentation", href: "#" },
  {
    label: "GitHub",
    href: "https://github.com/HimanshuSingh36/rag-ai-knowledge-base",
  },
];

export default function Footer() {
  return (
    <footer className="relative z-10 border-t border-white/[0.08]">
      <div className="mx-auto max-w-6xl px-6 py-16 md:py-20">
        <div className="grid gap-12 md:grid-cols-2 lg:grid-cols-4">
          {/* Brand */}
          <div className="lg:col-span-2">
            <Link
              href="/"
              className="text-lg font-semibold tracking-tight text-white"
            >
              AI Knowledge Base
            </Link>

            <p className="mt-4 max-w-sm text-sm leading-6 text-neutral-500">
              Turn your documents into an intelligent knowledge base. Ask
              questions and get answers grounded in your own information.
            </p>

            <div className="mt-6 flex items-center gap-3">
              <a
                href="https://github.com/HimanshuSingh36/rag-ai-knowledge-base"
                target="_blank"
                rel="noopener noreferrer"
                className="flex h-9 items-center rounded-lg border border-white/10 px-3 text-xs text-neutral-500 transition hover:border-white/20 hover:bg-white/[0.04] hover:text-white"
              >
                GitHub
              </a>

              <a
                href="#"
                className="flex h-9 items-center rounded-lg border border-white/10 px-3 text-xs text-neutral-500 transition hover:border-white/20 hover:bg-white/[0.04] hover:text-white"
              >
                LinkedIn
              </a>
            </div>
          </div>

          {/* Product */}
          <div>
            <h3 className="text-sm font-medium text-white">Product</h3>

            <ul className="mt-5 space-y-3">
              {productLinks.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-sm text-neutral-500 transition hover:text-white"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-sm font-medium text-white">Resources</h3>

            <ul className="mt-5 space-y-3">
              {resourceLinks.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-neutral-500 transition hover:text-white"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-16 flex flex-col gap-4 border-t border-white/[0.08] pt-6 text-sm text-neutral-600 md:flex-row md:items-center md:justify-between">
          <p>
            © {new Date().getFullYear()} AI Knowledge Base. All rights reserved.
          </p>

          <p>Built with Next.js</p>
        </div>
      </div>
    </footer>
  );
}
