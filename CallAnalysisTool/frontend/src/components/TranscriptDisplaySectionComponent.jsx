import React, { useRef, useEffect, useState } from 'react';

const TranscriptSection = ({ transcriptData = [], isLoading = false }) => {
  const transcriptRef = useRef(null);
  const [isScrollable, setIsScrollable] = useState(false);


  useEffect(() => {
    // Check if transcript content exceeds container height
    const checkScrollable = () => {
      if (transcriptRef.current) {
        const { scrollHeight, clientHeight } = transcriptRef.current;
        setIsScrollable(scrollHeight > clientHeight);
      }
    };

    checkScrollable();
    // Re-check when window is resized or transcript data changes
    window.addEventListener('resize', checkScrollable);
    return () => window.removeEventListener('resize', checkScrollable);
  }, [transcriptData]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (transcriptRef.current && transcriptData.length > 0) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [transcriptData]);

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold text-[#4a4a4a] mb-4">Transcript</h2>
      
      <div className="relative">
        <div 
          ref={transcriptRef}
          className="bg-[#f9f9fd] rounded-md p-3 h-[200px] overflow-y-auto"
        >
          {isLoading ? (
            <div className="flex justify-center items-center h-full">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#7b68ee]"></div>
            </div>
          ) : transcriptData.length > 0 ? (
            <div className="space-y-3">
              {transcriptData.map((message, index) => (
                <div key={index} className="text-sm">
                  <span className="font-medium text-[#4a4a4a]">{message.sender}: </span>
                  <span className="text-[#4a4a4a]">{message.text}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex justify-center items-center h-full text-[#8a8a8a] italic">
              No transcript data available
            </div>
          )}
        </div>
        
        {isScrollable && (
          <div className="absolute right-1 top-1 bottom-1 w-1.5">
            <div className="bg-[#f2f2f7] h-full rounded-full w-1.5">
              <div className="bg-[#d0d0e0] rounded-full w-1.5 h-1/3"></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TranscriptSection;