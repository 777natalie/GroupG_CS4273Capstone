"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Dispatcher } from "@/types/dispatcher";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";

const DispatcherList = () => {
  const [dispatchers, setDispatchers] = useState<Dispatcher[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Function to load dispatchers from localStorage
  const loadDispatchers = () => {
    const storedDispatchers = localStorage.getItem("dispatchers");
    if (storedDispatchers) {
      setDispatchers(JSON.parse(storedDispatchers));
    }
  };

  useEffect(() => {
    // Load dispatchers from localStorage on mount
    loadDispatchers();

    // Listen for custom event when dispatchers are updated
    const handleDispatchersUpdate = () => {
      loadDispatchers();
    };

    window.addEventListener("dispatchersUpdated", handleDispatchersUpdate);

    // Cleanup listener on unmount
    return () => {
      window.removeEventListener("dispatchersUpdated", handleDispatchersUpdate);
    };
  }, []);

  // Filter dispatchers based on search query
  const filteredDispatchers = dispatchers.filter((dispatcher) =>
    dispatcher.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="container mx-auto p-4 sm:p-6 max-w-7xl">
      <h1 className="text-xl sm:text-2xl lg:text-3xl font-bold text-center mb-6 sm:mb-10">
        Please Select a Dispatcher to View Grades and Transcripts
      </h1>

      {/* Search Bar */}
      {dispatchers.length > 0 && (
        <div className="mb-8 max-w-md mx-auto">
          <input
            type="text"
            placeholder="Search dispatchers..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      )}

      {filteredDispatchers.length === 0 && dispatchers.length > 0 ? (
        <p className="text-gray-500 text-center">
          No dispatchers found matching &quot;{searchQuery}&quot;.
        </p>
      ) : filteredDispatchers.length === 0 && dispatchers.length === 0 ? (
        <p className="text-gray-500 text-center">
          No dispatchers found. Please upload files to get started.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 2xl:grid-cols-4 gap-4 md:gap-6">
          {filteredDispatchers.map((dispatcher) => (
            <Link key={dispatcher.id} href={`/records/${dispatcher.id}`}>
              <Card className="cursor-pointer hover:shadow-lg transition-shadow h-full flex flex-col">
                <CardHeader className="flex-shrink-0">
                  <CardTitle className="text-base sm:text-lg break-words">
                    {dispatcher.name}
                  </CardTitle>
                  <CardDescription className="text-xs sm:text-sm truncate">
                    ID: {dispatcher.id.substring(0, 8)}...
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex-grow flex flex-col justify-between">
                  <div className="space-y-2">
                    <div>
                      <p className="text-xs sm:text-sm font-semibold">
                        Transcript Files:
                      </p>
                      <p className="text-xs sm:text-sm text-gray-600">
                        {dispatcher.files.transcriptFiles.length} file(s)
                      </p>
                    </div>
                    <div>
                      <p className="text-xs sm:text-sm font-semibold">
                        Audio Files:
                      </p>
                      <p className="text-xs sm:text-sm text-gray-600">
                        {dispatcher.files.audioFiles.length} file(s)
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default DispatcherList;
