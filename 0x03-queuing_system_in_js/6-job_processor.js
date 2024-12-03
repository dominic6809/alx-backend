#!/usr/bin/env node

const kue = require('kue');
const queue = kue.createQueue();

// Function to send notifications
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Queue process to handle new jobs in the 'push_notification_code' queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;
  
  // Call sendNotification with the job data
  sendNotification(phoneNumber, message);

  // done job
  done();
});
