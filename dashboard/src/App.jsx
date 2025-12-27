import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import Pipelines from './pages/Pipelines'
import Vulnerabilities from './pages/Vulnerabilities'
import Fixes from './pages/Fixes'
import Reports from './pages/Reports'
import LogParser from './pages/LogParser'
import Logs from './pages/Logs'
import Login from './pages/Login'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<Layout />}>
                    <Route index element={<Dashboard />} />
                    <Route path="pipelines" element={<Pipelines />} />
                    <Route path="vulnerabilities" element={<Vulnerabilities />} />
                    <Route path="fixes" element={<Fixes />} />
                    <Route path="reports" element={<Reports />} />
                    <Route path="log-parser" element={<LogParser />} />
                    <Route path="logs" element={<Logs />} />
                </Route>
            </Routes>
        </Router>
    )
}

export default App
