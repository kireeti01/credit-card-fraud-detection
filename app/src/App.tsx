import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Shield, 
  Moon, 
  Sun, 
  Activity, 
  BarChart3, 
  History,
  Brain,
  AlertTriangle,
  CheckCircle2
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Toaster } from '@/components/ui/sonner'
import { toast } from 'sonner'

import PredictionForm from './components/PredictionForm'
import ResultCard from './components/ResultCard'
import AnalyticsDashboard from './components/AnalyticsDashboard'
import TransactionHistory from './components/TransactionHistory'
import { ThemeProvider, useTheme } from './context/ThemeContext'
import './App.css'

// Animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { 
      staggerChildren: 0.1,
      delayChildren: 0.2 
    }
  }
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { 
    y: 0, 
    opacity: 1,
    transition: { type: 'spring' as const, stiffness: 100 }
  }
}

function AppContent() {
  const { theme, toggleTheme } = useTheme()
  const [prediction, setPrediction] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [stats, setStats] = useState({
    totalPredictions: 0,
    fraudCount: 0,
    safeCount: 0,
    fraudPercentage: 0
  })

  // Fetch stats on mount
  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/stats')
      if (response.ok) {
        const data = await response.json()
        if (data.data) {
          setStats({
            totalPredictions: data.data.total_predictions || 0,
            fraudCount: data.data.fraud_count || 0,
            safeCount: data.data.safe_count || 0,
            fraudPercentage: data.data.fraud_percentage || 0
          })
        }
      }
    } catch (error) {
      console.log('Backend not connected, using mock stats')
    }
  }

  const handlePrediction = async (formData: any) => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        throw new Error('Prediction failed')
      }

      const result = await response.json()
      setPrediction(result)
      toast.success('Prediction completed!')
      
      // Update stats
      fetchStats()
    } catch (error) {
      toast.error('Failed to get prediction. Is the backend running?')
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuickTest = async (type: 'fraud' | 'safe') => {
    setIsLoading(true)
    
    // Generate test data
    const testData = type === 'fraud' 
      ? generateFraudulentTransaction()
      : generateSafeTransaction()
    
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testData)
      })

      if (!response.ok) {
        throw new Error('Prediction failed')
      }

      const result = await response.json()
      setPrediction(result)
      toast.success(`${type === 'fraud' ? 'Fraudulent' : 'Safe'} transaction test completed!`)
      fetchStats()
    } catch (error) {
      toast.error('Failed to get prediction. Is the backend running?')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 transition-colors duration-300">
      {/* Header */}
      <motion.header 
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="sticky top-0 z-50 backdrop-blur-lg bg-white/70 dark:bg-slate-900/70 border-b border-slate-200 dark:border-slate-700"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <motion.div 
              className="flex items-center gap-3"
              whileHover={{ scale: 1.02 }}
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg blur opacity-50"></div>
                <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                  <Shield className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  FraudGuard AI
                </h1>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Intelligent Fraud Detection
                </p>
              </div>
            </motion.div>

            <div className="flex items-center gap-4">
              {/* Stats Pills */}
              <div className="hidden md:flex items-center gap-2">
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-100 dark:bg-emerald-900/30 rounded-full"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
                  <span className="text-xs font-medium text-emerald-700 dark:text-emerald-400">
                    {stats.safeCount} Safe
                  </span>
                </motion.div>
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-rose-100 dark:bg-rose-900/30 rounded-full"
                >
                  <AlertTriangle className="w-3.5 h-3.5 text-rose-600 dark:text-rose-400" />
                  <span className="text-xs font-medium text-rose-700 dark:text-rose-400">
                    {stats.fraudCount} Fraud
                  </span>
                </motion.div>
              </div>

              {/* Theme Toggle */}
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleTheme}
                className="rounded-full hover:bg-slate-200 dark:hover:bg-slate-700"
              >
                <AnimatePresence mode="wait">
                  {theme === 'dark' ? (
                    <motion.div
                      key="sun"
                      initial={{ rotate: -90, opacity: 0 }}
                      animate={{ rotate: 0, opacity: 1 }}
                      exit={{ rotate: 90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <Sun className="w-5 h-5 text-amber-400" />
                    </motion.div>
                  ) : (
                    <motion.div
                      key="moon"
                      initial={{ rotate: 90, opacity: 0 }}
                      animate={{ rotate: 0, opacity: 1 }}
                      exit={{ rotate: -90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <Moon className="w-5 h-5 text-slate-600" />
                    </motion.div>
                  )}
                </AnimatePresence>
              </Button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Hero Section */}
          <motion.section variants={itemVariants} className="mb-8">
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-8 text-white">
              <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIj48Y2lyY2xlIGN4PSIzMCIgY3k9IjMwIiByPSIyIi8+PC9nPjwvZz48L3N2Zz4=')] opacity-30"></div>
              <div className="relative">
                <div className="flex items-center gap-3 mb-4">
                  <Brain className="w-8 h-8" />
                  <span className="px-3 py-1 bg-white/20 rounded-full text-sm font-medium">
                    ML-Powered
                  </span>
                </div>
                <h2 className="text-3xl font-bold mb-2">
                  Credit Card Fraud Detection
                </h2>
                <p className="text-white/80 max-w-2xl">
                  Advanced machine learning system that analyzes transactions in real-time 
                  to detect fraudulent activities with high accuracy.
                </p>
                
                {/* Quick Test Buttons */}
                <div className="flex gap-3 mt-6">
                  <Button
                    onClick={() => handleQuickTest('safe')}
                    disabled={isLoading}
                    className="bg-white/20 hover:bg-white/30 text-white border-0"
                  >
                    <CheckCircle2 className="w-4 h-4 mr-2" />
                    Test Safe Transaction
                  </Button>
                  <Button
                    onClick={() => handleQuickTest('fraud')}
                    disabled={isLoading}
                    variant="outline"
                    className="border-white/30 text-white hover:bg-white/20 hover:text-white"
                  >
                    <AlertTriangle className="w-4 h-4 mr-2" />
                    Test Fraud Transaction
                  </Button>
                </div>
              </div>
            </div>
          </motion.section>

          {/* Tabs Content */}
          <motion.section variants={itemVariants}>
            <Tabs defaultValue="predict" className="space-y-6">
              <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
                <TabsTrigger value="predict" className="flex items-center gap-2">
                  <Activity className="w-4 h-4" />
                  <span className="hidden sm:inline">Predict</span>
                </TabsTrigger>
                <TabsTrigger value="analytics" className="flex items-center gap-2">
                  <BarChart3 className="w-4 h-4" />
                  <span className="hidden sm:inline">Analytics</span>
                </TabsTrigger>
                <TabsTrigger value="history" className="flex items-center gap-2">
                  <History className="w-4 h-4" />
                  <span className="hidden sm:inline">History</span>
                </TabsTrigger>
              </TabsList>

              <TabsContent value="predict" className="space-y-6">
                <div className="grid lg:grid-cols-2 gap-6">
                  <PredictionForm 
                    onSubmit={handlePrediction} 
                    isLoading={isLoading} 
                  />
                  <ResultCard 
                    prediction={prediction} 
                    isLoading={isLoading} 
                  />
                </div>
              </TabsContent>

              <TabsContent value="analytics">
                <AnalyticsDashboard stats={stats} />
              </TabsContent>

              <TabsContent value="history">
                <TransactionHistory />
              </TabsContent>
            </Tabs>
          </motion.section>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-slate-500 dark:text-slate-400">
              © 2026 FraudGuard AI. Built with FastAPI + React + ML
            </p>
            <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
              <span className="flex items-center gap-1.5">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                System Online
              </span>
              <span>v1.0.0</span>
            </div>
          </div>
        </div>
      </footer>

      <Toaster position="top-right" richColors />
    </div>
  )
}

// Helper functions to generate test data
function generateSafeTransaction() {
  return {
    time: Math.random() * 172792,
    v1: (Math.random() - 0.5) * 2,
    v2: (Math.random() - 0.5) * 2,
    v3: (Math.random() - 0.5) * 2,
    v4: (Math.random() - 0.5) * 2,
    v5: (Math.random() - 0.5) * 2,
    v6: (Math.random() - 0.5) * 2,
    v7: (Math.random() - 0.5) * 2,
    v8: (Math.random() - 0.5) * 2,
    v9: (Math.random() - 0.5) * 2,
    v10: (Math.random() - 0.5) * 2,
    v11: (Math.random() - 0.5) * 2,
    v12: (Math.random() - 0.5) * 2,
    v13: (Math.random() - 0.5) * 2,
    v14: (Math.random() - 0.5) * 2,
    v15: (Math.random() - 0.5) * 2,
    v16: (Math.random() - 0.5) * 2,
    v17: (Math.random() - 0.5) * 2,
    v18: (Math.random() - 0.5) * 2,
    v19: (Math.random() - 0.5) * 2,
    v20: (Math.random() - 0.5) * 2,
    v21: (Math.random() - 0.5) * 2,
    v22: (Math.random() - 0.5) * 2,
    v23: (Math.random() - 0.5) * 2,
    v24: (Math.random() - 0.5) * 2,
    v25: (Math.random() - 0.5) * 2,
    v26: (Math.random() - 0.5) * 2,
    v27: (Math.random() - 0.5) * 2,
    v28: (Math.random() - 0.5) * 2,
    amount: 20 + Math.random() * 200
  }
}

function generateFraudulentTransaction() {
  return {
    time: Math.random() * 172792,
    v1: 2 + Math.random() * 3,
    v2: -2 + Math.random() * 2,
    v3: 2 + Math.random() * 3,
    v4: 1 + Math.random() * 2,
    v5: -1 + Math.random() * 2,
    v6: 1 + Math.random() * 2,
    v7: 0.5 + Math.random() * 2,
    v8: -0.5 + Math.random() * 2,
    v9: 1 + Math.random() * 2,
    v10: 0.5 + Math.random() * 2,
    v11: -1 + Math.random() * 2,
    v12: -1.5 + Math.random() * 2,
    v13: -2 + Math.random() * 2,
    v14: -1 + Math.random() * 2,
    v15: 1.5 + Math.random() * 2,
    v16: -1 + Math.random() * 2,
    v17: 0.5 + Math.random() * 2,
    v18: 0.2 + Math.random() * 2,
    v19: 1 + Math.random() * 2,
    v20: 0.5 + Math.random() * 2,
    v21: -0.5 + Math.random() * 2,
    v22: 0.5 + Math.random() * 2,
    v23: -0.5 + Math.random() * 2,
    v24: 0.2 + Math.random() * 2,
    v25: 0.5 + Math.random() * 2,
    v26: -0.5 + Math.random() * 2,
    v27: 0.5 + Math.random() * 2,
    v28: -0.2 + Math.random() * 2,
    amount: 500 + Math.random() * 2000
  }
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  )
}

export default App
