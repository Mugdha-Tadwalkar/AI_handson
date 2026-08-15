"use client";

import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(
        "https://animated-lamp-97545vqr5q9p3jgw-8000.app.github.dev/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const responseText = await response.text();

      console.log("Backend status:", response.status);
      console.log("Backend response:", responseText);

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
        "Sorry, I could not connect to the AI assistant."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center px-6 py-12">

      <div className="w-full max-w-3xl">

        {/* Header */}
        <div className="text-center mb-10">

          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full border border-white/20 bg-white/5 mb-6">
            <span className="text-3xl">✦</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-semibold tracking-tight">
            Mugdha's AI Assistant
          </h1>

          <p className="text-gray-400 mt-4 text-base md:text-lg">
            Ask questions about Mugdha's professional profile
          </p>

        </div>


        {/* Main Chat Card */}
        <div className="bg-white text-black rounded-3xl shadow-2xl p-6 md:p-8">

          {/* Question Label */}
          <div className="flex items-center justify-between mb-3">

            <label className="text-sm font-semibold text-gray-800">
              Ask a question
            </label>

            <span className="text-xs text-gray-400">
              AI Resume Assistant
            </span>

          </div>


          {/* Textarea */}
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g. What projects has Mugdha worked on?"
            className="w-full h-36 resize-none rounded-2xl border border-gray-200 bg-gray-50 p-5 text-gray-900 placeholder-gray-400 outline-none focus:border-black focus:ring-1 focus:ring-black transition"
          />


          {/* Button */}
          <button
            onClick={askQuestion}
            disabled={loading}
            className="mt-4 w-full rounded-2xl bg-black text-white py-4 font-medium hover:bg-gray-800 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? "Thinking..." : "Ask Assistant →"}
          </button>


          {/* Answer */}
          {answer && (

            <div className="mt-7 border-t border-gray-200 pt-6">

              <div className="flex items-center gap-3 mb-4">

                <div className="w-9 h-9 rounded-full bg-black text-white flex items-center justify-center">
                  <span className="text-sm">✦</span>
                </div>

                <div>
                  <p className="font-semibold text-gray-900">
                    AI Assistant
                  </p>

                  <p className="text-xs text-gray-400">
                    Based on the resume
                  </p>
                </div>

              </div>


              <div className="rounded-2xl bg-gray-50 border border-gray-200 p-5">

                <p className="text-gray-700 leading-7 whitespace-pre-line">
                  {answer}
                </p>

              </div>

            </div>

          )}

        </div>


        {/* Example Questions */}
        <div className="mt-8">

          <p className="text-xs uppercase tracking-widest text-gray-500 text-center mb-4">
            Try asking
          </p>

          <div className="flex flex-wrap justify-center gap-3">

            {[
              "What are Mugdha's skills?",
              "Tell me about her projects",
              "What is her experience?",
              "What technologies does she know?",
            ].map((item) => (

              <button
                key={item}
                onClick={() => setQuestion(item)}
                className="rounded-full border border-white/15 bg-white/5 px-4 py-2 text-sm text-gray-300 hover:bg-white hover:text-black transition"
              >
                {item}
              </button>

            ))}

          </div>

        </div>


        {/* Footer */}
        <div className="text-center mt-10">

          <p className="text-xs text-gray-600">
            Powered by FastAPI · Groq · Llama
          </p>

        </div>

      </div>

    </main>
  );
}