# Queuing System in JS

## Overview
This project demonstrates a seat reservation system using Node.js, Redis, and Kue for job queuing. The system enables users to reserve seats and tracks the available seats dynamically with the help of Redis. It integrates an Express server, Redis for data persistence, and Kue for handling seat reservation jobs.

## Technologies Used
- **Node.js**: Backend server.
- **Express**: Web framework for Node.js.
- **Redis**: In-memory database used for storing available seats.
- **Kue**: Job queue system for processing seat reservations.
- **Promisify**: Used for converting Redis methods to promise-based functions for better async/await handling.

## Features Implemented
### 1. **Seat Reservation System**
   - The system allows users to check and reserve available seats.
   - Initially, there are 50 seats available.
   - Users can check the number of available seats and reserve them.

### 2. **Redis Integration**
   - Redis is used to store and retrieve the current number of available seats.
   - The `reserveSeat` function sets the number of available seats in Redis, and `getCurrentAvailableSeats` retrieves this value.
   - The reservation system is updated dynamically by adjusting the available seats in Redis.

### 3. **Queue Management**
   - **Kue** is used to manage the reservation requests as jobs.
   - Jobs are added to the queue when a seat reservation request is made, and the jobs are processed to decrement the available seats.

### 4. **Express Server**
   - An Express server listens on port `1245`.
   - The following routes are provided:
     - **GET /available_seats**: Returns the current number of available seats.
     - **GET /reserve_seat**: Initiates a seat reservation job.
     - **GET /process**: Processes the queue and reserves a seat if available.

### 5. **Reservation Logic**
   - If no seats are available, the reservation system blocks further reservations.
   - The system dynamically updates the reservation availability in real-time.

## API Endpoints
### 1. **GET /available_seats**
   - Returns the current number of available seats in the system.

   **Example:**
   ```json
   {"numberOfAvailableSeats":"50"}
```

## License
This project is licensed under the MIT License - see the LICENSE file for details
```

### Key Features Highlighted:
- Redis for seat availability tracking.
- Kue queue for seat reservation jobs.
- Express server with API endpoints for seat availability and reservation.
- Error handling for reservation blocking when seats are unavailable.
