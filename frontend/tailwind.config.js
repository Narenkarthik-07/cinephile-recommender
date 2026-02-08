/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                cinema: {
                    900: '#0a0a0a', // Deep black background
                    800: '#1a1a1a', // Card background
                    500: '#e50914', // Netflix Red accent
                }
            }
        },
    },
    plugins: [],
}