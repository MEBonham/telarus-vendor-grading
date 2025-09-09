<script>
    import { Accordion } from "bits-ui";
    import { weightedGradeOutOf100, WEIGHTS } from "$lib/utils";

    let vendorData = $state([]);
    $effect(() => {
        vendorData = JSON.parse(window.localStorage.getItem('vendorData'));
    });

    let vendorScores = $derived.by(() => {
        if (vendorData.length === 0) return {};
        return vendorData.slice(1).reduce((acc, row) => {
            acc[row[0]] = weightedGradeOutOf100([ ...row ]);
            return acc;
        }, {});
    });

    let sortedVendors = $derived(
        [ ...Object.keys(vendorScores) ].sort((a, b) => vendorScores[b] - vendorScores[a])
    );

    let vendorViewed = $state("");
    let explanation = $state("");
    let isLoadingExplanation = $state(false);

    $effect(async () => {
        if (!vendorViewed) return;

        explanation = "";
        isLoadingExplanation = true;

        const key = `telarus-explanations-${vendorViewed}`;
        const stored = localStorage.getItem(key);

        if (stored) {
            explanation = stored;
            isLoadingExplanation = false;
            return;
        }

        const vendorRow = vendorData.find((row) => row[0] === vendorViewed);
        if (!vendorRow) {
            explanation = "No data available for this vendor.";
            isLoadingExplanation = false;
            return;
        }

        try {
            const response = await fetch("/api/ai_proxy", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    vendor: vendorViewed,
                    ratings: vendorRow.slice(1),
                    weights: WEIGHTS,
                    finalScore: vendorScores[vendorViewed]
                }),
            });

            if (!response.ok) throw new Error(`Request failed: ${response.status}`);

            const result = await response.text(); // or `.json()` depending on API
            localStorage.setItem(key, result);
            explanation = result;
        } catch (e) {
            explanation = "Failed to fetch explanation.";
        } finally {
            isLoadingExplanation = false;
        }
    });
</script>

<header>
    <h2>Grades</h2>
</header>
{#if vendorData.length > 0}
    <Accordion.Root bind:value={vendorViewed} type="single">
        {#each sortedVendors as vendor}
            <Accordion.Item value={vendor}>
                <Accordion.Header>
                    <Accordion.Trigger>
                        <h2>
                            {vendor}
                            {vendorScores[vendor]}
                        </h2>
                    </Accordion.Trigger>
                </Accordion.Header>
                <Accordion.Content>
                    <h3>Explanation</h3>
                    {#if explanation}
                        <p>{explanation}</p>
                    {:else}
                        <p>
                            <em>Loading explanation...</em>
                        </p>
                    {/if}
                    <h3>Full Star Scores</h3>
                    <article>
                        {#each [1,2,3,4,5,6,7,8,9,10] as i}
                            <span>
                                <strong>{vendorData[0][i]}</strong>
                                {vendorData.filter((row) => row[0] === vendor)[0][i]}
                            </span>
                        {/each}
                    </article>
                </Accordion.Content>
            </Accordion.Item>
        {/each}
    </Accordion.Root>
{:else}
    <main><em>Please upload vendor data.</em></main>
{/if}
<section>
    <h2>How are these scores calculated?</h2>
    <p>The final score for each telecom vendor is calculated by combining their ratings across all 10 evaluation factors, with each factor contributing a different amount of weight to the total. First, every factor (like Price, Reliability, Security, etc.) is scored on a scale from 1 to 5, where 1 means very poor and 5 means excellent. Each score is then converted into a percentage by dividing it by 5 (so a 5 equals 100%, a 3 equals 60%, etc.) and multiplied by the weight assigned to that factor (for example, Price might count for 15% of the total). Once all these weighted contributions are calculated, they are added together to get a single final score out of 100. This way, the most important factors influence the overall score more heavily, while less critical factors still play a role but have less impact.</p>
    <p>Here's how the weights are distributed across the 10 factors in the scoring model: Price (15%), Cost Transparency & Contract Flexibility (8%), Reliability & Uptime (15%), Service Performance (12%), Innovation & Technology Adoption (8%), Security & Privacy (12%), Regulatory Compliance (8%), Reputation & Customer Reviews (7%), Customer Support Quality (8%), and Environmental & Social Impact (5%). Together, these add up to 100%, ensuring that each vendor’s final score fairly balances financial value, service quality, trust, and long-term responsibility.</p>
</section>

<style>
    article {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        margin-bottom: 3rem;

        & > span {
            width: 25%;
            padding: 0.5rem 0;
        }
    }
</style>
