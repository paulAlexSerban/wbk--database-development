import { faker } from '@faker-js/faker'

export const generateUsers = (count) => {
  return Array.from({ length: count }, () => ({
    username: faker.internet.username(),
    password: faker.internet.password(),
  }));
};

export const users = generateUsers(100);

export const usersTableSchema = `
    CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username TEXT NOT NULL,
      password TEXT NOT NULL
    )
  `;

export const setupUsersTable = async (pool) => {
  try {
    await pool.query("DROP TABLE IF EXISTS users");
    await pool.query(usersTableSchema);
  } catch (err) {
    console.error("Error creating users table:", err);
    throw err;
  }
};

export const insertUsers = async (pool, users) => {
  try {
    for (const user of users) {
      await pool.query(
        "INSERT INTO users (username, password) VALUES ($1, $2)",
        [user.username, user.password],
      );
    }
  } catch (err) {
    console.error("Error inserting users:", err);
    throw err;
  }
};

export const countUsers = async (pool) => {
  try {
    const { rows } = await pool.query(
      "SELECT COUNT(*)::int AS count FROM users",
    );
    return rows[0].count;
  } catch (err) {
    console.error("Error counting users:", err);
    throw err;
  }
};
