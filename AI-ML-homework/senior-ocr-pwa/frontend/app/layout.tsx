import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "읽어드림",
  description: "사진 찍으면 글자를 크게 보여드립니다",
  manifest: "/manifest.json",
  themeColor: "#fbbf24",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "읽어드림",
  },
  icons: {
    icon: [
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
    ],
    apple: "/apple-touch-icon.png",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
