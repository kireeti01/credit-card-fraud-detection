import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  History, 
  AlertTriangle, 
  CheckCircle2, 
  RefreshCw,
  Search,
  Filter,
  ChevronLeft,
  ChevronRight,
  Shield,
  Clock
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

interface Transaction {
  _id: string
  transaction_id: string
  prediction: boolean
  confidence: number
  timestamp: string
  input_features?: {
    amount?: number
    time?: number
  }
}

export default function TransactionHistory() {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'fraud' | 'safe'>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  const fetchTransactions = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/recent?limit=50')
      if (response.ok) {
        const data = await response.json()
        setTransactions(data.data || [])
      } else {
        // Use mock data if backend not available
        setTransactions(generateMockTransactions())
      }
    } catch (error) {
      console.log('Using mock data')
      setTransactions(generateMockTransactions())
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTransactions()
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchTransactions, 30000)
    return () => clearInterval(interval)
  }, [])

  // Filter and search transactions
  const filteredTransactions = transactions.filter(tx => {
    const matchesFilter = filter === 'all' || 
      (filter === 'fraud' && tx.prediction) || 
      (filter === 'safe' && !tx.prediction)
    
    const matchesSearch = searchQuery === '' || 
      tx.transaction_id?.toLowerCase().includes(searchQuery.toLowerCase())
    
    return matchesFilter && matchesSearch
  })

  // Pagination
  const totalPages = Math.ceil(filteredTransactions.length / itemsPerPage)
  const paginatedTransactions = filteredTransactions.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )

  const getStatusBadge = (isFraud: boolean, _confidence: number) => {
    if (isFraud) {
      return (
        <Badge 
          variant="destructive" 
          className="flex items-center gap-1 bg-red-500 hover:bg-red-600"
        >
          <AlertTriangle className="w-3 h-3" />
          Fraud
        </Badge>
      )
    }
    return (
      <Badge 
        variant="default" 
        className="flex items-center gap-1 bg-emerald-500 hover:bg-emerald-600"
      >
        <CheckCircle2 className="w-3 h-3" />
        Safe
      </Badge>
    )
  }

  const getConfidenceColor = (confidence: number, isFraud: boolean) => {
    if (isFraud) {
      if (confidence > 0.8) return 'text-red-600 dark:text-red-400'
      if (confidence > 0.5) return 'text-orange-600 dark:text-orange-400'
      return 'text-yellow-600 dark:text-yellow-400'
    }
    return 'text-emerald-600 dark:text-emerald-400'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="border-slate-200 dark:border-slate-700">
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg">
                <History className="w-5 h-5 text-slate-600 dark:text-slate-400" />
              </div>
              <CardTitle className="text-lg">Transaction History</CardTitle>
            </div>
            
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={fetchTransactions}
                disabled={loading}
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-3 mt-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                placeholder="Search by transaction ID..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={filter} onValueChange={(v: any) => setFilter(v)}>
              <SelectTrigger className="w-[140px]">
                <Filter className="w-4 h-4 mr-2" />
                <SelectValue placeholder="Filter" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="fraud">Fraud Only</SelectItem>
                <SelectItem value="safe">Safe Only</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>

        <CardContent>
          {loading && transactions.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                className="w-10 h-10 border-4 border-slate-200 border-t-blue-600 rounded-full mb-4"
              />
              <p className="text-slate-500">Loading transactions...</p>
            </div>
          ) : paginatedTransactions.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="w-16 h-16 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center mb-4">
                <Shield className="w-8 h-8 text-slate-400" />
              </div>
              <h3 className="text-lg font-medium text-slate-700 dark:text-slate-300 mb-2">
                No Transactions Found
              </h3>
              <p className="text-sm text-slate-500 max-w-xs">
                {searchQuery || filter !== 'all' 
                  ? 'Try adjusting your filters' 
                  : 'Make a prediction to see it here'}
              </p>
            </div>
          ) : (
            <>
              <div className="rounded-lg border border-slate-200 dark:border-slate-700 overflow-hidden">
                <Table>
                  <TableHeader>
                    <TableRow className="bg-slate-50 dark:bg-slate-800/50">
                      <TableHead>Transaction ID</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Confidence</TableHead>
                      <TableHead>Amount</TableHead>
                      <TableHead>Time</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <AnimatePresence>
                      {paginatedTransactions.map((tx, index) => (
                        <motion.tr
                          key={tx._id || index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: 20 }}
                          transition={{ delay: index * 0.05 }}
                          className="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
                        >
                          <TableCell>
                            <code className="text-xs bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">
                              {tx.transaction_id?.slice(0, 20)}...
                            </code>
                          </TableCell>
                          <TableCell>
                            {getStatusBadge(tx.prediction, tx.confidence)}
                          </TableCell>
                          <TableCell>
                            <span className={`font-medium ${getConfidenceColor(tx.confidence, tx.prediction)}`}>
                              {(tx.confidence * 100).toFixed(1)}%
                            </span>
                          </TableCell>
                          <TableCell>
                            ${tx.input_features?.amount?.toFixed(2) || 'N/A'}
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1.5 text-sm text-slate-500">
                              <Clock className="w-3.5 h-3.5" />
                              {tx.timestamp 
                                ? new Date(tx.timestamp).toLocaleString() 
                                : 'N/A'}
                            </div>
                          </TableCell>
                        </motion.tr>
                      ))}
                    </AnimatePresence>
                  </TableBody>
                </Table>
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between mt-4">
                  <p className="text-sm text-slate-500">
                    Showing {(currentPage - 1) * itemsPerPage + 1} to{' '}
                    {Math.min(currentPage * itemsPerPage, filteredTransactions.length)} of{' '}
                    {filteredTransactions.length} transactions
                  </p>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                      disabled={currentPage === 1}
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </Button>
                    <span className="text-sm text-slate-600 dark:text-slate-400">
                      Page {currentPage} of {totalPages}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                      disabled={currentPage === totalPages}
                    >
                      <ChevronRight className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )
}

// Generate mock transactions for demo
function generateMockTransactions(): Transaction[] {
  return Array.from({ length: 25 }, (_, i) => ({
    _id: `mock_${i}`,
    transaction_id: `txn_${Math.random().toString(36).substring(2, 18)}`,
    prediction: Math.random() > 0.85,
    confidence: Math.random(),
    timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString(),
    input_features: {
      amount: Math.random() * 1000,
      time: Math.random() * 172792
    }
  }))
}
