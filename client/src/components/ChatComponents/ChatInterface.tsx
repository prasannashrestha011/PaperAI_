"use client";

import { testCitations, testResult } from "@/mis/text";
import React, { useState, useEffect, useRef } from "react";
import { ArrowUp, LineSquiggle } from "lucide-react";
import PaperWithCitations from "./ChatWithCitation";
import { usePdfSearch } from "@/utils/pdf_search";
import Image from "next/image";

// ---------------- MAIN PAGE ----------------
export default function ChatInterface() {
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string }[]
  >([]);
  const [current, setCurrent] = useState("");
  const [input, setInput] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);
  const { performSearch } = usePdfSearch();

  const handleSend = () => {
    setMessages((prev) => [...prev, { role: "assistant", content: input }]);
    setInput("");
  };

  // Auto-scroll effect
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, current]);

  return (
    <div className="bg-gray-900 h-screen p-2">
      <div className="h-[80vh] overflow-y-auto  font-sans">
        {messages.map((msg, i) =>
          msg.role == "assistant" ? (
            <div key={i} className="mb-1 flex gap-2 items-start">
              <div className="whitespace-pre-wrap">
                <PaperWithCitations
                  aiResponse={testResult}
                  citations={testCitations}
                  performSearch={performSearch}
                />

                <span>References</span>
                <ul className="text-xs text-gray-400">
                  {testCitations.map((citation, idx) => (
                    <li
                      key={idx}
                      onClick={() => performSearch(citation)}
                      className="mb-2 flex gap-2 hover:cursor-pointer"
                    >
                      <b className="text-blue-900">({idx + 1})</b>
                      <span>{citation}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <div>{msg.content}</div>
          )
        )}
        {/* Invisible anchor for scrolling */}
        <div ref={chatEndRef} />
      </div>
      {/* Input */}
      <div className="flex flex-col  items-center justify-center">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask something about this paper."
          className="w-full bg-gray-800 p-2 outline-none rounded-tl-sm rounded-tr-sm text-sm min-h-10 max-h-18 h-18"
        />
        <div className="w-full flex bg-gray-800 rounded-bl-sm rounded-br-sm">
          <span className="flex-1">
            <LineSquiggle
              className="active:scale-90 hover:bg-gray-700 p-1 rounded-full"
              size={30}
            />
          </span>
          <button
            onClick={handleSend}
            className="bg-[#3b82f6] rounded-full w-8 h-8 flex items-center justify-center cursor-pointer active:bg-blue-400 active:scale-80 transition-all ease-in-out duration-150"
          >
            <ArrowUp size={12} className="text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}
