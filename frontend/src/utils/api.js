import axios from 'axios'
const api = axios.create({ baseURL: '/api' })
export const analyzeTranscript = (p) => api.post('/signals/analyze', p)
export const fetchTicker = (ticker, quarter, year) => api.get('/signals/fetch/' + ticker, { params: { quarter, year } })
export const listSignals = () => api.get('/signals/')
export const deleteSignal = (id) => api.delete('/signals/' + id)
export const runBacktest = () => api.get('/signals/backtest/run')
export const getBacktestResults = () => api.get('/signals/backtest/results')
export default api
