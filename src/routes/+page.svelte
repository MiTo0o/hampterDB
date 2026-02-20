<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { fade, scale } from 'svelte/transition';

	// Types
	type HamsterList = string[];

	// State (Svelte 5)
	let hamsters: HamsterList = $state([]);
	let selectedHamster: string | null = $state(null);

	onMount(async () => {
		try {
			const response = await fetch(`${base}/manifest.json`);
			if (!response.ok) throw new Error('Failed to load manifest');
			
			const data: HamsterList = await response.json();
			// Alphabetical sort for a predictable grid
			hamsters = data.sort((a, b) => a.localeCompare(b));
		} catch (err) {
			console.error('Error fetching hamsters:', err);
		}
	});

	// Logic
	const open = (name: string): void => { selectedHamster = name; };
	const close = (): void => { selectedHamster = null; };

	const handleKeydown = (e: KeyboardEvent): void => {
		// Close on Escape key
		if (e.key === 'Escape' && selectedHamster) {
			close();
		}
		// Also allow closing with Enter/Space if the backdrop is focused
		if ((e.key === 'Enter' || e.key === ' ') && e.target === document.querySelector('.modal-backdrop')) {
			close();
		}
	};
</script>

<svelte:window onkeydown={handleKeydown} />

<main>
	<header>
		<h1>🐹 Hampter Archive</h1>
		<p>Browsing <strong>{hamsters.length}</strong> specimens</p>
	</header>

	<div class="grid">
		{#each hamsters as name (name)}
			<button 
				type="button"
				class="icon-btn" 
				onclick={() => open(name)}
				aria-label="View {name}"
			>
				<img src="{base}/images/{name}" alt="Silly Hamster" loading="lazy" />
			</button>
		{/each}
	</div>

	{#if selectedHamster}
		<div 
			class="modal-backdrop" 
			role="button"
			tabindex="0"
			onclick={close} 
			onkeydown={handleKeydown}
			transition:fade={{ duration: 200 }}
			aria-label="Close image"
		>
			<div 
				class="modal-content" 
				onclick={(e) => e.stopPropagation()} 
				transition:scale={{ duration: 200, start: 0.95 }}
			>
				<div class="actions">
					<a 
						href="{base}/images/{selectedHamster}" 
						download={selectedHamster} 
						class="btn download"
					>
						💾 Download
					</a>
					<button type="button" class="btn close" onclick={close} aria-label="Close">✕</button>
				</div>

				<img src="{base}/images/{selectedHamster}" alt="Full size hamster" />
				
				<div class="info">
					<code>{selectedHamster}</code>
				</div>
			</div>
		</div>
	{/if}
</main>

<style>
	:global(body) { 
		background: #0f0f0f; 
		color: #e0e0e0; 
		font-family: system-ui, -apple-system, sans-serif; 
		margin: 0;
		overflow-y: scroll;
	}

	header { text-align: center; padding: 3rem 1rem; }
	h1 { margin: 0; color: #ff4b4b; font-size: 2.5rem; }
	p { color: #888; margin-top: 0.5rem; }

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
		gap: 12px;
		padding: 20px;
		max-width: 1400px;
		margin: 0 auto;
	}

	@media (min-width: 600px) {
		.grid { grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 20px; }
	}

	.icon-btn {
		background: #1e1e1e;
		border: 1px solid #333;
		border-radius: 14px;
		cursor: pointer;
		padding: 8px;
		transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.icon-btn:hover {
		transform: translateY(-5px) scale(1.05);
		border-color: #ff4b4b;
		box-shadow: 0 8px 20px rgba(255, 75, 75, 0.15);
	}

	.icon-btn img { width: 100%; height: auto; border-radius: 8px; }

	.modal-backdrop {
		position: fixed; top: 0; left: 0; width: 100%; height: 100%;
		background: rgba(0,0,0,0.9); 
		backdrop-filter: blur(10px);
		display: flex; align-items: center; justify-content: center; 
		z-index: 1000;
		padding: 20px;
		cursor: zoom-out;
		outline: none; /* Removes the focus ring on the backdrop */
	}

	.modal-content {
		background: #1a1a1a;
		padding: 10px;
		border-radius: 20px;
		max-width: 95vw;
		max-height: 90vh;
		display: flex;
		flex-direction: column;
		border: 1px solid #444;
		cursor: default;
	}

	.actions { display: flex; justify-content: space-between; padding-bottom: 10px; }

	.btn {
		background: #2a2a2a;
		border: none;
		color: white;
		padding: 8px 16px;
		border-radius: 10px;
		cursor: pointer;
		font-weight: 600;
		text-decoration: none;
		font-size: 0.85rem;
		display: flex;
		align-items: center;
	}

	.btn:hover { background: #3a3a3a; }
	.btn.close { 
		background: rgba(255, 75, 75, 0.1); 
		color: #ff4b4b; 
		width: 35px; height: 35px; justify-content: center;
	}
	.btn.close:hover { background: #ff4b4b; color: white; }

	.modal-content img { 
		max-width: 100%; 
		max-height: 70vh; 
		object-fit: contain; 
		border-radius: 10px;
	}

	.info { padding: 15px; text-align: center; }
	code { background: #000; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; color: #ff4b4b; }
</style>