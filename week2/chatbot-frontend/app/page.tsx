"use client";

import { useState } from "react";
const API_URL = process.env.NEXT_PUBLIC_API_URL;

const exampleQuestions = [
  "What are Mugdha's skills?",
  "Tell me about her projects",
  "What is her experience?",
  "What technologies does she know?",
];

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      const responseText = await response.text();

      if (!response.ok) {
        throw new Error(
          `Backend request failed: ${response.status} - ${responseText}`
        );
      }

      const data = JSON.parse(responseText);

      setAnswer(data.answer);
    } catch (error) {
      console.error(error);

      setAnswer(
        "I couldn't connect to the assistant right now. Please try again in a moment."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#050505] text-white">

      {/* Background */}
      <div className="ambient" />
      <div className="grid-background absolute inset-0 opacity-60" />

      {/* Content */}
      <div className="relative z-10 mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 sm:px-8">

        {/* Navbar */}
        <nav className="flex items-center justify-between border-b border-white/[0.07] py-6">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06]">
              <span className="text-sm">✦</span>
            </div>

            <span className="text-sm font-medium tracking-wide text-white/80">
              MUGDHA
            </span>

          </div>

          <div className="hidden items-center gap-8 text-sm text-white/40 sm:flex">
            <span className="transition hover:text-white">
              About
            </span>

            <span className="transition hover:text-white">
              Experience
            </span>

            <span className="transition hover:text-white">
              Projects
            </span>

            <span className="text-white/80">
              AI Assistant
            </span>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5">

            <span className="pulse-dot h-1.5 w-1.5 rounded-full bg-emerald-400" />

            <span className="text-xs text-white/50">
              AI Online
            </span>

          </div>

        </nav>


        {/* Hero */}
        <section className="flex flex-1 flex-col items-center justify-center py-16 sm:py-24">

          {/* Badge */}
          <div className="float mb-8 flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-4 py-2">

            <span className="text-sm">✦</span>

            <span className="text-xs font-medium tracking-wide text-white/60">
              AI-POWERED PORTFOLIO
            </span>

          </div>


          {/* Heading */}
          <div className="max-w-4xl text-center">

            <h1 className="text-5xl font-semibold leading-[1.05] tracking-[-0.04em] sm:text-6xl md:text-7xl">

              Meet{" "}

              <span className="bg-gradient-to-r from-white via-white/80 to-white/40 bg-clip-text text-transparent">
                Mugdha.
              </span>

              <br />

              <span className="text-white/35">
                Ask her AI anything.
              </span>

            </h1>

            <p className="mx-auto mt-7 max-w-2xl text-base leading-7 text-white/40 sm:text-lg">
              Explore Mugdha&apos;s professional journey, skills,
              projects and experience through an intelligent
              conversational assistant.
            </p>

          </div>


          {/* AI Card */}
          <div className="mt-12 w-full max-w-3xl">

            <div className="glass glow rounded-[28px] p-2">

              {/* Card Header */}
              <div className="flex items-center justify-between px-5 py-4">

                <div className="flex items-center gap-3">

                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-black shadow-lg">
                    ✦
                  </div>

                  <div>
                    <p className="text-sm font-medium">
                      Mugdha AI
                    </p>

                    <p className="text-[11px] text-white/35">
                      Professional profile assistant
                    </p>
                  </div>

                </div>

                <div className="hidden rounded-full border border-white/10 px-3 py-1 text-[10px] uppercase tracking-wider text-white/30 sm:block">
                  Llama · Groq
                </div>

              </div>


              {/* Input */}
              <div className="rounded-[22px] border border-white/[0.08] bg-black/40 p-4">

                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask anything about Mugdha..."
                  className="min-h-[130px] w-full resize-none bg-transparent p-2 text-base leading-7 text-white outline-none placeholder:text-white/20"
                />

                <div className="flex items-center justify-between pt-3">

                  <span className="hidden text-xs text-white/20 sm:block">
                    Press Enter to ask · Shift + Enter for new line
                  </span>

                  <span className="text-xs text-white/20 sm:hidden">
                    AI Assistant
                  </span>

                  <button
                    onClick={askQuestion}
                    disabled={loading || !question.trim()}
                    className="group flex items-center gap-2 rounded-xl bg-white px-5 py-2.5 text-sm font-medium text-black transition-all duration-300 hover:bg-white/90 hover:shadow-[0_0_30px_rgba(255,255,255,0.15)] disabled:cursor-not-allowed disabled:opacity-30"
                  >

                    {loading ? (
                      <>
                        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-black/20 border-t-black" />
                        Thinking
                      </>
                    ) : (
                      <>
                        Ask AI
                        <span className="transition-transform group-hover:translate-x-1">
                          →
                        </span>
                      </>
                    )}

                  </button>

                </div>

              </div>


              {/* Answer */}
              {answer && (

                <div className="mx-2 mb-2 mt-2 overflow-hidden rounded-[22px] border border-white/[0.07] bg-white/[0.025]">

                  <div className="flex items-center gap-3 border-b border-white/[0.06] px-5 py-4">

                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-xs text-black">
                      ✦
                    </div>

                    <div>
                      <p className="text-xs font-medium">
                        Mugdha AI
                      </p>

                      <p className="text-[10px] text-white/30">
                        Generated from profile knowledge
                      </p>
                    </div>

                  </div>

                  <div className="px-5 py-5">

                    <p className="whitespace-pre-line text-sm leading-7 text-white/65">
                      {answer}
                    </p>

                  </div>

                </div>

              )}

            </div>

          </div>


          {/* Suggested questions */}
          <div className="mt-8 w-full max-w-3xl">

            <p className="mb-4 text-center text-[10px] font-medium uppercase tracking-[0.2em] text-white/20">
              Explore her profile
            </p>

            <div className="flex flex-wrap justify-center gap-2">

              {exampleQuestions.map((item) => (

                <button
                  key={item}
                  onClick={() => setQuestion(item)}
                  className="rounded-full border border-white/[0.08] bg-white/[0.025] px-4 py-2 text-xs text-white/40 transition-all duration-300 hover:border-white/20 hover:bg-white/[0.07] hover:text-white/80"
                >
                  {item}
                </button>

              ))}

            </div>

          </div>

        </section>


        {/* Footer */}
        <footer className="flex flex-col items-center justify-between gap-3 border-t border-white/[0.07] py-6 sm:flex-row">

          <p className="text-[11px] text-white/20">
            © 2026 Mugdha. All rights reserved.
          </p>

          <p className="text-[11px] text-white/20">
            Built with Next.js · FastAPI · Groq
          </p>

        </footer>

      </div>

    </main>
  );
}