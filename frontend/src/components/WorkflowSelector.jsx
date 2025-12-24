import React from 'react'
import { motion } from 'framer-motion'

function WorkflowSelector({ onSelectWorkflow }) {
  const workflows = [
    {
      id: 'image-upload',
      title: 'Image Upload → Motion Effect',
      description: 'Upload an image and generate stunning motion effects for your ad creatives',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      ),
    },
    {
      id: 'product-url',
      title: 'Product URL → AI Ad Image',
      description: 'Enter a product URL and let AI generate professional ad creatives automatically',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
        </svg>
      ),
    },
  ]

  return (
    <div className="max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: [0.4, 0, 0.2, 1] }}
        className="text-center mb-16"
      >
        <h2 className="text-4xl md:text-5xl font-semibold mb-4 text-gray-900 tracking-tight">
          Choose Your Workflow
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto font-normal">
          Transform your ideas into premium ad creatives with AI-powered tools
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {workflows.map((workflow, index) => (
          <motion.div
            key={workflow.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ 
              duration: 0.4, 
              delay: index * 0.1,
              ease: [0.4, 0, 0.2, 1]
            }}
            whileHover={{ y: -4 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelectWorkflow(workflow.id)}
            className="premium-card p-8 cursor-pointer group"
          >
            <div className="w-12 h-12 bg-gray-900 rounded-lg flex items-center justify-center text-white mb-6 group-hover:bg-gray-800 transition-colors duration-200">
              {workflow.icon}
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900 tracking-tight">{workflow.title}</h3>
            <p className="text-gray-600 mb-6 leading-relaxed text-sm">{workflow.description}</p>
            <div className="flex items-center text-gray-900 font-medium text-sm group-hover:gap-2 transition-all duration-200">
              Get Started
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default WorkflowSelector

