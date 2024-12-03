#!/usr/bin/env node

const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

// Create an array of products
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

// Create an Express app
const app = express();
const port = 1245;

// Create a Redis client and promisify it
const client = redis.createClient();
client.get = promisify(client.get);
client.set = promisify(client.set);

// Function to get item by ID
const getItemById = (id) => {
  return listProducts.find(product => product.itemId === id);
};

// Route to return all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Function to reserve stock
const reserveStockById = async (itemId, stock) => {
  await client.set(`item.${itemId}`, stock);
};

// Function to get current reserved stock
const getCurrentReservedStockById = async (itemId) => {
  const stock = await client.get(`item.${itemId}`);
  return stock ? parseInt(stock) : 0;
};

// Route to return product details with current available stock
app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(Number(itemId));
  
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.initialAvailableQuantity - reservedStock;
  
  res.json({
    ...product,
    currentQuantity
  });
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(Number(itemId));

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.initialAvailableQuantity - reservedStock;

  if (currentQuantity <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  await reserveStockById(itemId, reservedStock + 1);

  res.json({ status: 'Reservation confirmed', itemId });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
