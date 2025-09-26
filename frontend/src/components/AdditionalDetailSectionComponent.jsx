import React from 'react';

const AdditionalDetailsSection = ({ metadata = {}, isLoading = false }) => {
  return (
    <div className="bg-[#f8f9fe] border border-[#e6e6e6] rounded-md p-4 w-full h-[100px]">
      {isLoading ? (
        <div className="flex items-center justify-center h-full">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#7b68ee]"></div>
        </div>
      ) : Object.keys(metadata).length > 0 ? (
        <div className="space-y-2">
          {Object.entries(metadata).map(([key, value], index) => (
            <div key={index} className="flex">
              <span className="text-sm font-medium text-[#4a4a4a] w-1/3">{key}:</span>
              <span className="text-sm text-[#4a4a4a]">{value}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center h-full text-center">
          <p className="text-[#8a8a8a] font-medium italic">Additional Details Section</p>
          <p className="text-xs text-[#8a8a8a] italic">(Placeholder for future content)</p>
        </div>
      )}
    </div>
  );
};

export default AdditionalDetailsSection;