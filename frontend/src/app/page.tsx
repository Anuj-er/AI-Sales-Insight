"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { UploadCloud, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

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
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
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

    setStatus("loading");
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("email", email);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await axios.post(`${apiUrl}/api/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-API-Key": process.env.NEXT_PUBLIC_API_KEY || "default-dev-key"
        },
      });
      setStatus("success");
      setMessage(response.data.message || "Summary successfully generated and sent! Check your inbox.");
    } catch (err: any) {
      setStatus("error");
      setMessage(
        err.response?.data?.detail ||
        "An unexpected error occurred. Ensure the backend is running and reachable."
      );
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900 flex flex-col items-center justify-center p-6 font-sans">
      <div className="w-full max-w-xl bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden">
        <div className="p-8 border-b border-gray-100 bg-white flex flex-col items-center">
          <img src="/logo.png" alt="Sales Insight Automator Logo" className="w-16 h-16 mb-6 drop-shadow-sm" />
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 text-center">
            Sales Insight Automator
          </h1>
          <p className="text-gray-500 mt-3 text-sm leading-relaxed text-center max-w-sm">
            Upload your quarterly sales data (CSV/Excel) to securely generate a professional executive narrative delivered straight to your inbox.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          <div className="space-y-4">
            <label className="block text-sm font-medium text-gray-700">Data File</label>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center transition-all cursor-pointer bg-gray-50/50 ${isDragActive ? "border-indigo-500 bg-indigo-50/50" : "border-gray-300 hover:border-indigo-400 hover:bg-gray-50"
                }`}
            >
              <input {...getInputProps()} />
              <UploadCloud className={`w-8 h-8 mb-3 ${isDragActive ? "text-indigo-500" : "text-gray-400"}`} />
              <p className="text-sm font-medium text-gray-700 text-center">
                {file ? file.name : (isDragActive ? "Drop file here..." : "Drag & drop your CSV or Excel file here")}
              </p>
              {!file && <p className="text-xs text-gray-500 mt-1">or click to browse from your computer</p>}
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Recipient Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="executive@company.com"
              className="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-gray-900 placeholder-gray-400 shadow-sm"
              required
            />
          </div>

          <button
            type="submit"
            disabled={status === "loading" || !file || !email}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 rounded-lg flex items-center justify-center transition-all disabled:opacity-70 disabled:cursor-not-allowed shadow-sm"
          >
            {status === "loading" ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Processing...
              </>
            ) : "Generate & Send Insight Brief"}
          </button>
        </form>

        {status !== "idle" && status !== "loading" && (
          <div className={`p-4 mx-8 mb-8 rounded-lg border flex items-start space-x-3 text-sm animate-in fade-in slide-in-from-bottom-2 ${status === "success"
            ? "bg-green-50 border-green-200 text-green-800"
            : "bg-red-50 border-red-200 text-red-800"
            }`}>
            {status === "success" ? <CheckCircle className="w-5 h-5 shrink-0 mt-0.5 text-green-600" /> : <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-red-600" />}
            <span className="leading-relaxed">{message}</span>
          </div>
        )}
      </div>

      <p className="mt-8 text-gray-400 text-xs text-center uppercase tracking-wider font-semibold">
        Powered by Next.js, FastAPI & Groq
      </p>
    </main>
  );
}
