import { useState ,useEffect, useMemo} from "react"
import {Page} from 'react-pdf'; 

console.warn=()=>{}
export default function usePdfLoader() {
  const pdfUrl = "https://cwlklruqhmtcgrtsrmkh.supabase.co/storage/v1/object/public/pdfs/1cfeba82-12ac-4bdd-b77c-c26973fd5551/c8a7ce1e-da24-445f-8bb2-0a647e883709/sample.pdf";
  const [numPages, setNumPages] = useState<number>()
  const [scale,setScale]=useState<number>(1)
  const [isClientReady,setIsClientReady]=useState<boolean>(false)
  const [workerReady, setWorkerReady] = useState<boolean>(false)
  const initializePdf = async () => {
      try {
        // Load style
        await import('react-pdf/dist/Page/AnnotationLayer.css');
        await import('react-pdf/dist/Page/TextLayer.css');
        
        // Setup worker
        const pdfjs = await import('react-pdf').then(mod => mod.pdfjs);
        pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.mjs';
        
        // Mark worker as ready
        setWorkerReady(true)
      } catch (err) {
        console.log('PDF initialization error:', err)
      }
    }

  useEffect(() => {
    setIsClientReady(true)
    setWorkerReady(false)
    initializePdf()
  },[])

  const handleScale = (delta: number) => {
    setScale((prev) => {
      const next = prev + delta
      if (next < 0.7) return 0.7
      if (next > 2.0) return 2.0
      return next
    })
  }
  // @ts-expect-error: ignoring type for react-pdf load success
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages)
  }

  const pages = useMemo(() => {
    if (!numPages || numPages === 0 || !isClientReady || !workerReady) return null;
    
    return Array.from(new Array(numPages), (_, index) => (
      <Page 
        key={`page_${index + 1}`}
        scale={scale}
        pageNumber={index + 1} 
        renderTextLayer={true}
        renderAnnotationLayer={true}
      />
    ));
  }, [numPages, scale, isClientReady, workerReady]);

  return {
    pages,
    handleScale,
    onDocumentLoadSuccess,
    isClientReady,
    workerReady,
    numPages,
    scale
  }
}

