<script>
    import { goto } from "$app/navigation";

	let vendorData = $state([]);
	let csvFile;

    $effect(() => {
        window.localStorage.setItem('vendorData', JSON.stringify(vendorData));
        if (vendorData.length > 0) {
            goto("/");
        }
    });

	function handleSubmit(event) {
		event.preventDefault();

		if (!csvFile) return;

		const reader = new FileReader();
		reader.onload = (e) => {
			const text = e.target.result;
			const rows = text.trim().split('\n').map(row => row.split(','));
			vendorData = rows;
		};

		reader.readAsText(csvFile);
	}
</script>

<header>
    <h2>Upload Vendors (CSV Format)</h2>
</header>
<form onsubmit={handleSubmit}>
	<input
		type="file"
		accept=".csv"
		onchange={(e) => csvFile = e.target.files[0]}
	/>
	<button type="submit">Upload</button>
</form>
