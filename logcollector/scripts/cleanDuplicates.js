const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function cleanDuplicates() {
    console.log('🔍 Searching for duplicate run_ids...');

    // Get all logs grouped by run_id
    const logs = await prisma.log.findMany({
        orderBy: { timestamp_received: 'desc' }
    });

    const seen = new Set();
    const toDelete = [];

    for (const log of logs) {
        if (seen.has(log.run_id)) {
            toDelete.push(log.id);
            console.log(`❌ Duplicate found: run_id=${log.run_id}, id=${log.id}`);
        } else {
            seen.add(log.run_id);
        }
    }

    if (toDelete.length === 0) {
        console.log('✅ No duplicates found!');
        return;
    }

    console.log(`🗑️  Deleting ${toDelete.length} duplicate(s)...`);

    await prisma.log.deleteMany({
        where: { id: { in: toDelete } }
    });

    console.log('✅ Duplicates deleted!');
    console.log('📋 Now run: npx prisma db push');
}

cleanDuplicates()
    .catch(console.error)
    .finally(() => prisma.$disconnect());
