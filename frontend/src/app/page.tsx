"use client";

import { useState } from "react";
import Image from "next/image";
import { useDropzone } from "react-dropzone";
import axios, { AxiosError } from "axios";
import { UploadCloud, CheckCircle, AlertCircle, Loader2, FileText, Mail } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "text/csv": [".csv"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    },
    maxFiles: 1,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !email) {
      setStatus("error");
      setMessage("Please provide both a file and an email address.");
      return;
    }

    // Read file into memory BEFORE state changes trigger re-renders.
    // Re-renders can invalidate the browser's file input reference, causing
    // ERR_UPLOAD_FILE_CHANGED when the DOM input element is recreated.
    let fileBuffer: ArrayBuffer;
    try {
      fileBuffer = await file.arrayBuffer();
    } catch {
      setStatus("error");
      setMessage("Failed to read the file. Please try selecting it again.");
      return;
    }

    setStatus("loading");
    setMessage("");

    const fileBlob = new Blob([fileBuffer], { type: file.type });
    const formData = new FormData();
    formData.append("file", fileBlob, file.name);
    formData.append("email", email);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await axios.post(`${apiUrl}/api/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-API-Key": process.env.NEXT_PUBLIC_API_KEY || "default-dev-key",
        },
      });
      setStatus("success");
      setMessage(response.data.message || "Summary successfully generated and sent! Check your inbox.");
    } catch (err) {
      const error = err as AxiosError<{ detail: string }>;
      setStatus("error");
      setMessage(
        error.response?.data?.detail ||
          "An unexpected error occurred. Ensure the backend is running and reachable."
      );
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6">
      {/* Page header */}
      <div className="w-full max-w-md mb-8 flex flex-col items-center">
        <Image src="/logo.png" alt="Sales Insight Automator" width={40} height={40} className="mb-4" />
        <h1 className="text-xl font-semibold text-slate-800 tracking-tight text-center">
          Sales Insight Automator
        </h1>
        <p className="text-sm text-slate-400 mt-1.5 text-center leading-relaxed max-w-xs">
          Upload your sales data and receive an AI‑generated executive summary straight to your inbox.
        </p>
      </div>

      {/* Card */}
      <div className="w-full max-w-md bg-white rounded-2xl border border-slate-100 shadow-sm p-8 space-y-5">
        {/* File upload zone */}
        <div className="space-y-1.5">
          <label className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            Data File
          </label>
          <div
            {...getRootProps()}
            className={`rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer transition-all duration-200 ${
              isDragActive
                ? "border-2 border-sky-300 bg-sky-50"
                : file
                ? "border border-slate-200 bg-slate-50"
                : "border-2 border-dashed border-slate-200 bg-slate-50/40 hover:bg-slate-50 hover:border-slate-300"
            }`}
          >
            <input {...getInputProps()} />
            {file ? (
              <div className="flex items-center gap-3 w-full">
                <div className="w-9 h-9 rounded-lg bg-sky-50 border border-sky-100 flex items-center justify-center shrink-0">
                  <FileText className="w-4 h-4 text-sky-500" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-slate-700 truncate">{file.name}</p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {(file.size / 1024).toFixed(1)} KB &middot; click to change
                  </p>
                </div>
              </div>
            ) : (
              <>
                <div
                  className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${
                    isDragActive ? "bg-sky-100" : "bg-slate-100"
                  }`}
                >
                  <UploadCloud
                    className={`w-5 h-5 ${isDragActive ? "text-sky-500" : "text-slate-400"}`}
                  />
                </div>
                <p className="text-sm font-medium text-slate-600">
                  {isDragActive ? "Release to upload" : "Drop your file here"}
                </p>
                <p className="text-xs text-slate-400 mt-1">CSV or Excel &middot; click to browse</p>
              </>
            )}
          </div>
        </div>

        {/* Email input */}
        <div className="space-y-1.5">
          <label
            htmlFor="email"
            className="text-xs font-medium text-slate-400 uppercase tracking-wider"
          >
            Recipient Email
          </label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-300 pointer-events-none" />
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="executive@company.com"
              className="w-full pl-9 pr-4 py-2.5 text-sm border border-slate-200 rounded-xl bg-white text-slate-800 placeholder-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-200 focus:border-sky-300 transition-all"
              required
            />
          </div>
        </div>

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={status === "loading" || !file || !email}
          className="w-full bg-slate-800 hover:bg-slate-700 active:bg-slate-900 text-white text-sm font-medium py-2.5 rounded-xl flex items-center justify-center gap-2 transition-all duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {status === "loading" ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Processing…
            </>
          ) : (
            "Generate & Send Brief"
          )}
        </button>

        {/* Status feedback */}
        {status !== "idle" && status !== "loading" && (
          <div
            className={`flex items-start gap-2.5 p-3.5 rounded-xl text-sm border ${
              status === "success"
                ? "bg-emerald-50 border-emerald-100 text-emerald-700"
                : "bg-red-50 border-red-100 text-red-600"
            }`}
          >
            {status === "success" ? (
              <CheckCircle className="w-4 h-4 shrink-0 mt-0.5" />
            ) : (
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            )}
            <span className="leading-relaxed">{message}</span>
          </div>
        )}
      </div>

      <p className="mt-6 text-xs text-slate-300 tracking-widest uppercase text-center">
        Powered by Next.js &middot; FastAPI &middot; Groq
      </p>
    </main>
  );
}
