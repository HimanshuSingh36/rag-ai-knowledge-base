import Navbar from "@/components/navbar";
import { Button } from "@/components/moving-border";
import { Spotlight } from "@/components/spotlight";
import Features from "@/components/features";
import HowItWorks from "@/components/how-it-works";
import CTA from "@/components/cta";
import Footer from "@/components/footer";
import Link from "next/link";

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-black text-white">
      <Navbar />

      <Spotlight
        className="-top-40 left-0 md:-top-20 md:left-60"
        fill="white"
      />

      {/* HERO SECTION */}
      <section className="relative z-10 flex min-h-screen flex-col items-center justify-center px-6 pt-20">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-neutral-500">
          AI Knowledge Base
        </p>

        <h1 className="max-w-4xl text-center text-5xl font-bold leading-tight tracking-tight md:text-6xl lg:text-7xl">
          Ask your documents.
        </h1>

        <p className="mt-6 max-w-2xl text-center text-lg text-neutral-400">
          Upload your documents, ask questions, and get intelligent answers
          backed by your own knowledge base.
        </p>

        <div className="mt-10 flex gap-4">
          <Link href="/chat" className="cursor-pointer">
            <Button>Start Chatting</Button>
          </Link>

          <Link
            href="/chat"
            className="rounded-lg border border-neutral-700 px-6 py-3 font-medium text-white transition hover:bg-neutral-900"
          >
            Upload Documents
          </Link>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <Features />
      <HowItWorks />
      <CTA />
      <Footer />
    </main>
  );
}
