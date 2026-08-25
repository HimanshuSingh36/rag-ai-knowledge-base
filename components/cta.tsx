"use client";

import { ArrowRight } from "lucide-react";
import { motion } from "motion/react";
import { Button } from "@/components/moving-border";

export default function CTA() {
  return (
    <section className="relative z-10 px-6 py-24 md:py-32">
      <div className="relative mx-auto max-w-5xl overflow-hidden rounded-3xl border border-white/10 bg-white/[0.02]">
        {/* Subtle background */}
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white/[0.04] blur-3xl" />
        </div>

        <div className="relative px-6 py-20 text-center md:px-12 md:py-24">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-sm uppercase tracking-[0.3em] text-neutral-500">
              Start exploring
            </p>

            <h2 className="mx-auto mt-5 max-w-3xl text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl">
              Your documents have
              <span className="block text-neutral-500">
                more to say.
              </span>
            </h2>

            <p className="mx-auto mt-6 max-w-xl text-base leading-7 text-neutral-400 md:text-lg">
              Stop searching through documents manually.
              Ask questions and let your knowledge base find
              the answers.
            </p>

            <div className="mt-10 flex justify-center">
              <Button
                containerClassName="h-14 w-48"
                className="gap-2"
              >
                Start Chatting
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}