import { createPool } from "./db.js";
import {
  setupUsersTable,
  insertUsers,
  countUsers,
  usersTableSchema,
  users,
} from "./seeds/users.js";
import {
  setupCustomersTable,
  insertCustomers,
  countCustomers,
  customersTableSchema,
  customers,
  setupOrdersTable,
  insertOrders,
  countOrders,
  ordersTableSchema,
  orders,
  setupOrderItemsTable,
  insertOrderItems,
  countOrderItems,
  orderItemsTableSchema,
  orderItems,
  createIndexes,
  joinAcrossAllTables,
} from "./seeds/customerOrders.js";

async function seedUsers() {
  const pool = createPool();

  await setupUsersTable(pool);
  await insertUsers(pool, users);
  const count = await countUsers(pool);
  console.log(`Seeded ${count} users`);
}

async function seedCustomers() {
  const pool = createPool();
  await setupCustomersTable(pool);
  await insertCustomers(pool, customers);
  const count = await countCustomers(pool);
  console.log(`Seeded ${count} customers`);
}

async function seedOrders() {
  const pool = createPool();
  await setupOrdersTable(pool);
  await insertOrders(pool, orders);
  const count = await countOrders(pool);
  console.log(`Seeded ${count} orders`);
}

async function seedOrderItems() {
  const pool = createPool();
  await setupOrderItemsTable(pool);
  await insertOrderItems(pool, orderItems);
  const count = await countOrderItems(pool);
  console.log(`Seeded ${count} order items`);
  await createIndexes(pool);
  const rows = await joinAcrossAllTables(pool);
  console.log(rows);
}

async function seed() {
  await seedUsers();
  await seedCustomers();
  await seedOrders();
  await seedOrderItems();

}

seed().catch((err) => {
  console.error(err);
  process.exit(1);
});
