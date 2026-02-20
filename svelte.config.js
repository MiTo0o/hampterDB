import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter({
            fallback: '404.html'
        }),
        paths: {
            // Set this to an empty string for custom domains
            base: '' 
        }
    }
};

export default config;