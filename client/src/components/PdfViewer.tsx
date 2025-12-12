"use client"
import { testCitations } from "@/mis/text";
import "../lib/promisePolyfill"
import { usePdfSearch } from '@/utils/pdf_search';
import { Minus, Plus, Search } from 'lucide-react';
import { useEffect , useState } from 'react';
import { Document, pdfjs } from 'react-pdf'; 
import ChatInterface from "./ChatInterface";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import usePdfLoader from "./hooks/PdfLoader";

pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.mjs';

const TestViewer = () => {
  const pdfUrl = "https://cwlklruqhmtcgrtsrmkh.supabase.co/storage/v1/object/public/pdfs/1cfeba82-12ac-4bdd-b77c-c26973fd5551/c8a7ce1e-da24-445f-8bb2-0a647e883709/sample.pdf";
  const [currSearchText, setCurrSearchText] = useState<string>("");
  const {pages,isClientReady,workerReady,handleScale,onDocumentLoadSuccess,numPages,scale}=usePdfLoader()
  const {
    searchText,
    setSearchText,
    searchResults,
    currentMatch,
    performSearch,
    goToNextMatch,
    handleClearSearch
  } = usePdfSearch();


    useEffect(() => {
       if (searchText.trim() !== "") {
          performSearch();
       }
    }, [searchText]);




  const handleCitationClick=(citation:string)=>{
   handleClearSearch()
   setSearchText(citation) 
  }

  if(!isClientReady || !workerReady){
    return <div>Initializing the pdf</div>
  }
  return (
    <div className=' flex h-screen'>
<PanelGroup direction="horizontal">
				<Panel minSize={20}>

      <div className='sticky top-0 z-10 h-12 bg-gray-900 flex justify-center items-center w-full gap-4 px-4'>
        <div className='flex items-center gap-2 flex-1 max-w-md'>
          <input
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                if (searchText === currSearchText) {
                  if (currentMatch < searchResults.length - 1) {
                    goToNextMatch();
                  }
                } else {
                  setCurrSearchText(searchText);
                  performSearch();
                }
              } else if (e.key === 'Escape') {
                handleClearSearch();
              }
            }}
            placeholder="Search in PDF (press Enter)..."
            className='flex-1 border px-2 py-1 outline-none rounded text-white text-sm focus:outline-none focus:ring-2 border-gray-800 focus:ring-blue-500'
          />
          <button
            onClick={() => performSearch()}
            className='px-3 py-1.5 hover:bg-gray-800 text-white rounded text-sm transition-colors'
          >
           <Search size={18}/> 
          </button>
		  </div>
        
        <div className='flex items-center gap-2 border border-gray-600 rounded px-3 py-1'>
          <button 
            onClick={() => handleScale(-0.2)}
            className='hover:bg-gray-700 transition-colors duration-75 rounded p-1'>
            <Minus size={16} className="text-white"/>
          </button>
          <span className='text-xs text-white min-w-[3rem] text-center'>
            {Math.round(scale * 100)}%
          </span>
          <button 
            onClick={() => handleScale(0.2)}
            className='hover:bg-gray-700 transition-colors duration-75 rounded p-1'>
            <Plus size={16} className="text-white"/>
          </button>
        </div>

        {numPages && (
          <span className="text-white text-sm">
            {numPages} pages
          </span>
        )}
      </div>
      <Document 
        file={pdfUrl} 
        onLoadSuccess={onDocumentLoadSuccess}
        onError={(e) => console.log('PDF Error:', e)}
        loading={
          <div className='flex items-center justify-center h-96 bg-gray-50'>
            <div className='text-gray-600'>Loading PDF document...</div>
          </div>
        }
        className={"flex-1 h-screen overflow-auto"}
      >

        
        {pages}
      </Document> 
				</Panel>

        <PanelResizeHandle className="w-2 bg-gray-400 cursor-col-resize" />
	<Panel minSize={40}>
          <div className="">
		<ChatInterface/>
         </div>
	</Panel>
</PanelGroup>
    </div>
  ) 
}

export default TestViewer
