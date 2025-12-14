"use client";
// import { testCitations,testResult } from '@/mis/text';
import { parseCitations } from "@/utils/text_parser";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
interface Params {
  aiResponse: string;
  citations: string[];
  performSearch: (citationTexts: string) => void;
}
export default function PaperWithCitations({
  aiResponse,
  citations,
  performSearch,
}: Params) {
  //indexes the extracted numbers to citation list
  const handleCitationClick = (numbers: number[]) => {
    const citationTexts = numbers
      .map((num) => {
        const idx = num - 1;
        return citations[idx] ? `${citations[idx]}` : `Citation not found`;
      })
      .join("\n\n");
    performSearch(citationTexts);
  };

  const parts = parseCitations(aiResponse);

  return (
    <div className="max-w-5xl mx-auto p-6  ">
      <div className="prose prose-lg">
        <div className="text-slate-100 leading-relaxed">
          <>
            {parts.map((part, idx) => {
              if (part.type === "text") {
                return (
                  <ReactMarkdown
                    key={idx}
                    children={part.content}
                    remarkPlugins={[remarkMath]}
                    rehypePlugins={[rehypeKatex]}
                  />
                );
              } else {
                return (
                  <sup
                    key={part.key}
                    className="font-bold text-blue-600 cursor-pointer hover:text-blue-800 hover:underline"
                    onClick={() => handleCitationClick(part.numbers ?? [])}
                  >
                    [{part.rawMatch}]
                  </sup>
                );
              }
            })}
          </>
        </div>
      </div>
    </div>
  );
}
