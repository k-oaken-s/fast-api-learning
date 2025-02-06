'use client';

import { useState } from 'react';
import Image from 'next/image';
import { api, type Image as ImageType } from '@/lib/api';

interface LGTMImageProps {
  image: ImageType;
}

export default function LGTMImage({ image }: LGTMImageProps) {
  const [isProcessing, setIsProcessing] = useState(false);
  const [customText, setCustomText] = useState("LGTM");
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);

  const handleAddLGTM = async () => {
    setIsProcessing(true);
    try {
      const blob = await api.addLgtmToImage(image.id, customText);
      const url = URL.createObjectURL(blob);
      setProcessedImageUrl(url);
    } catch (error) {
      console.error('Failed to add LGTM:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCopyToClipboard = async () => {
    if (processedImageUrl) {
      try {
        const response = await fetch(processedImageUrl);
        const blob = await response.blob();
        await navigator.clipboard.write([
          new ClipboardItem({
            [blob.type]: blob
          })
        ]);
        alert('Image copied to clipboard!');
      } catch (err) {
        console.error('Failed to copy:', err);
        alert('Failed to copy image. Try right-clicking and copying manually.');
      }
    }
  };

  return (
    <div className="relative group">
      <div className="aspect-square relative">
        <Image
          src={processedImageUrl || image.url}
          alt={image.title || 'LGTM Image'}
          fill
          className="object-cover rounded-lg"
        />
      </div>
      
      <div className="absolute bottom-0 left-0 right-0 p-4 bg-black bg-opacity-50 rounded-b-lg">
        <div className="flex flex-col gap-2">
          <input
            type="text"
            value={customText}
            onChange={(e) => setCustomText(e.target.value)}
            className="px-2 py-1 text-sm rounded bg-white text-black"
            placeholder="Custom text..."
          />
          
          <div className="flex gap-2">
            <button
              onClick={handleAddLGTM}
              disabled={isProcessing}
              className="px-3 py-1 bg-violet-500 text-white rounded text-sm hover:bg-violet-600 disabled:opacity-50"
            >
              {isProcessing ? 'Processing...' : 'Add Text'}
            </button>
            
            {processedImageUrl && (
              <button
                onClick={handleCopyToClipboard}
                className="px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600"
              >
                Copy
              </button>
            )}
          </div>
        </div>
      </div>
      
      {/* Tags */}
      <div className="absolute top-2 left-2 flex flex-wrap gap-1">
        {image.tags.map((tag) => (
          <span
            key={tag.id}
            className="text-xs text-white px-2 py-1 rounded-full bg-violet-500 bg-opacity-75"
          >
            {tag.name}
          </span>
        ))}
      </div>
    </div>
  );
}