import React from 'react'
import { motion } from 'framer-motion'

export function SkeletonCard() {
  return (
    <div className="premium-card p-6 md:p-8 space-y-4">
      <div className="skeleton-shimmer h-8 w-3/4 rounded-lg"></div>
      <div className="skeleton-shimmer h-4 w-full rounded"></div>
      <div className="skeleton-shimmer h-4 w-5/6 rounded"></div>
      <div className="skeleton-shimmer h-32 w-full rounded-lg mt-4"></div>
    </div>
  )
}

export function SkeletonImage({ width = 'full', height = '400px' }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={`skeleton-shimmer rounded-xl`}
      style={{ width, height }}
    />
  )
}

export function SkeletonText({ lines = 3, className = '' }) {
  return (
    <div className={`space-y-2 ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={`skeleton-shimmer h-4 rounded ${
            i === lines - 1 ? 'w-3/4' : 'w-full'
          }`}
        />
      ))}
    </div>
  )
}

export function SkeletonButton({ className = '' }) {
  return (
    <div className={`skeleton-shimmer h-10 w-32 rounded-lg ${className}`} />
  )
}

export function SkeletonAdPreview() {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="skeleton-shimmer h-5 w-32 rounded"></div>
          <div className="skeleton-shimmer h-4 w-24 rounded"></div>
        </div>
        <div className="skeleton-shimmer h-9 w-24 rounded-lg"></div>
      </div>
      <div className="bg-gray-100 rounded-xl p-4 flex justify-center">
        <div className="skeleton-shimmer h-64 w-64 rounded-lg"></div>
      </div>
    </div>
  )
}

export function SkeletonCategory() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-gray-50 border border-gray-200 rounded-xl p-6"
    >
      <div className="flex items-center gap-4">
        <div className="skeleton-shimmer w-16 h-16 rounded-xl"></div>
        <div className="flex-1 space-y-2">
          <div className="skeleton-shimmer h-4 w-32 rounded"></div>
          <div className="skeleton-shimmer h-6 w-48 rounded"></div>
          <div className="skeleton-shimmer h-3 w-40 rounded"></div>
        </div>
      </div>
    </motion.div>
  )
}




