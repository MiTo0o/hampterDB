import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter({
            fallback: '404.html'
        }),
        paths: {
            // When using a Custom Domain, the base is almost always empty
            base: '' 
        }
    }
};

export default config;