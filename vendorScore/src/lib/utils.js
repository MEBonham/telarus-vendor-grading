const WEIGHTS = {
    price: 0.15,
    costTransparency: 0.08,
    reliability: 0.15,
    servicePerformance: 0.12,
    innovation: 0.08,
    security: 0.12,
    compliance: 0.08,
    reputation: 0.07,
    customerSupport: 0.08,
    environmentalImpact: 0.05,
};

const MAX_STARS_RATING = 5;

export const weightedGradeOutOf100 = (row) => {
    let processedRow = [];
    processedRow.push({ name: "price", value: row[1] });
    processedRow.push({ name: "costTransparency", value: row[2] });
    processedRow.push({ name: "reliability", value: row[3] });
    processedRow.push({ name: "servicePerformance", value: row[4] });
    processedRow.push({ name: "innovation", value: row[5] });
    processedRow.push({ name: "security", value: row[6] });
    processedRow.push({ name: "compliance", value: row[7] });
    processedRow.push({ name: "reputation", value: row[8] });
    processedRow.push({ name: "customerSupport", value: row[9] });
    processedRow.push({ name: "environmentalImpact", value: row[10] });

    return Math.round(
        processedRow.reduce((acc, cur, i) => {
            if (i === 0) return acc;
            return acc + (WEIGHTS[cur.name] * cur.value / MAX_STARS_RATING);
        }, 0) * 100
    );
}
