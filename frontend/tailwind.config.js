/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#041b2d",
        panel: "#0c2638",
        accent: "#2dd4bf",
        signal: "#67e8f9"
      },
      boxShadow: {
        glow: "0 20px 60px rgba(45, 212, 191, 0.18)"
      }
    }
  },
  plugins: []
};
