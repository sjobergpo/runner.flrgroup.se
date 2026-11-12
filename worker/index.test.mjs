import assert from 'node:assert/strict';
import test from 'node:test';
import worker from './index.mjs';

const destination = 'https://apps.apple.com/app/apple-store/id6816334642?pt=127207286&ct=website&mt=8';

test('GET and HEAD redirect to the existing campaign without caching or cookies', async () => {
  for (const method of ['GET', 'HEAD']) {
    const response = worker.fetch(new Request('https://clicks.example/', { method }));
    assert.equal(response.status, 302);
    assert.equal(response.headers.get('Location'), destination);
    assert.equal(response.headers.get('Cache-Control'), 'no-store');
    assert.equal(response.headers.get('Set-Cookie'), null);
    assert.equal(await response.text(), '');
  }
});

test('incoming query parameters cannot change the destination or campaign', () => {
  const response = worker.fetch(new Request('https://clicks.example/?url=https://example.com&ct=other&pt=0'));
  assert.equal(response.headers.get('Location'), destination);
});

test('other paths and methods do not redirect', () => {
  const missing = worker.fetch(new Request('https://clicks.example/favicon.ico'));
  assert.equal(missing.status, 404);
  assert.equal(missing.headers.get('Location'), null);
  const rejected = worker.fetch(new Request('https://clicks.example/', { method: 'POST' }));
  assert.equal(rejected.status, 405);
  assert.equal(rejected.headers.get('Allow'), 'GET, HEAD');
  assert.equal(rejected.headers.get('Location'), null);
});
