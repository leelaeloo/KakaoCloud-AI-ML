import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontSize: {
        "2xl": "1.75rem",
        "3xl": "2rem",
        "4xl": "2.5rem",
        "5xl": "3rem",
      },
      colors: {
        // 커스텀 primary 색상 팔레트
        primary: {
          50: "#f0fdf4",
          100: "#dcfce7",
          200: "#bbf7d0",
          300: "#86efac",
          400: "#4ade80",
          500: "#22c55e",
          600: "#16a34a",
          700: "#15803d",
          800: "#166534",
          900: "#14532d",
        },
        // CSS 변수를 Tailwind 클래스로 사용
        theme: {
          "bg-card": "var(--color-bg-card)",
          "bg-light": "var(--color-bg-light)",
          "bg-lighter": "var(--color-bg-lighter)",
          border: "var(--color-border)",
          "text-primary": "var(--color-text-primary)",
          "text-secondary": "var(--color-text-secondary)",
          "text-dark": "var(--color-text-dark)",
          button: "var(--color-button)",
          "button-hover": "var(--color-button-hover)",
        },
      },
    },
  },
  plugins: [],
};
export default config;
