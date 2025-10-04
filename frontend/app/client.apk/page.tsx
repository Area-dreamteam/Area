'use client'
import { useEffect } from 'react';

export default function APKDownloadPage() {
  useEffect(() => {
    const link = document.createElement('a');
    link.href = '/files/client.apk';
    link.download = 'client.apk';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Downloading client.apk...</h1>
        <p className="text-gray-600 mb-4">Your download should start automatically.</p>
        <p className="text-sm text-gray-500">
          If it doesn't, <a href="/files/client.apk" className="text-blue-600 underline">click here</a>.
        </p>
      </div>
    </div>
  );
}
