/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** page
 */

'use client'

import { Input } from '@/components/ui/input'
import { useRouter } from 'next/navigation'

export default function Help() {
  const router = useRouter();

  return (
    <div>
      <p
        className="hover:cursor-pointer text-[40px]  font-bold hover:text-[#3b3b3b]"
        onClick={(e) => {
          e.preventDefault()
          router.push('/explore')
        }}
      >
        Area
      </p>
      <h1 className="centered mt-[150px] text-[50px] font-bold mb-[20px]">
        Help Center
      </h1>
      <h2 className="centered text-[25px] text-[#8a8a8a] mb-[20px]">
        Answers to frequently asked questions
      </h2>
      <div className="max-w-4xl mx-auto mt-10 space-y-6">
        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <h3 className="text-2xl font-bold mb-3">📚 User Journey Guide</h3>
          <p className="text-gray-700 mb-4">
            Learn how to use AREA from start to finish - registration, creating applets, managing services, and more.
          </p>
          <div className="flex gap-4">
            <a
              href="https://github.com/Area-dreamteam/Area/wiki/User-journey_AREA.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 font-semibold underline"
            >
              View PDF Guide →
            </a>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <h3 className="text-2xl font-bold mb-3">🔧 Developer Documentation</h3>
          <p className="text-gray-700 mb-4">
            Technical guides for implementing services, OAuth flows, and automation features.
          </p>
          <a
            href="https://github.com/Area-dreamteam/Area/wiki"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 font-semibold underline"
          >
            View Developer Wiki →
          </a>
        </div>
      </div>
    </div>
  )
}
