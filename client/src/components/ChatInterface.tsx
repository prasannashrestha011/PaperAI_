
"use client";
import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import { ArrowUp, LineSquiggle } from "lucide-react";


// ---------------- MAIN PAGE ----------------
export default function ChatInterface() {
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string }[]
  >([]);
  const [current, setCurrent] = useState("");
  const [input, setInput] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  const handleSend=()=>{
    setMessages((prev)=>[...prev,{"role":"user",content:input}])
    setInput("")
  }

  // Auto-scroll effect
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, current]);

  return (
    <div  className="bg-gray-950 h-screen p-2">
      <div
        className="h-[80vh] overflow-y-auto"
      >
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: "1rem" }}>
            <div
              style={{
                background: msg.role === "user" ? "#3b82f6" : "#eaeaea",
                color: msg.role === "user" ? "white" : "black",
                padding: "12px 16px",
                borderRadius: "14px",
                maxWidth: "75%",
                whiteSpace: "pre-wrap",
              }}
            >
              <ReactMarkdown
                remarkPlugins={[remarkMath]}
                rehypePlugins={[rehypeKatex]}
              >
                {msg.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
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
            <LineSquiggle className="active:scale-90 hover:bg-gray-700 p-1 rounded-full" size={30} />

          </span>
        <button
           onClick={handleSend}
          className="bg-[#3b82f6] rounded-full w-8 h-8 flex items-center justify-center cursor-pointer active:bg-blue-400 active:scale-80 transition-all ease-in-out duration-150"
        >
          <ArrowUp size={12} className="text-white"/>
        </button>

        </div>
      </div>
    </div>
  );
}
