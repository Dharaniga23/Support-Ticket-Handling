/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    peach: '#E0A28A',
                    sage: '#CDD1B7',
                    mint: '#BDEBD5',
                    navy: '#373691',
                },
                slate: {
                    850: '#151e2e',
                }
            },
        },
    },
    plugins: [],
}
