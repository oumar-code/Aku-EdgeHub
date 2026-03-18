const request = require('supertest');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Edge Hub service is running!'));

describe('GET /', () => {
  it('should return service running message', async () => {
    const res = await request(app).get('/');
    expect(res.text).toBe('Edge Hub service is running!');
  });
});
