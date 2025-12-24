import React from 'react'
import { motion } from 'framer-motion'
import Header from './components/Header'
import WorkflowSelector from './components/WorkflowSelector'
import ImageUploadWorkflow from './components/ImageUploadWorkflow'
import ProductURLWorkflow from './components/ProductURLWorkflow'

function App() {
  const [activeWorkflow, setActiveWorkflow] = React.useState(null)

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-8 md:py-12">
        {!activeWorkflow ? (
          <WorkflowSelector onSelectWorkflow={setActiveWorkflow} />
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <button
              onClick={() => setActiveWorkflow(null)}
              className="mb-6 flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Workflows
            </button>
            {activeWorkflow === 'image-upload' && <ImageUploadWorkflow />}
            {activeWorkflow === 'product-url' && <ProductURLWorkflow />}
          </motion.div>
        )}
      </main>
    </div>
  )
}

export default App




