
const prisma = require('./config/db');

async function check() {
    try {
        const logs = await prisma.log.findMany({
            orderBy: { timestamp_received: 'desc' },
            take: 1
        });
        console.log("Most recent log entry:");
        console.log(JSON.stringify(logs, null, 2));
    } catch (e) {
        console.error(e);
    } finally {
        await prisma.$disconnect();
    }
}

check();
