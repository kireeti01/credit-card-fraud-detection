import { motion, AnimatePresence } from 'framer-motion'
import { 
  ShieldCheck, 
  ShieldAlert, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle2,
  Info,
  Copy,
  Check
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useState } from 'react'

interface ResultCardProps {
  prediction: {
    fraud: boolean
    confidence: number
    message: string
    transaction_id?: string
    timestamp?: string
  } | null
  isLoading: boolean
}

export default function ResultCard({ prediction, isLoading }: ResultCardProps) {
  const [copied, setCopied] = useState(false)

  const copyTransactionId = () => {
    if (prediction?.transaction_id) {
      navigator.clipboard.writeText(prediction.transaction_id)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const getConfidenceColor = (confidence: number, isFraud: boolean) => {
    if (isFraud) {
      if (confidence > 0.8) return 'from-red-500 to-rose-600'
      if (confidence > 0.5) return 'from-orange-500 to-amber-600'
      return 'from-yellow-500 to-amber-500'
    } else {
      if (confidence < 0.2) return 'from-emerald-500 to-green-600'
      if (confidence < 0.5) return 'from-teal-500 to-emerald-500'
      return 'from-blue-500 to-cyan-500'
    }
  }

  const getStatusIcon = (isFraud: boolean) => {
    if (isFraud) {
      return <ShieldAlert className="w-16 h-16 text-white" />
    }
    return <ShieldCheck className="w-16 h-16 text-white" />
  }

  const getStatusBg = (isFraud: boolean) => {
    if (isFraud) {
      return 'bg-gradient-to-br from-red-500 via-rose-500 to-pink-600'
    }
    return 'bg-gradient-to-br from-emerald-500 via-green-500 to-teal-600'
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
    >
      <Card className="border-slate-200 dark:border-slate-700 shadow-lg h-full">
        <CardHeader className="pb-4">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
              <TrendingUp className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <CardTitle className="text-lg">Prediction Result</CardTitle>
          </div>
        </CardHeader>

        <CardContent>
          <AnimatePresence mode="wait">
            {!prediction && !isLoading && (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center justify-center py-12 text-center"
              >
                <div className="w-24 h-24 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center mb-4">
                  <Info className="w-10 h-10 text-slate-400" />
                </div>
                <h3 className="text-lg font-medium text-slate-700 dark:text-slate-300 mb-2">
                  No Prediction Yet
                </h3>
                <p className="text-sm text-slate-500 max-w-xs">
                  Fill in the transaction details and click "Detect Fraud" to get a prediction
                </p>
              </motion.div>
            )}

            {isLoading && (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center justify-center py-12"
              >
                <motion.div
                  animate={{ 
                    rotate: 360,
                    scale: [1, 1.1, 1]
                  }}
                  transition={{ 
                    rotate: { duration: 2, repeat: Infinity, ease: 'linear' },
                    scale: { duration: 1, repeat: Infinity }
                  }}
                  className="w-20 h-20 border-4 border-blue-200 dark:border-blue-800 border-t-blue-600 rounded-full mb-4"
                />
                <p className="text-slate-600 dark:text-slate-400 font-medium">
                  Analyzing transaction...
                </p>
                <p className="text-sm text-slate-400 mt-1">
                  Running ML model inference
                </p>
              </motion.div>
            )}

            {prediction && !isLoading && (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ type: 'spring', stiffness: 200 }}
              >
                {/* Status Banner */}
                <motion.div
                  initial={{ y: -20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.1 }}
                  className={`relative overflow-hidden rounded-2xl ${getStatusBg(prediction.fraud)} p-6 mb-6`}
                >
                  <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIj48Y2lyY2xlIGN4PSIyMCIgY3k9IjIwIiByPSIyIi8+PC9nPjwvZz48L3N2Zz4=')] opacity-30"></div>
                  <div className="relative flex items-center gap-4">
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
                      className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm"
                    >
                      {getStatusIcon(prediction.fraud)}
                    </motion.div>
                    <div className="text-white">
                      <motion.div
                        initial={{ x: 20, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: 0.3 }}
                      >
                        <h3 className="text-2xl font-bold">
                          {prediction.fraud ? 'Fraud Detected!' : 'Transaction Safe'}
                        </h3>
                        <p className="text-white/80 text-sm mt-1">
                          {prediction.fraud 
                            ? 'This transaction shows suspicious patterns' 
                            : 'No fraudulent patterns detected'}
                        </p>
                      </motion.div>
                    </div>
                  </div>
                </motion.div>

                {/* Confidence Score */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.4 }}
                  className="mb-6"
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">
                      Confidence Score
                    </span>
                    <span className={`text-lg font-bold bg-gradient-to-r ${getConfidenceColor(prediction.confidence, prediction.fraud)} bg-clip-text text-transparent`}>
                      {(prediction.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="relative h-4 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${prediction.confidence * 100}%` }}
                      transition={{ duration: 1, delay: 0.5, ease: 'easeOut' }}
                      className={`absolute inset-y-0 left-0 bg-gradient-to-r ${getConfidenceColor(prediction.confidence, prediction.fraud)} rounded-full`}
                    />
                    {/* Gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                  </div>
                  <div className="flex justify-between text-xs text-slate-400 mt-1">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </motion.div>

                {/* Message */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.5 }}
                  className={`p-4 rounded-xl mb-4 ${
                    prediction.fraud 
                      ? 'bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-800' 
                      : 'bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-100 dark:border-emerald-800'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    {prediction.fraud ? (
                      <AlertTriangle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                    ) : (
                      <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-0.5 flex-shrink-0" />
                    )}
                    <p className={`text-sm ${
                      prediction.fraud 
                        ? 'text-red-700 dark:text-red-400' 
                        : 'text-emerald-700 dark:text-emerald-400'
                    }`}>
                      {prediction.message}
                    </p>
                  </div>
                </motion.div>

                {/* Transaction Details */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.6 }}
                  className="space-y-2"
                >
                  {prediction.transaction_id && (
                    <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                      <span className="text-xs text-slate-500">Transaction ID</span>
                      <div className="flex items-center gap-2">
                        <code className="text-xs bg-slate-100 dark:bg-slate-700 px-2 py-1 rounded">
                          {prediction.transaction_id.slice(0, 16)}...
                        </code>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6"
                          onClick={copyTransactionId}
                        >
                          {copied ? (
                            <Check className="w-3 h-3 text-green-500" />
                          ) : (
                            <Copy className="w-3 h-3" />
                          )}
                        </Button>
                      </div>
                    </div>
                  )}
                  
                  {prediction.timestamp && (
                    <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                      <span className="text-xs text-slate-500">Timestamp</span>
                      <span className="text-xs text-slate-700 dark:text-slate-300">
                        {new Date(prediction.timestamp).toLocaleString()}
                      </span>
                    </div>
                  )}
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>
    </motion.div>
  )
}
