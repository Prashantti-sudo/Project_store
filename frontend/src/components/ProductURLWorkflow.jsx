import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { SkeletonCategory, SkeletonAdPreview, SkeletonText } from './SkeletonLoader'

function ProductURLWorkflow() {
  const [productUrl, setProductUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingStage, setLoadingStage] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [urlError, setUrlError] = useState('')

  const validateURL = (url) => {
    try {
      const urlObj = new URL(url)
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:'
    } catch {
      return false
    }
  }

  const handleUrlChange = (e) => {
    const url = e.target.value
    setProductUrl(url)
    setError(null)
    
    if (url.trim() && !validateURL(url.trim())) {
      setUrlError('Please enter a valid URL (starting with http:// or https://)')
    } else {
      setUrlError('')
    }
  }

  const handleGenerate = async () => {
    if (!productUrl.trim()) {
      setError('Please enter a product URL')
      return
    }

    if (!validateURL(productUrl.trim())) {
      setError('Please enter a valid URL')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    setLoadingStage('Fetching product information...')

    try {
      const response = await axios.post('/api/generate-ad-from-url', {
        product_url: productUrl.trim(),
      }, {
        onUploadProgress: (progressEvent) => {
          if (progressEvent.loaded < progressEvent.total) {
            setLoadingStage('Analyzing product image and style...')
          }
        }
      })

      setLoadingStage('Generating ad creatives...')
      console.log('API Response:', response.data);
      console.log('Ad sizes:', response.data.ad_sizes);
      if (response.data.ad_sizes) {
        console.log('Facebook:', response.data.ad_sizes.facebook ? 'Present' : 'Missing');
        console.log('Twitter:', response.data.ad_sizes.twitter ? 'Present' : 'Missing');
        console.log('TikTok:', response.data.ad_sizes.tiktok ? 'Present' : 'Missing');
      }
      setResult(response.data)
      setLoadingStage('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate ad creative. Please try again.')
      setLoadingStage('')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setProductUrl('')
    setResult(null)
    setError(null)
  }

  return (
    <div className="max-w-5xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
        className="premium-card p-6 md:p-8"
      >
        <h2 className="text-3xl md:text-4xl font-semibold mb-2 text-gray-900 tracking-tight">AI Ad Image Generator</h2>
        <p className="text-gray-600 mb-8 text-sm">Enter a product URL and let AI create professional ad creatives automatically</p>

        <div className="space-y-6">
          {/* URL Input Section */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Product URL
            </label>
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <input
                  type="url"
                  value={productUrl}
                  onChange={handleUrlChange}
                  placeholder="https://example.com/product"
                  className={`w-full pl-12 pr-4 py-3 border rounded-lg focus:ring-2 transition-all outline-none text-gray-900 text-sm ${
                    urlError ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 focus:border-gray-900 focus:ring-gray-200'
                  }`}
                />
              </div>
              {productUrl && (
                <button
                  onClick={handleReset}
                  className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
            <p className="text-sm text-gray-500 mt-2">Enter any product page URL from e-commerce sites</p>
            {urlError && (
              <p className="text-sm text-red-600 mt-2">{urlError}</p>
            )}
          </div>

          {/* Generate Button */}
          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={handleGenerate}
            disabled={loading || !productUrl.trim()}
            className="btn-primary w-full flex items-center justify-center gap-2.5"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="text-sm">{loadingStage || 'Processing...'}</span>
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Generate Ad Creative
              </>
            )}
          </motion.button>

          {/* Error Message */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
                className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm"
              >
                {error}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Loading Skeleton */}
          {loading && !result && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-6"
            >
              <SkeletonCategory />
              <div className="space-y-4">
                <SkeletonText lines={2} />
                <SkeletonAdPreview />
                <SkeletonAdPreview />
                <SkeletonAdPreview />
              </div>
            </motion.div>
          )}

          {/* Result Section */}
          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                className="space-y-6"
              >
                <h3 className="text-2xl font-bold text-gray-900">Generated Ad Creative</h3>
                
                {/* Category Display */}
                {result.category && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
                    className="bg-gray-50 border border-gray-200 rounded-lg p-6"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gray-900 rounded-lg flex items-center justify-center text-white font-semibold text-lg">
                        {result.category.charAt(0)}
                      </div>
                      <div>
                        <p className="text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">Detected Style Category</p>
                        <h4 className="text-xl font-semibold text-gray-900 tracking-tight">{result.category}</h4>
                        <p className="text-sm text-gray-600 mt-1">{result.category_description || 'AI-analyzed visual style'}</p>
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Product Info */}
                {result.product_info && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.1 }}
                    className="bg-gray-50 border border-gray-200 rounded-lg p-6"
                  >
                    <h4 className="font-semibold text-gray-900 mb-4 text-sm">Product Information</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      {result.product_info.title && (
                        <div>
                          <span className="font-medium text-gray-500 text-xs uppercase tracking-wide">Title</span>
                          <p className="text-gray-900 mt-1.5 font-medium">{result.product_info.title}</p>
                        </div>
                      )}
                      {result.product_info.price && (
                        <div>
                          <span className="font-medium text-gray-500 text-xs uppercase tracking-wide">Price</span>
                          <p className="text-gray-900 mt-1.5 font-medium">{result.product_info.price}</p>
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}

                {/* Ad Platform Sizes */}
                {result.ad_sizes && Object.keys(result.ad_sizes).length > 0 && (
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-2">Ad Creatives by Platform</h4>
                      <p className="text-sm text-gray-600">Generated in multiple sizes for different social media platforms</p>
                    </div>
                    
                    {/* Facebook Feed - 1:1 */}
                    {result.ad_sizes.facebook && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                        className="space-y-3"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h5 className="font-semibold text-gray-900 text-sm">Facebook Feed</h5>
                            <p className="text-xs text-gray-500 mt-0.5">1:1 Ratio (1080×1080)</p>
                          </div>
                          <a
                            href={result.ad_sizes.facebook.url}
                            download={`facebook-ad-${result.product_info?.title?.replace(/\s+/g, '-') || 'creative'}.png`}
                            className="btn-secondary px-4 py-2 text-sm"
                          >
                            Download
                          </a>
                        </div>
                        <div className="bg-gray-100 rounded-lg p-4 flex justify-center">
                          <img
                            src={result.ad_sizes.facebook.url}
                            alt="Facebook Ad"
                            className="max-w-full h-auto rounded-lg shadow-soft"
                            style={{ maxHeight: '400px' }}
                            onError={(e) => {
                              console.error('Error loading Facebook ad image');
                              e.target.style.display = 'none';
                            }}
                          />
                        </div>
                      </motion.div>
                    )}

                    {/* X/Twitter - 16:9 */}
                    {result.ad_sizes.twitter && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.1 }}
                        className="space-y-3"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h5 className="font-semibold text-gray-900 text-sm">X / Twitter</h5>
                            <p className="text-xs text-gray-500 mt-0.5">16:9 Ratio (1200×675)</p>
                          </div>
                          <a
                            href={result.ad_sizes.twitter.url}
                            download={`twitter-ad-${result.product_info?.title?.replace(/\s+/g, '-') || 'creative'}.png`}
                            className="btn-secondary px-4 py-2 text-sm"
                          >
                            Download
                          </a>
                        </div>
                        <div className="bg-gray-100 rounded-lg p-4 flex justify-center">
                          <img
                            src={result.ad_sizes.twitter.url}
                            alt="Twitter Ad"
                            className="max-w-full h-auto rounded-lg shadow-soft"
                            style={{ maxHeight: '300px' }}
                            onError={(e) => {
                              console.error('Error loading Twitter ad image');
                              e.target.style.display = 'none';
                            }}
                          />
                        </div>
                      </motion.div>
                    )}

                    {/* TikTok/Reels - 9:16 */}
                    {result.ad_sizes.tiktok && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.2 }}
                        className="space-y-3"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h5 className="font-semibold text-gray-900 text-sm">TikTok / Reels</h5>
                            <p className="text-xs text-gray-500 mt-0.5">9:16 Ratio (1080×1920)</p>
                          </div>
                          <a
                            href={result.ad_sizes.tiktok.url}
                            download={`tiktok-ad-${result.product_info?.title?.replace(/\s+/g, '-') || 'creative'}.png`}
                            className="btn-secondary px-4 py-2 text-sm"
                          >
                            Download
                          </a>
                        </div>
                        <div className="bg-gray-100 rounded-lg p-4 flex justify-center">
                          <img
                            src={result.ad_sizes.tiktok.url}
                            alt="TikTok Ad"
                            className="max-w-full h-auto rounded-lg shadow-soft"
                            style={{ maxHeight: '500px' }}
                            onError={(e) => {
                              console.error('Error loading TikTok ad image');
                              e.target.style.display = 'none';
                            }}
                          />
                        </div>
                      </motion.div>
                    )}

                    {/* Download All Button */}
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3, delay: 0.3 }}
                      className="pt-6 border-t border-gray-200"
                    >
                      <button
                        onClick={() => {
                          // Download all images
                          if (result.ad_sizes.facebook) {
                            const link = document.createElement('a')
                            link.href = result.ad_sizes.facebook.url
                            link.download = `facebook-ad-${result.product_info?.title?.replace(/\s+/g, '-') || 'creative'}.png`
                            link.click()
                          }
                          setTimeout(() => {
                            if (result.ad_sizes.twitter) {
                              const link = document.createElement('a')
                              link.href = result.ad_sizes.twitter.url
                              link.download = `twitter-ad-${result.product_info?.title?.replace(/\s+/g, '-') || 'creative'}.png`
                              link.click()
                            }
                          }, 500)
                          setTimeout(() => {
                            if (result.ad_sizes.tiktok) {
                              const link = document.createElement('a')
                              link.href = result.ad_sizes.tiktok.url
                              link.download = `tiktok-ad-${result.product_info?.title?.replace(/\s+/g, '-') || 'creative'}.png`
                              link.click()
                            }
                          }, 1000)
                        }}
                        className="w-full btn-primary flex items-center justify-center gap-2"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        Download All Ad Sizes
                      </button>
                    </motion.div>
                  </div>
                )}

                {/* Fallback: Generated Images (if ad_sizes not available) */}
                {(!result.ad_sizes || Object.keys(result.ad_sizes).length === 0) && result.ad_images && result.ad_images.length > 0 && (
                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">Ad Creatives</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {result.ad_images.map((image, index) => (
                        <div key={index} className="rounded-xl overflow-hidden shadow-lg">
                          <img
                            src={image.url}
                            alt={`Ad Creative ${index + 1}`}
                            className="w-full h-auto"
                          />
                          {image.description && (
                            <div className="bg-white p-4 border-t">
                              <p className="text-sm text-gray-600">{image.description}</p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Generated Keywords */}
                {result.keywords && result.keywords.length > 0 && (
                  <div className="bg-gray-50 rounded-xl p-6">
                    <h4 className="font-semibold text-gray-900 mb-3">Generated Keywords</h4>
                    <div className="flex flex-wrap gap-2">
                      {result.keywords.map((keyword, index) => (
                        <span
                          key={index}
                          className="bg-white border border-gray-200 px-4 py-2 rounded-full text-sm text-gray-700 font-medium"
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  )
}

export default ProductURLWorkflow

