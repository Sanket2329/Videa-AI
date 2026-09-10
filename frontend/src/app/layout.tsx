import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import QueryProvider from '@/providers/QueryProvider';
import { SmoothScroller } from '@/components/layout/SmoothScroller';
import { Navbar } from '@/components/layout/Navbar';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: 'AI Video Studio',
  description: 'Turn your ideas into cinematic videos.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans min-h-screen antialiased selection:bg-violet-500/30 selection:text-white`}>
        <SmoothScroller>
          <QueryProvider>
            <Navbar />
            <main className="relative z-10 w-full flex flex-col items-center overflow-hidden">
              {children}
            </main>
          </QueryProvider>
        </SmoothScroller>
      </body>
    </html>
  );
}
