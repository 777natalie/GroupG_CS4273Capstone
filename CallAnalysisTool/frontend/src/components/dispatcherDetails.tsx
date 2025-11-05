"use client";
import React from "react";
import Link from "next/link";
import { Dispatcher } from "@/types/dispatcher";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";

interface DispatcherDetailsProps {
  dispatcher: Dispatcher;
}

const DispatcherDetails = ({ dispatcher }: DispatcherDetailsProps) => {
  return (
    <div className="container mx-auto p-6">
      <div className="mb-6">
        <Link
          href="/records"
          className="text-blue-500 hover:underline mb-4 inline-block"
        >
          ← Back to Records
        </Link>
        <h1 className="text-3xl font-bold mt-4">{dispatcher.name}</h1>
        <p className="text-gray-500 mt-2">Dispatcher ID: {dispatcher.id}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Transcript Files Section */}
        <Card>
          <CardHeader>
            <CardTitle>Transcript Files</CardTitle>
            <CardDescription>
              {dispatcher.files.transcriptFiles.length} file(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            {dispatcher.files.transcriptFiles.length > 0 ? (
              <ul className="space-y-2">
                {dispatcher.files.transcriptFiles.map((filename, index) => (
                  <li
                    key={index}
                    className="p-3 bg-gray-50 rounded-lg border border-gray-200 flex items-center justify-between"
                  >
                    <p className="text-sm font-medium flex-1">{filename}</p>
                    <span
                      // Green if 90% or above, Yellow if 70-89%, Red if below 70%
                      className={`text-sm font-semibold ${
                        Number(dispatcher.grades?.[filename]) > 90
                          ? `text-green-600`
                          : `${
                              Number(dispatcher.grades?.[filename]) > 70
                                ? `text-yellow-400`
                                : `text-red-600`
                            }`
                      } ml-4`}
                    >
                      {dispatcher.grades?.[filename]
                        ? `Grade: ${dispatcher.grades[filename]}`
                        : "No Grade"}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No transcript files available.</p>
            )}
          </CardContent>
        </Card>

        {/* Audio Files Section */}
        <Card>
          <CardHeader>
            <CardTitle>Audio Files</CardTitle>
            <CardDescription>
              {dispatcher.files.audioFiles.length} file(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            {dispatcher.files.audioFiles.length > 0 ? (
              <ul className="space-y-2">
                {dispatcher.files.audioFiles.map((filename, index) => (
                  <li
                    key={index}
                    className="p-3 bg-gray-50 rounded-lg border border-gray-200"
                  >
                    <p className="text-sm font-medium">{filename}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No audio files available.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DispatcherDetails;
