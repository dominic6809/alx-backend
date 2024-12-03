#!/usr/bin/env node

const kue = require('kue');
const queue = kue.createQueue();
const _ = require('lodash');

// Blacklisted phone numbers
const blacklistedNumbers = [
  '4153518780',
  '4153518781'
];

// Function to send notifications
function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100); // Track the progress from 0 to 100
  // Check if the phone number is blacklisted
  if (_.includes(blacklistedNumbers, phoneNumber)) {
    job.failed().save(); // Mark job as failed and save
    console.log(`Notification job #${job.id} failed: Phone number ${phoneNumber} is blacklisted`);
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`)); // done
  }

  // Track job progress to 50%
  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  
  // Simulate notification being sent
  setTimeout(() => {
    job.progress(100, 100); // Job is completed
    job.remove(); // Remove the job
    console.log(`Notification job #${job.id} completed`);
    done(); // done
  }, 1000);
}

// Process the jobs in the queue
queue.process('push_notification_code_2', 2, function(job, done) {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
