import React, { useEffect, useState } from 'react';
import { FiShield, FiAlertTriangle, FiCheckCircle, FiClock, FiAlertOctagon, FiActivity } from 'react-icons/fi';
import MetricCard from '../components/dashboard/MetricCard';
import TrendChart from '../components/dashboard/TrendChart';
import SecurityScore from '../components/dashboard/SecurityScore';
import AlertsTable from '../components/dashboard/AlertsTable';
import { vulnService } from '../services/vulnService';
import { dashboardService } from '../services/dashboardService';
import ServiceHealthGrid from '../components/dashboard/ServiceHealthGrid';
import RabbitMQMonitor from '../components/dashboard/RabbitMQMonitor';

const Dashboard = () => {
    const [stats, setStats] = useState({
        total: 0,
        by_severity: { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 }
    });
    // Removed health state as ServiceHealthGrid will handle service health
    // const [health, setHealth] = useState({ status: 'unknown' });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            try {
                const data = await vulnService.getStats();
                setStats(data);

                // Removed LogParser Health check as ServiceHealthGrid will handle service health
                // const healthData = await logParserService.checkHealth();
                // setHealth(healthData);
            } catch (err) {
                console.error("Dashboard Load Error:", err);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, []);

    const activeRisks = (stats.by_severity?.HIGH || 0) + (stats.by_severity?.CRITICAL || 0);
    // Simple score logic: Start at 100, deduct points for severities
    const scoreDeduction = ((stats.by_severity?.CRITICAL || 0) * 20) + ((stats.by_severity?.HIGH || 0) * 10) + ((stats.by_severity?.MEDIUM || 0) * 2);
    const securityScore = Math.max(0, 100 - scoreDeduction);

    let grade = 'A';
    if (securityScore < 90) grade = 'B';
    if (securityScore < 70) grade = 'C';
    if (securityScore < 50) grade = 'D';
    if (securityScore < 30) grade = 'F';

    return (
        <div className="flex-1 overflow-y-auto bg-background p-8 font-body">
            <div className="max-w-7xl mx-auto space-y-8">
                {/* Header Section */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-display font-bold text-gray-900 tracking-tight">Security Dashboard</h1>
                        <p className="mt-2 text-gray-500 font-medium">Real-time overview of security posture and microservice health.</p>
                    </div>
                    <button className="btn-primary">
                        Generate Report
                    </button>
                </div>

                {/* Microservice Health Grid */}
                <ServiceHealthGrid />

                {/* RabbitMQ Monitor */}
                <RabbitMQMonitor />

                {/* Metrics Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <MetricCard
                        title="Active Risks"
                        value={activeRisks.toString()}
                        icon={FiAlertOctagon}
                        color={activeRisks > 0 ? "danger-light" : "success-light"}
                        change={activeRisks > 5 ? "+2" : "0"}
                    />
                    <MetricCard
                        title="Total Vulnerabilities"
                        value={stats.total?.toString() || "0"}
                        icon={FiActivity}
                        color="primary"
                        change="Live"
                    />
                    <MetricCard
                        title="Code Coverage"
                        value="94.2%"
                        icon={FiCheckCircle}
                        color="success-light"
                        change="+0.8%"
                    />
                    <MetricCard
                        title="Avg Fix Time"
                        value="45m"
                        icon={FiClock}
                        color="secondary"
                        change="-15%"
                    />
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Charts Section */}
                    <div className="lg:col-span-8 h-[400px]">
                        <TrendChart />
                    </div>

                    {/* Score Section */}
                    <div className="lg:col-span-4 h-[400px]">
                        <SecurityScore score={securityScore} grade={grade} />
                    </div>
                </div>

                {/* Recent Alerts Section */}
                <div>
                    <AlertsTable />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
