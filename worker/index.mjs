export const APP_STORE_URL = 'https://apps.apple.com/app/apple-store/id6816334642?pt=127207286&ct=website&mt=8';

export default {
  fetch(request) {
    const headers = {
      'Cache-Control': 'no-store',
      'X-Robots-Tag': 'noindex, nofollow',
    };

    if (new URL(request.url).pathname !== '/') {
      return new Response(null, { status: 404, headers });
    }
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response(null, {
        status: 405,
        headers: { ...headers, Allow: 'GET, HEAD' },
      });
    }

    return new Response(null, {
      status: 302,
      headers: { ...headers, Location: APP_STORE_URL },
    });
  },
};
