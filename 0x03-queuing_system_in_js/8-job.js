#!/usr/bin/env node

const kue = require('kue');

// Function to create push notification jobs
function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Loop through each job and add it to the queue
  jobs.forEach(jobData => {
    const job = queue.create('push_notification_code_3', jobData)
      .save((err) => {
        if (err) {
          console.log('Notification job failed to create:', err);
        } else {
          console.log(`Notification job created: ${job.id}`);
        }
      });

    // On job progress
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });

    // On job completion
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    // On job failure
    job.on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    });
  });
}

module.exports = createPushNotificationsJobs;
