const steps = [
  {
    number: "01",
    title: "Upload Documents",
    description:
      "Add your PDFs and documents to create your private knowledge base.",
  },
  {
    number: "02",
    title: "Process & Index",
    description:
      "Your documents are processed and converted into searchable knowledge.",
  },
  {
    number: "03",
    title: "Ask Questions",
    description:
      "Ask questions naturally and let the system find the most relevant information.",
  },
  {
    number: "04",
    title: "Get Grounded Answers",
    description:
      "Receive an answer based on your documents with relevant sources.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="scroll-mt-24 relative z-10 border-t border-white/[0.08] px-6 py-28 md:py-32">
      <div className="mx-auto max-w-6xl">
        {/* Heading */}
        <div className="mx-auto mb-16 max-w-2xl text-center">
          <p className="text-sm uppercase tracking-[0.3em] text-neutral-500">
            How it works
          </p>

          <h2 className="mt-4 text-3xl font-bold tracking-tight md:text-4xl lg:text-5xl">
            From documents to{" "}
            <span className="text-neutral-500">answers.</span>
          </h2>

          <p className="mt-5 text-neutral-400">
            A simple workflow that turns your documents into an
            intelligent knowledge base.
          </p>
        </div>

        {/* Steps */}
        <div className="grid gap-6 md:grid-cols-4">
          {steps.map((step) => (
            <div
              key={step.number}
              className="group relative rounded-2xl border border-white/10 bg-white/[0.02] p-6 transition duration-300 hover:border-white/20 hover:bg-white/[0.04]"
            >
              <span className="text-sm font-medium text-neutral-600">
                {step.number}
              </span>

              <h3 className="mt-6 text-lg font-semibold">
                {step.title}
              </h3>

              <p className="mt-3 text-sm leading-6 text-neutral-400">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}