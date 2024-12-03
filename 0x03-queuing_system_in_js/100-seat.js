#!/usr/bin/env node

const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

// Initialize Redis client and promisify
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Initialize Kue queue
const queue = kue.createQueue();

const app = express();
const port = 1245;

// Set initial number of available seats
const initialSeats = 50;
let reservationEnabled = true;

// Initialize available seats in Redis
const reserveSeat = async (number) => {
  try {
    await setAsync('available_seats', number);
    console.log('Initial seats set to 50');
  } catch (err) {
    console.error('Error while setting available seats:', err);
  }
};

// Get current available seats from Redis
const getCurrentAvailableSeats = async () => {
  try {
    const seats = await getAsync('available_seats');
    return parseInt(seats);
  } catch (err) {
    console.error('Error getting available seats:', err);
    return 0;
  }
};

// Route to get available seats
app.get('/available_seats', async (req, res) => {
  try {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats.toString() });
  } catch (err) {
    res.status(500).json({ status: 'Error retrieving available seats' });
  }
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  // Create a job in the queue to reserve a seat
  const job = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

// Route to process the queue and reserve a seat
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  // Process the queue to reserve a seat
  queue.process('reserve_seat', async (job, done) => {
    try {
      const availableSeats = await getCurrentAvailableSeats();

      if (availableSeats <= 0) {
        reservationEnabled = false;
        done(new Error('Not enough seats available'));
        console.log(`Seat reservation job ${job.id} failed: Not enough seats available`);
        return;
      }

      const newAvailableSeats = availableSeats - 1;
      await reserveSeat(newAvailableSeats);

      if (newAvailableSeats >= 0) {
        console.log(`Seat reservation job ${job.id} completed`);
        done();
      } else {
        done(new Error('Not enough seats available'));
        console.log(`Seat reservation job ${job.id} failed: Not enough seats available`);
      }
    } catch (err) {
      console.error('Error during seat reservation:', err);
      done(err);
    }
  });
});

// Start the server
app.listen(port, async () => {
  // Initialize available seats in Redis when the server starts
  await reserveSeat(initialSeats);
  console.log(`Server listening on port ${port}`);
});
