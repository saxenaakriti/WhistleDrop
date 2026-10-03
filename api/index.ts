import app from '../src/index.js';

export default function handler(req: any, res: any) {
  if (req.url === '/api' || req.url === '/api/') {
    req.url = '/';
  } else if (req.url?.startsWith('/api/')) {
    req.url = req.url.slice(4);
  }
  return app(req, res);
}
