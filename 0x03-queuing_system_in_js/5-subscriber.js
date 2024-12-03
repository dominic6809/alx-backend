#!/usr/bin/env node

const redis = require('redis');

// Create a redis client
const subscriber = redis.createClient();

// On connect, log a success message
subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

// On error, log an error message
subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the channel
subscriber.subscribe('holberton school channel');

// When a message is received, log it to the console
subscriber.on('message', (channel, message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe();
    subscriber.quit();
  }
});
