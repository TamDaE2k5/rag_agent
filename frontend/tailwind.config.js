/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        grid: {
          blue: "#2563EB",
          dark: "#0F172A",
          card: "#1E293B",
          accent: "#10B981",
          amber: "#F59E0B"
        }
      }
    },
  },
  plugins: [],
}
