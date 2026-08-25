"use client";
import { FileUp, Database, MessageSquare, Sparkles } from "lucide-react";
import { motion } from "motion/react";
// import { use } from "react";

const steps = [
  {
    number: "01",
    title: "Upload Documents",
    description:
      "Add your PDFs and documents to create your private knowledge base.",
    icon: FileUp,
  },
  {
    number: "02",
    title: "Process & Index",
    description:
      "Your documents are processed and converted into searchable knowledge.",
    icon: Database,
  },
  {
    number: "03",
    title: "Ask Questions",
    description:
      "Ask questions naturally and let the system find the most relevant information.",
    icon: MessageSquare,
  },
  {
    number: "04",
    title: "Get Grounded Answers",
    description:
      "Receive an answer based on your documents with relevant sources.",
    icon: Sparkles,
  },
];

export default function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="scroll-mt-24 relative z-10 border-t border-white/[0.08] px-6 py-28 md:py-32"
    >
      <div className="mx-auto max-w-6xl">
        {/* Heading */}
        <div className="mx-auto mb-16 max-w-2xl text-center">
          <p className="text-sm uppercase tracking-[0.3em] text-neutral-500">
            How it works
          </p>

          <h2 className="mt-4 text-3xl font-bold tracking-tight md:text-4xl lg:text-5xl">
            From documents to <span className="text-neutral-500">answers.</span>
          </h2>

          <p className="mt-5 text-neutral-400">
            A simple workflow that turns your documents into an intelligent
            knowledge base.
          </p>
        </div>

        {/* Steps */}
        <div className="relative grid gap-6 md:grid-cols-4">
          {/* Connecting line */}
          <div className="absolute left-[12.5%] right-[12.5%] top-8 hidden h-px overflow-hidden bg-white/10 md:block">
            <motion.div
              className="h-full w-1/3 bg-gradient-to-r from-transparent via-sky-500 to-transparent"
              animate={{
                x: ["-100%", "400%"],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: "linear",
              }}
            />
          </div>
          {steps.map((step) => {
            const Icon = step.icon;

            return (
              <div key={step.number} className="group relative">
                {/* Step number + icon */}
                <div className="relative z-10 mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-white/10 bg-black transition duration-300 group-hover:border-white/30 group-hover:bg-white/[0.05]">
                  <Icon className="h-6 w-6 text-neutral-400 transition duration-300 group-hover:text-white" />
                </div>

                {/* Content */}
                <div className="mt-6 text-center">
                  <span className="text-xs font-medium tracking-[0.2em] text-neutral-600">
                    {step.number}
                  </span>

                  <h3 className="mt-3 text-lg font-semibold">{step.title}</h3>

                  <p className="mx-auto mt-3 max-w-xs text-sm leading-6 text-neutral-400">
                    {step.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
