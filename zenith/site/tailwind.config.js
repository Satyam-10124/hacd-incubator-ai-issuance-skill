/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      colors: {
        bg: "#07070A",
        surface: "#0F0F14",
        border: "rgba(255,255,255,0.08)",
        accent: {
          violet: "#7C5CFF",
          cyan: "#22D3EE",
        },
        tier: {
          common: "#64748B",
          uncommon: "#22C55E",
          rare: "#22D3EE",
          legendary: "#7C5CFF",
          mythic: "#F59E0B",
        },
      },
      backgroundImage: {
        "gradient-zen": "linear-gradient(135deg, #7C5CFF 0%, #22D3EE 100%)",
        "gradient-bg": "radial-gradient(ellipse at 50% 0%, #0A0A0F 0%, #07070A 70%)",
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-out",
        "slide-up": "slideUp 0.3s ease-out",
        "count-up": "countUp 0.8s ease-out",
        "ring-fill": "ringFill 0.8s ease-out forwards",
        "shimmer": "shimmer 2s linear infinite",
      },
      keyframes: {
        fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
        slideUp: { from: { opacity: 0, transform: "translateY(12px)" }, to: { opacity: 1, transform: "translateY(0)" } },
        shimmer: {
          "0%": { backgroundPosition: "-200% center" },
          "100%": { backgroundPosition: "200% center" },
        },
      },
    },
  },
  plugins: [],
};
