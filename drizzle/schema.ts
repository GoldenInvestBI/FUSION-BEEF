import { int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

// Products table for Minerva inventory
export const products = mysqlTable("products", {
  id: int("id").autoincrement().primaryKey(),
  sku: varchar("sku", { length: 50 }).notNull().unique(),
  name: varchar("name", { length: 500 }).notNull(),
  category: varchar("category", { length: 100 }).notNull(),
  priceOriginal: varchar("priceOriginal", { length: 20 }).notNull(),
  priceWithMarkup: varchar("priceWithMarkup", { length: 20 }).notNull(),
  markup: varchar("markup", { length: 10 }).notNull().default("60.00"),
  imageUrl: text("imageUrl"),
  imageLocalPath: text("imageLocalPath"),
  description: text("description"),
  inStock: int("inStock").notNull().default(1),
  stockStatus: varchar("stockStatus", { length: 50 }),
  weight: varchar("weight", { length: 50 }),
  origin: varchar("origin", { length: 100 }),
  brand: varchar("brand", { length: 100 }),
  minervaUrl: text("minervaUrl"),
  lastScrapedAt: timestamp("lastScrapedAt"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Product = typeof products.$inferSelect;
export type InsertProduct = typeof products.$inferInsert;

// Scrape logs table for tracking automation
export const scrapeLogs = mysqlTable("scrape_logs", {
  id: int("id").autoincrement().primaryKey(),
  status: varchar("status", { length: 50 }).notNull(),
  productsFound: int("productsFound").default(0),
  productsAdded: int("productsAdded").default(0),
  productsUpdated: int("productsUpdated").default(0),
  productsRemoved: int("productsRemoved").default(0),
  errorMessage: text("errorMessage"),
  details: text("details"),
  startedAt: timestamp("startedAt").notNull(),
  completedAt: timestamp("completedAt"),
  duration: int("duration"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type ScrapeLog = typeof scrapeLogs.$inferSelect;
export type InsertScrapeLog = typeof scrapeLogs.$inferInsert;

// Settings table for global configuration
export const settings = mysqlTable("settings", {
  id: int("id").autoincrement().primaryKey(),
  key: varchar("key", { length: 100 }).notNull().unique(),
  value: text("value").notNull(),
  description: text("description"),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Setting = typeof settings.$inferSelect;
export type InsertSetting = typeof settings.$inferInsert;