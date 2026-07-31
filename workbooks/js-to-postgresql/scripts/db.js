import pg from 'pg';

const {
  DATABASE_HOST = 'localhost',
  DATABASE_PORT = '5432',
  DATABASE_USER,
  DATABASE_PASSWORD,
  COMPOSE_PROJECT_NAME,
} = process.env;

export function createPool() {
  return new pg.Pool({
    host: DATABASE_HOST,
    port: Number(DATABASE_PORT),
    user: DATABASE_USER,
    password: DATABASE_PASSWORD,
    database: COMPOSE_PROJECT_NAME,
  });
}
