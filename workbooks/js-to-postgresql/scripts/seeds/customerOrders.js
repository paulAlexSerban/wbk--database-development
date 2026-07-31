import { faker } from "@faker-js/faker";

export const customersTableSchema = `
  CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
  )
`;

export const generateCustomers = (count) => {
  return Array.from({ length: count }, () => ({
    email: faker.internet.email(),
  }));
};

export const customers = generateCustomers(100);

export const setupCustomersTable = async (pool) => {
  try {
    await pool.query("DROP TABLE IF EXISTS customers CASCADE");
    await pool.query(customersTableSchema);
  } catch (err) {
    console.error("Error creating customers table:", err);
    throw err;
  }
};

export const insertCustomers = async (pool, customers) => {
  try {
    for (const customer of customers) {
      await pool.query("INSERT INTO customers (email) VALUES ($1)", [
        customer.email,
      ]);
    }
  } catch (err) {
    console.error("Error inserting customers:", err);
    throw err;
  }
};

export const countCustomers = async (pool) => {
  try {
    const { rows } = await pool.query(
      "SELECT COUNT(*)::int AS count FROM customers",
    );
    return rows[0].count;
  } catch (err) {
    console.error("Error counting customers:", err);
    throw err;
  }
};

export const ordersTableSchema = `
  CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
  )
`;

export const generateOrders = (count) => {
  return Array.from({ length: count }, () => ({
    customer_id: faker.number.int({ min: 1, max: 100 }),
    status: faker.helpers.arrayElement(["pending", "shipped", "delivered"]),
  }));
};

export const orders = generateOrders(100);

export const setupOrdersTable = async (pool) => {
  try {
    await pool.query("DROP TABLE IF EXISTS orders CASCADE");
    await pool.query(ordersTableSchema);
  } catch (err) {
    console.error("Error creating orders table:", err);
    throw err;
  }
};

export const insertOrders = async (pool, orders) => {
  try {
    for (const order of orders) {
      await pool.query(
        "INSERT INTO orders (customer_id, status) VALUES ($1, $2)",
        [order.customer_id, order.status],
      );
    }
  } catch (err) {
    console.error("Error inserting orders:", err);
    throw err;
  }
};

export const countOrders = async (pool) => {
  try {
    const { rows } = await pool.query(
      "SELECT COUNT(*)::int AS count FROM orders",
    );
    return rows[0].count;
  } catch (err) {
    console.error("Error counting orders:", err);
    throw err;
  }
};

export const orderItemsTableSchema = `
  CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_sku VARCHAR(64) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0)
  )
`;

export const generateOrderItems = (count) => {
  return Array.from({ length: count }, () => ({
    order_id: faker.number.int({ min: 1, max: 100 }),
    product_sku: faker.string.alphanumeric(64),
    quantity: faker.number.int({ min: 1, max: 100 }),
    unit_price_cents: faker.number.int({ min: 0, max: 10000 }),
  }));
};

export const orderItems = generateOrderItems(10000);

export const setupOrderItemsTable = async (pool) => {
  try {
    await pool.query("DROP TABLE IF EXISTS order_items CASCADE");
    await pool.query(orderItemsTableSchema);
  } catch (err) {
    console.error("Error creating order items table:", err);
    throw err;
  }
};

export const insertOrderItems = async (pool, orderItems) => {
  try {
    for (const orderItem of orderItems) {
      await pool.query("INSERT INTO order_items (order_id, product_sku, quantity, unit_price_cents) VALUES ($1, $2, $3, $4)", [orderItem.order_id, orderItem.product_sku, orderItem.quantity, orderItem.unit_price_cents]);
    }
  } catch (err) {
    console.error("Error inserting order items:", err);
    throw err;
  }
};

export const countOrderItems = async (pool) => {
  try {
    const { rows } = await pool.query(
      "SELECT COUNT(*)::int AS count FROM order_items",
    );
    return rows[0].count;
  } catch (err) {
    console.error("Error counting order items:", err);
    throw err;
  }
};

export const createIndexes = async (pool) => {
  try {
    await pool.query("CREATE INDEX idx_orders_customer_id ON orders (customer_id)");
    await pool.query("CREATE INDEX idx_order_items_order_id ON order_items (order_id)");
  } catch (err) {
    console.error("Error creating indexes:", err);
    throw err;
  }
};

export const joinAcrossAllTables = async (pool) => {
  const query = `
    SELECT
      o.id AS order_id,
      c.email,
      o.status,
      SUM(oi.quantity * oi.unit_price_cents) AS total_cents
    FROM orders o
    JOIN customers c ON c.id = o.customer_id
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.status = 'pending'
    GROUP BY o.id, c.email, o.status
    ORDER BY o.created_at DESC
    LIMIT 50
    `;

    try {
      const { rows } = await pool.query(query);
      return rows;
    } catch (err) {
      console.error("Error joining across all tables:", err);
      throw err;
    }
}

