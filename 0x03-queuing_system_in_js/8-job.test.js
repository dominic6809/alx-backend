#!/usr/bin/env node
const kue = require('kue');
const chai = require('chai');
const expect = chai.expect;
const createPushNotificationsJobs = require('./8-job.js');

describe('createPushNotificationsJobs', () => {
  let queue;
  let logs;

  // Before each test, create a new queue and enable test mode
  beforeEach(() => {
    queue = kue.createQueue();
    logs = [];
    // Mock console.log to capture log messages
    console.log = (msg) => logs.push(msg);
  });

  // After each test, clear the queue and reset the mock
  afterEach(() => {
    queue = null;  // Reset queue
    logs = []; // Clear logs
    console.log = () => {}; // Reset the console.log mock
  });

  it('should throw an error if jobs is not an array', () => {
    // Try calling createPushNotificationsJobs with non-array argument
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('should create two new jobs in the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 5678 to verify your account' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Verify that the jobs are correctly added to the queue
    expect(queue.length()).to.equal(2); // Ensure the queue has 2 jobs

    // Check if the logs contain the job creation messages
    expect(logs).to.include('Notification job created: 1');
    expect(logs).to.include('Notification job created: 2');
  });

  it('should log "Notification job created" for each job created', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 5678 to verify your account' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Check if the log output contains the correct messages
    expect(logs).to.include('Notification job created: 1');
    expect(logs).to.include('Notification job created: 2');
  });

  it('should log the correct job progress', (done) => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Retrieve the job that was created
    const job = queue.testMode.jobs[0];

    // Simulate job progress
    job.progress(0, 100); // Simulate progress 0%
    job.progress(50, 100); // Simulate progress 50%

    setTimeout(() => {
      // Check for the correct progress log message
      expect(logs).to.include('Notification job 1 0% complete');
      expect(logs).to.include('Notification job 1 50% complete');
      done();
    }, 50);
  });

  it('should log job completion', (done) => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Retrieve the job that was created
    const job = queue.testMode.jobs[0];

    // Simulate job completion
    job.complete(); // Simulate completion

    setTimeout(() => {
      // Check for the correct completion log message
      expect(logs).to.include('Notification job 1 completed');
      done();
    }, 100);
  });

  it('should log job failure', (done) => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Retrieve the job that was created
    const job = queue.testMode.jobs[0];

    // Simulate job failure
    job.failed(new Error('Phone number 4153518780 is blacklisted')); // Simulate failure

    setTimeout(() => {
      // Check for the correct failure log message
      expect(logs).to.include('Notification job 1 failed: Error: Phone number 4153518780 is blacklisted');
      done();
    }, 100);
  });
});
