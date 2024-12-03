#!/usr/bin/env node

import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Promisify the `client.get` method to use async/await
const getAsync = promisify(client.get).bind(client);

// Function to set a new school value
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, reply) => {
    if (err) {
      console.log(`Error: ${err.message}`);
    } else {
      console.log(`Reply: ${reply}`);
    }
  });
}

// Async function to display the value of a school
async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.log(`Error: ${err.message}`);
  }
}

// Test the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
