"use client";
import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Dispatcher } from "@/types/dispatcher";
import DispatcherDetails from "@/components/dispatcherDetails";

export default function DispatcherDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [dispatcher, setDispatcher] = useState<Dispatcher | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const dispatcherId = params.id as string;

    // Load dispatchers from localStorage
    const storedDispatchers = localStorage.getItem("dispatchers");
    if (storedDispatchers) {
      const dispatchers: Dispatcher[] = JSON.parse(storedDispatchers);
      const foundDispatcher = dispatchers.find((d) => d.id === dispatcherId);

      if (foundDispatcher) {
        setDispatcher(foundDispatcher);
      } else {
        // Dispatcher not found, redirect back to records
        router.push("/records");
      }
    } else {
      router.push("/records");
    }
    setLoading(false);
  }, [params.id, router]);

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <p>Loading...</p>
      </div>
    );
  }

  if (!dispatcher) {
    return (
      <div className="container mx-auto p-6">
        <p>Dispatcher not found.</p>
        <Link href="/records" className="text-blue-500 hover:underline">
          Back to Records
        </Link>
      </div>
    );
  }

  return <DispatcherDetails dispatcher={dispatcher} />;
}
