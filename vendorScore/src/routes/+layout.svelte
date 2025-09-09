<script>
	import favicon from '$lib/assets/favicon.svg';
    import MainNav from '$lib/components/MainNav.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header>
	<h1>Telecomm Vendor Grading</h1>
</header>
<MainNav />
<main>
	{@render children?.()}
</main>


