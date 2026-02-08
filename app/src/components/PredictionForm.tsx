import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Send, 
  RotateCcw, 
  Clock, 
  DollarSign,
  Sparkles,
  ChevronDown,
  ChevronUp
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

interface PredictionFormProps {
  onSubmit: (data: any) => void
  isLoading: boolean
}

const defaultValues = {
  time: 0,
  v1: 0, v2: 0, v3: 0, v4: 0, v5: 0,
  v6: 0, v7: 0, v8: 0, v9: 0, v10: 0,
  v11: 0, v12: 0, v13: 0, v14: 0, v15: 0,
  v16: 0, v17: 0, v18: 0, v19: 0, v20: 0,
  v21: 0, v22: 0, v23: 0, v24: 0, v25: 0,
  v26: 0, v27: 0, v28: 0,
  amount: 100
}

export default function PredictionForm({ onSubmit, isLoading }: PredictionFormProps) {
  const [formData, setFormData] = useState(defaultValues)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [fillProgress, setFillProgress] = useState(0)

  const handleChange = (field: string, value: number) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    
    // Calculate fill progress
    const filled = Object.values({ ...formData, [field]: value }).filter(v => v !== 0).length
    setFillProgress((filled / 30) * 100)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handleReset = () => {
    setFormData(defaultValues)
    setFillProgress(0)
  }

  const fillRandomData = () => {
    const randomData = {
      time: Math.random() * 172792,
      v1: (Math.random() - 0.5) * 4,
      v2: (Math.random() - 0.5) * 4,
      v3: (Math.random() - 0.5) * 4,
      v4: (Math.random() - 0.5) * 4,
      v5: (Math.random() - 0.5) * 4,
      v6: (Math.random() - 0.5) * 4,
      v7: (Math.random() - 0.5) * 4,
      v8: (Math.random() - 0.5) * 4,
      v9: (Math.random() - 0.5) * 4,
      v10: (Math.random() - 0.5) * 4,
      v11: (Math.random() - 0.5) * 4,
      v12: (Math.random() - 0.5) * 4,
      v13: (Math.random() - 0.5) * 4,
      v14: (Math.random() - 0.5) * 4,
      v15: (Math.random() - 0.5) * 4,
      v16: (Math.random() - 0.5) * 4,
      v17: (Math.random() - 0.5) * 4,
      v18: (Math.random() - 0.5) * 4,
      v19: (Math.random() - 0.5) * 4,
      v20: (Math.random() - 0.5) * 4,
      v21: (Math.random() - 0.5) * 4,
      v22: (Math.random() - 0.5) * 4,
      v23: (Math.random() - 0.5) * 4,
      v24: (Math.random() - 0.5) * 4,
      v25: (Math.random() - 0.5) * 4,
      v26: (Math.random() - 0.5) * 4,
      v27: (Math.random() - 0.5) * 4,
      v28: (Math.random() - 0.5) * 4,
      amount: Math.random() * 1000
    }
    setFormData(randomData)
    setFillProgress(100)
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="border-slate-200 dark:border-slate-700 shadow-lg">
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <Sparkles className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <CardTitle className="text-lg">Transaction Input</CardTitle>
            </div>
            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={fillRandomData}
                className="text-xs"
              >
                Random
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={handleReset}
                className="text-xs"
              >
                <RotateCcw className="w-3 h-3 mr-1" />
                Reset
              </Button>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-3">
            <div className="flex justify-between text-xs text-slate-500 mb-1">
              <span>Form Completion</span>
              <span>{Math.round(fillProgress)}%</span>
            </div>
            <Progress value={fillProgress} className="h-1.5" />
          </div>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Primary Fields */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="time" className="flex items-center gap-1.5 text-sm">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  Time
                </Label>
                <Input
                  id="time"
                  type="number"
                  step="0.01"
                  value={formData.time}
                  onChange={(e) => handleChange('time', parseFloat(e.target.value) || 0)}
                  className="h-9"
                  placeholder="0.0"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="amount" className="flex items-center gap-1.5 text-sm">
                  <DollarSign className="w-3.5 h-3.5 text-slate-400" />
                  Amount
                </Label>
                <Input
                  id="amount"
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => handleChange('amount', parseFloat(e.target.value) || 0)}
                  className="h-9"
                  placeholder="0.0"
                />
              </div>
            </div>

            {/* Advanced Fields Toggle */}
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
            >
              {showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              {showAdvanced ? 'Hide' : 'Show'} PCA Features (V1-V28)
            </button>

            {/* V Features Grid */}
            <motion.div
              initial={false}
              animate={{ 
                height: showAdvanced ? 'auto' : 0,
                opacity: showAdvanced ? 1 : 0
              }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="grid grid-cols-4 gap-2 pt-2">
                {Array.from({ length: 28 }, (_, i) => i + 1).map((num) => (
                  <div key={`v${num}`} className="space-y-1">
                    <Label htmlFor={`v${num}`} className="text-xs text-slate-500">
                      V{num}
                    </Label>
                    <Input
                      id={`v${num}`}
                      type="number"
                      step="0.01"
                      value={formData[`v${num}` as keyof typeof formData]}
                      onChange={(e) => handleChange(`v${num}`, parseFloat(e.target.value) || 0)}
                      className="h-8 text-xs"
                    />
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Submit Button */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
              >
                {isLoading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                    className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                  />
                ) : (
                  <>
                    <Send className="w-4 h-4 mr-2" />
                    Detect Fraud
                  </>
                )}
              </Button>
            </motion.div>
          </form>
        </CardContent>
      </Card>
    </motion.div>
  )
}
