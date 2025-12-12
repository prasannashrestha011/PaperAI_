"use client"
import { testCitations,testResult } from '@/mis/text';
import { parseCitations } from '@/utils/text_parser';
export default function PaperWithCitations() {
  

  const handleCitationClick = (numbers:number[]) => {
    const citationTexts = numbers
      .map(num => {
        const idx = num - 1;
        return testCitations[idx] 
          ? `[${num}] ${testCitations[idx]}` 
          : `[${num}] Citation not found`;
      })
      .join('\n\n');
      console.log("Citation texts: ",citationTexts)
    
  };

  const parts = parseCitations(testResult);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">
        Research Paper with Interactive Citations
      </h1>
      
      <div className="prose prose-lg">
        <p className="text-gray-700 leading-relaxed">
          {parts.map((part) => {
            if (part.type === 'text') {
              return <span key={part.key}>{part.content}</span>;
            } else {
              return (
                <sup
                  key={part.key}
                  className="font-bold text-blue-600 cursor-pointer hover:text-blue-800 hover:underline"
                  onClick={() => handleCitationClick(part.numbers)}
                >
                  [{part.rawMatch}]
                </sup>
              );
            }
          })}
        </p>
      </div>

      
    </div>
  );
}
