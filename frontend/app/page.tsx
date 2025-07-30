"use client";

import { useState } from "react";

const API_URL = "https://ai-study-buddy-pnyu.onrender.com";

interface ProcessingStep {
  id: string;
  name: string;
  status: "pending" | "processing" | "completed" | "error";
  description: string;
}

interface Event {
  frame: number;
  timestamp: string;
  action: string;
  confidence: number;
}

export default function SurgiTrack() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [fileKey, setFileKey] = useState<string>("");
  const [jobId, setJobId] = useState<string>("");
  const [currentStep, setCurrentStep] = useState(0);
  const [events, setEvents] = useState<Event[]>([]);
  const [error, setError] = useState<string>("");

  const steps: ProcessingStep[] = [
    {
      id: "upload",
      name: "Upload Video",
      status: "pending",
      description: "Upload your surgical video file",
    },
    {
      id: "validate",
      name: "Validate",
      status: "pending",
      description: "Check file format and specifications",
    },
    {
      id: "extract",
      name: "Extract Frames",
      status: "pending",
      description: "Extract individual frames from video",
    },
    {
      id: "detect",
      name: "Detect Objects",
      status: "pending",
      description: "Identify surgical tools in frames",
    },
    {
      id: "track",
      name: "Track Events",
      status: "pending",
      description: "Track tool movements and events",
    },
    {
      id: "complete",
      name: "Complete",
      status: "pending",
      description: "Generate timeline results",
    },
  ];

  const [processingSteps, setProcessingSteps] =
    useState<ProcessingStep[]>(steps);

  const updateStepStatus = (
    stepId: string,
    status: ProcessingStep["status"]
  ) => {
    setProcessingSteps((prev) =>
      prev.map((step) => (step.id === stepId ? { ...step, status } : step))
    );
  };

  const handleFileUpload = async () => {
    if (!file) return;

    setError("");
    setCurrentStep(1);
    updateStepStatus("upload", "processing");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const result = await response.json();
      setFileKey(result.file_key);
      updateStepStatus("upload", "completed");
      updateStepStatus("validate", "completed");
      setCurrentStep(2);

      // Start processing
      await startProcessing(result.file_key);
    } catch (error) {
      console.error("Upload failed:", error);
      setError(
        `Upload failed: ${
          error instanceof Error ? error.message : "Unknown error"
        }`
      );
      updateStepStatus("upload", "error");
    } finally {
      setLoading(false);
    }
  };

  const startProcessing = async (fileKey: string) => {
    try {
      updateStepStatus("extract", "processing");

      const response = await fetch(
        `${API_URL}/process?file_key=${encodeURIComponent(fileKey)}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(`Processing failed: ${response.status}`);
      }

      const result = await response.json();
      setJobId(result.job_id);

      // Simulate processing steps (since we don't have real-time job status yet)
      setTimeout(() => {
        updateStepStatus("extract", "completed");
        updateStepStatus("detect", "processing");
      }, 2000);

      setTimeout(() => {
        updateStepStatus("detect", "completed");
        updateStepStatus("track", "processing");
      }, 5000);

      setTimeout(() => {
        updateStepStatus("track", "completed");
        updateStepStatus("complete", "completed");
        setCurrentStep(5);
        // Generate mock events for demo
        generateMockEvents();
      }, 8000);
    } catch (error) {
      console.error("Processing failed:", error);
      setError(
        `Processing failed: ${
          error instanceof Error ? error.message : "Unknown error"
        }`
      );
      updateStepStatus("extract", "error");
    }
  };

  const generateMockEvents = () => {
    // Mock events based on typical surgical tool tracking
    const mockEvents: Event[] = [
      {
        frame: 45,
        timestamp: "00:03",
        action: "Scalpel picked up",
        confidence: 0.94,
      },
      {
        frame: 180,
        timestamp: "00:12",
        action: "Forceps picked up",
        confidence: 0.87,
      },
      {
        frame: 320,
        timestamp: "00:21",
        action: "Scalpel placed back",
        confidence: 0.92,
      },
      {
        frame: 480,
        timestamp: "00:32",
        action: "Scissors picked up",
        confidence: 0.89,
      },
      {
        frame: 620,
        timestamp: "00:41",
        action: "Forceps placed back",
        confidence: 0.91,
      },
      {
        frame: 750,
        timestamp: "00:50",
        action: "Scissors placed back",
        confidence: 0.88,
      },
    ];
    setEvents(mockEvents);
  };

  const getStepIcon = (status: ProcessingStep["status"]) => {
    switch (status) {
      case "completed":
        return "✅";
      case "processing":
        return "🔄";
      case "error":
        return "❌";
      default:
        return "⭕";
    }
  };

  const formatFileSize = (bytes: number) => {
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  const resetProcess = () => {
    setFile(null);
    setFileKey("");
    setJobId("");
    setCurrentStep(0);
    setEvents([]);
    setError("");
    setProcessingSteps(steps);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl mb-6 shadow-lg">
            <span className="text-3xl">🏥</span>
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-blue-900 via-indigo-800 to-blue-900 bg-clip-text text-transparent">
            SurgiTrack
          </h1>
          <p className="text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            AI-Powered Surgical Tool Tracking System for Enhanced Operating Room
            Analytics
          </p>
        </div>

        {/* Upload Section */}
        {currentStep === 0 && (
          <div className="max-w-2xl mx-auto mb-12">
            <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 sm:px-8 py-6">
                <h2 className="text-xl sm:text-2xl font-bold text-white text-center">
                  🎬 Upload Surgical Video
                </h2>
                <p className="text-blue-100 text-center mt-2">
                  Select your surgical procedure video for AI analysis
                </p>
              </div>

              <div className="p-6 sm:p-8 space-y-6">
                <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 bg-slate-50 hover:bg-slate-100 transition-colors">
                  <input
                    type="file"
                    accept=".mp4"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="block w-full text-sm text-slate-600 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-blue-600 file:to-indigo-600 file:text-white hover:file:from-blue-700 hover:file:to-indigo-700 file:shadow-lg file:transition-all"
                  />
                </div>

                {file && (
                  <div className="bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 rounded-xl p-4">
                    <h3 className="font-semibold text-emerald-800 mb-3 flex items-center">
                      <span className="mr-2">✅</span>
                      File Selected
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                      <div className="text-slate-700">
                        <span className="font-medium text-slate-900">
                          Name:
                        </span>
                        <p className="truncate">{file.name}</p>
                      </div>
                      <div className="text-slate-700">
                        <span className="font-medium text-slate-900">
                          Size:
                        </span>
                        <p>{formatFileSize(file.size)}</p>
                      </div>
                      <div className="text-slate-700">
                        <span className="font-medium text-slate-900">
                          Type:
                        </span>
                        <p>{file.type}</p>
                      </div>
                    </div>
                  </div>
                )}

                <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
                  <h3 className="font-semibold text-amber-800 mb-2 flex items-center">
                    <span className="mr-2">⚠️</span>
                    Requirements
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-sm text-amber-700">
                    <div className="flex items-center">
                      <span className="w-2 h-2 bg-amber-400 rounded-full mr-2"></span>
                      MP4 format only
                    </div>
                    <div className="flex items-center">
                      <span className="w-2 h-2 bg-amber-400 rounded-full mr-2"></span>
                      Max 10MB size
                    </div>
                    <div className="flex items-center">
                      <span className="w-2 h-2 bg-amber-400 rounded-full mr-2"></span>
                      Max 60 FPS
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleFileUpload}
                  disabled={!file || loading}
                  className="w-full px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-700 hover:to-indigo-700 focus:ring-4 focus:ring-blue-200 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-3"></div>
                      Uploading & Processing...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center">
                      <span className="mr-2">🚀</span>
                      Upload & Start Processing
                    </div>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Processing Steps */}
        {currentStep > 0 && (
          <div className="max-w-4xl mx-auto mb-12">
            <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 sm:px-8 py-6">
                <h2 className="text-xl sm:text-2xl font-bold text-white text-center flex items-center justify-center">
                  <span className="mr-3">⚙️</span>
                  Processing Status
                </h2>
                <p className="text-indigo-100 text-center mt-2">
                  AI analysis in progress - please wait
                </p>
              </div>

              <div className="p-6 sm:p-8">
                <div className="grid gap-4 sm:gap-6">
                  {processingSteps.map((step, index) => {
                    const isActive = step.status === "processing";
                    const isCompleted = step.status === "completed";
                    const isError = step.status === "error";

                    return (
                      <div
                        key={step.id}
                        className={`relative flex items-center p-4 sm:p-6 rounded-xl border-2 transition-all duration-300 ${
                          isActive
                            ? "border-blue-300 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-lg"
                            : isCompleted
                            ? "border-emerald-300 bg-gradient-to-r from-emerald-50 to-teal-50"
                            : isError
                            ? "border-red-300 bg-gradient-to-r from-red-50 to-pink-50"
                            : "border-slate-200 bg-slate-50"
                        }`}
                      >
                        <div className="flex items-center space-x-4 sm:space-x-6 w-full">
                          <div
                            className={`flex items-center justify-center w-12 h-12 rounded-full text-2xl ${
                              isActive
                                ? "bg-blue-100 border-2 border-blue-300"
                                : isCompleted
                                ? "bg-emerald-100 border-2 border-emerald-300"
                                : isError
                                ? "bg-red-100 border-2 border-red-300"
                                : "bg-slate-100 border-2 border-slate-300"
                            }`}
                          >
                            {getStepIcon(step.status)}
                          </div>

                          <div className="flex-1 min-w-0">
                            <h3
                              className={`font-semibold text-lg ${
                                isActive
                                  ? "text-blue-900"
                                  : isCompleted
                                  ? "text-emerald-900"
                                  : isError
                                  ? "text-red-900"
                                  : "text-slate-700"
                              }`}
                            >
                              {step.name}
                            </h3>
                            <p
                              className={`text-sm mt-1 ${
                                isActive
                                  ? "text-blue-700"
                                  : isCompleted
                                  ? "text-emerald-700"
                                  : isError
                                  ? "text-red-700"
                                  : "text-slate-600"
                              }`}
                            >
                              {step.description}
                            </p>
                          </div>

                          <div className="flex items-center">
                            {step.status === "processing" && (
                              <div className="flex flex-col items-center space-y-2">
                                <div className="animate-spin h-6 w-6 border-3 border-blue-500 border-t-transparent rounded-full"></div>
                                <span className="text-xs text-blue-600 font-medium">
                                  Processing
                                </span>
                              </div>
                            )}
                            {step.status === "completed" && (
                              <div className="flex flex-col items-center space-y-1">
                                <div className="h-6 w-6 bg-emerald-500 rounded-full flex items-center justify-center">
                                  <span className="text-white text-sm">✓</span>
                                </div>
                                <span className="text-xs text-emerald-600 font-medium">
                                  Done
                                </span>
                              </div>
                            )}
                            {step.status === "error" && (
                              <div className="flex flex-col items-center space-y-1">
                                <div className="h-6 w-6 bg-red-500 rounded-full flex items-center justify-center">
                                  <span className="text-white text-sm">✕</span>
                                </div>
                                <span className="text-xs text-red-600 font-medium">
                                  Error
                                </span>
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Progress line between steps */}
                        {index < processingSteps.length - 1 && (
                          <div
                            className={`absolute left-9 top-full w-0.5 h-4 ${
                              processingSteps[index + 1].status === "completed"
                                ? "bg-emerald-300"
                                : "bg-slate-300"
                            }`}
                          ></div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Timeline Results */}
        {events.length > 0 && (
          <div className="max-w-5xl mx-auto mb-12">
            <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
              <div className="bg-gradient-to-r from-emerald-600 to-teal-600 px-6 sm:px-8 py-6">
                <h2 className="text-xl sm:text-2xl font-bold text-white text-center flex items-center justify-center">
                  <span className="mr-3">🎯</span>
                  Surgical Tool Timeline
                </h2>
                <p className="text-emerald-100 text-center mt-2">
                  AI-detected surgical tool events with timestamps
                </p>
              </div>

              <div className="p-6 sm:p-8">
                <div className="space-y-4">
                  {events.map((event, index) => {
                    const isPickup = event.action
                      .toLowerCase()
                      .includes("picked up");
                    const isPlacement = event.action
                      .toLowerCase()
                      .includes("placed back");

                    return (
                      <div
                        key={index}
                        className={`relative flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 sm:p-6 rounded-xl border-2 transition-all duration-200 hover:shadow-lg ${
                          isPickup
                            ? "border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50"
                            : isPlacement
                            ? "border-emerald-200 bg-gradient-to-r from-emerald-50 to-teal-50"
                            : "border-purple-200 bg-gradient-to-r from-purple-50 to-pink-50"
                        }`}
                      >
                        <div className="flex items-center space-x-4 w-full sm:w-auto">
                          <div
                            className={`flex items-center justify-center w-16 h-16 rounded-full text-2xl border-2 ${
                              isPickup
                                ? "bg-blue-100 border-blue-300"
                                : isPlacement
                                ? "bg-emerald-100 border-emerald-300"
                                : "bg-purple-100 border-purple-300"
                            }`}
                          >
                            {isPickup ? "🔼" : isPlacement ? "🔽" : "🔄"}
                          </div>

                          <div className="flex-1 min-w-0">
                            <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-4 space-y-2 sm:space-y-0">
                              <span
                                className={`inline-flex items-center px-4 py-2 rounded-full text-lg font-mono font-bold ${
                                  isPickup
                                    ? "bg-blue-600 text-white"
                                    : isPlacement
                                    ? "bg-emerald-600 text-white"
                                    : "bg-purple-600 text-white"
                                }`}
                              >
                                ⏱️ {event.timestamp}
                              </span>

                              <div className="flex-1">
                                <h3
                                  className={`text-lg font-semibold ${
                                    isPickup
                                      ? "text-blue-900"
                                      : isPlacement
                                      ? "text-emerald-900"
                                      : "text-purple-900"
                                  }`}
                                >
                                  {event.action}
                                </h3>
                                <p
                                  className={`text-sm ${
                                    isPickup
                                      ? "text-blue-700"
                                      : isPlacement
                                      ? "text-emerald-700"
                                      : "text-purple-700"
                                  }`}
                                >
                                  Detected at frame {event.frame}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center mt-4 sm:mt-0 w-full sm:w-auto justify-between sm:justify-end">
                          <div
                            className={`px-4 py-2 rounded-lg ${
                              event.confidence >= 0.9
                                ? "bg-emerald-100 text-emerald-800"
                                : event.confidence >= 0.8
                                ? "bg-yellow-100 text-yellow-800"
                                : "bg-orange-100 text-orange-800"
                            }`}
                          >
                            <div className="text-xs font-medium">
                              Confidence
                            </div>
                            <div className="text-lg font-bold">
                              {Math.round(event.confidence * 100)}%
                            </div>
                          </div>
                        </div>

                        {/* Timeline connector */}
                        {index < events.length - 1 && (
                          <div className="absolute left-10 top-full w-0.5 h-4 bg-gradient-to-b from-slate-300 to-slate-200"></div>
                        )}
                      </div>
                    );
                  })}
                </div>

                <div className="mt-8 pt-6 border-t border-slate-200">
                  <div className="text-center space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
                      <div className="bg-slate-50 rounded-lg p-3">
                        <div className="font-semibold text-slate-900">
                          Total Events
                        </div>
                        <div className="text-2xl font-bold text-blue-600">
                          {events.length}
                        </div>
                      </div>
                      <div className="bg-slate-50 rounded-lg p-3">
                        <div className="font-semibold text-slate-900">
                          Duration
                        </div>
                        <div className="text-2xl font-bold text-emerald-600">
                          {events[events.length - 1]?.timestamp || "N/A"}
                        </div>
                      </div>
                      <div className="bg-slate-50 rounded-lg p-3">
                        <div className="font-semibold text-slate-900">
                          Avg Confidence
                        </div>
                        <div className="text-2xl font-bold text-purple-600">
                          {Math.round(
                            (events.reduce((sum, e) => sum + e.confidence, 0) /
                              events.length) *
                              100
                          )}
                          %
                        </div>
                      </div>
                    </div>

                    <button
                      onClick={resetProcess}
                      className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 focus:ring-4 focus:ring-blue-200 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                    >
                      <span className="mr-2">🔄</span>
                      Process Another Video
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="max-w-2xl mx-auto mb-12">
            <div className="bg-white rounded-2xl shadow-xl border-2 border-red-200 overflow-hidden">
              <div className="bg-gradient-to-r from-red-600 to-pink-600 px-6 sm:px-8 py-6">
                <h3 className="text-xl font-bold text-white text-center flex items-center justify-center">
                  <span className="mr-3">❌</span>
                  Processing Error
                </h3>
                <p className="text-red-100 text-center mt-2">
                  Something went wrong during video processing
                </p>
              </div>

              <div className="p-6 sm:p-8 text-center space-y-4">
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                  <p className="text-red-800 font-medium">{error}</p>
                </div>

                <button
                  onClick={resetProcess}
                  className="px-8 py-3 bg-gradient-to-r from-red-600 to-pink-600 text-white font-semibold rounded-xl hover:from-red-700 hover:to-pink-700 focus:ring-4 focus:ring-red-200 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                  <span className="mr-2">🔄</span>
                  Try Again
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Job Info (for debugging) */}
        {(fileKey || jobId) && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className="bg-slate-100 border border-slate-300 rounded-xl p-4 sm:p-6">
              <h3 className="font-semibold text-slate-800 mb-4 flex items-center">
                <span className="mr-2">🔧</span>
                Debug Information
              </h3>
              <div className="space-y-3 text-sm">
                {fileKey && (
                  <div className="bg-white rounded-lg p-3 border border-slate-200">
                    <span className="font-medium text-slate-900">
                      File Key:
                    </span>
                    <p className="text-slate-700 font-mono text-xs mt-1 break-all">
                      {fileKey}
                    </p>
                  </div>
                )}
                {jobId && (
                  <div className="bg-white rounded-lg p-3 border border-slate-200">
                    <span className="font-medium text-slate-900">Job ID:</span>
                    <p className="text-slate-700 font-mono text-xs mt-1 break-all">
                      {jobId}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
