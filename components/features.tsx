"use client";

import { features } from "@/lib/features";
import { HoverEffect } from "@/components/card-hover";

export default function Features() {
  return (
    <section
      id="features"
      className="scroll-mt-24 relative z-10 border-t border-white/[0.08] px-6 py-28 md:py-32"
    >
      <div className="mx-auto max-w-6xl">

        {/* Heading */}
        <div className="mx-auto mb-10 max-w-2xl text-center">
          <p className="text-sm uppercase tracking-[0.3em] text-neutral-500">
            Powerful features
          </p>

          <h2 className="mt-4 text-3xl font-bold tracking-tight md:text-4xl lg:text-5xl">
            Everything you need to{" "}
            <span className="text-neutral-500">
              work with your knowledge.
            </span>
          </h2>
        </div>

        {/* Aceternity cards */}
        <HoverEffect items={features} />

      </div>
    </section>
  );
}