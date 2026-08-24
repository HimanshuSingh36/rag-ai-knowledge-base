import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="absolute left-0 top-0 z-50 w-full">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">

        {/* Logo */}
        <Link
          href="/"
          className="flex items-center gap-2 text-lg font-semibold"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-black">
            ✦
          </div>

          <span>RAG AI</span>
        </Link>

        {/* Navigation */}
        <div className="hidden items-center gap-8 text-sm text-neutral-400 md:flex">
          <Link
            href="#features"
            className="transition hover:text-white"
          >
            Features
          </Link>

          <Link
            href="#how-it-works"
            className="transition hover:text-white"
          >
            How it works
          </Link>
        </div>

        {/* Right */}
        <div className="flex items-center gap-3">
          <button className="hidden text-sm text-neutral-400 transition hover:text-white sm:block">
            Sign in
          </button>

          <button className="rounded-lg border border-neutral-700 bg-white px-4 py-2 text-sm font-medium text-black transition hover:bg-neutral-200">
            Get Started
          </button>
        </div>

      </div>
    </nav>
  );
}