import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "읽어드림",
  description: "사진 찍으면 글자를 크게 보여드립니다",
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
