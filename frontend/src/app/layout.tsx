import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'VC Startup Intelligence Engine Cockpit',
  description: 'Portfolio Cash Runway Risk Intelligence & Early Warning Radar',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
