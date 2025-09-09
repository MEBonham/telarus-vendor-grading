<script>
    import { Accordion } from "bits-ui";
    import { weightedGradeOutOf100 } from "$lib/utils";

    let vendorData = $state([]);
    $effect(() => {
        vendorData = JSON.parse(window.localStorage.getItem('vendorData')).slice(1);
    });

    let vendorScores = $derived.by(() => {
        if (vendorData.length === 0) return {};

        return vendorData.reduce((acc, row) => {
            acc[row[0]] = weightedGradeOutOf100([ ...row ]);
            return acc;
        }, {});
    });
    let sortedVendors = $derived(
        [ ...Object.keys(vendorScores) ].sort((a, b) => vendorScores[b] - vendorScores[a])
    );
</script>

<header>
    <h2>Grades</h2>
</header>
{#if sortedVendors.length > 0}
    <Accordion.Root>
        {#each sortedVendors as vendor}
            <Accordion.Item value={vendor}>
                <Accordion.Header>
                    <Accordion.Trigger>
                        {vendor}
                        {vendorScores[vendor]}
                    </Accordion.Trigger>
                </Accordion.Header>
                <Accordion.Content>
                </Accordion.Content>
            </Accordion.Item>
        {/each}
    </Accordion.Root>
{/if}
