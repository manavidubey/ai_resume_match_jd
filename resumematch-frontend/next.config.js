module.exports = {
  reactStrictMode: true,
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "/api/:path*",
      },
      {
        source: "/((?!api|_next/static|_next/image|favicon.ico).*)",
        destination: "/",
      },
    ];
  },
};
