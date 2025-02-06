'use client';

import { useState, useEffect } from 'react';
import { api, type Image as ImageType } from '@/lib/api';
import LGTMImage from '@/components/LGTMImage';

export default function Home() {
  const [images, setImages] = useState<ImageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadImages();
  }, []);

  const loadImages = async () => {
    try {
      const fetchedImages = await api.getImages();
      setImages(fetchedImages);
    } catch (err) {
      console.error('Failed to load images:', err);
      setError('Failed to load images');
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const uploadedImage = await api.uploadImage(file);
      setImages(prev => [uploadedImage, ...prev]);
    } catch (err) {
      setError('Upload failed. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">LGTM Image Service</h1>
        
        {/* Upload Section */}
        <div className="mb-8">
          <label className="block mb-4">
            <span className="sr-only">Choose file</span>
            <input
              type="file"
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-violet-50 file:text-violet-700
                hover:file:bg-violet-100"
              accept="image/*"
              onChange={handleFileUpload}
              disabled={isLoading}
            />
          </label>
          
          {isLoading && (
            <div className="text-sm text-gray-500">Uploading...</div>
          )}
          
          {error && (
            <div className="text-sm text-red-500">{error}</div>
          )}
        </div>

        {/* Image Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {images.map((image) => (
            <LGTMImage key={image.id} image={image} />
          ))}
        </div>
      </div>
    </main>
  );
}