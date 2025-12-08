import { z } from "zod";
import { publicProcedure, router } from "../_core/trpc";
import { getDb } from "../db";
import { products, scrapeLogs, settings } from "../../drizzle/schema";
import { eq, desc, and, like, or } from "drizzle-orm";

export const productsRouter = router({
  // Get all products with optional filters
  getAll: publicProcedure
    .input(
      z.object({
        category: z.string().optional(),
        search: z.string().optional(),
        inStockOnly: z.boolean().default(true),
      })
    )
    .query(async ({ input }) => {
      const db = await getDb();
      if (!db) return [];
      
      const conditions = [];
      
      if (input.inStockOnly) {
        conditions.push(eq(products.inStock, 1));
      }
      
      if (input.category && input.category !== "todas") {
        conditions.push(eq(products.category, input.category));
      }
      
      if (input.search) {
        conditions.push(
          or(
            like(products.name, `%${input.search}%`),
            like(products.sku, `%${input.search}%`)
          )
        );
      }
      
      const result = await db
        .select()
        .from(products)
        .where(conditions.length > 0 ? and(...conditions as any) : undefined)
        .orderBy(desc(products.updatedAt));
        
      return result;
    }),

  // Get product by SKU
  getBySku: publicProcedure
    .input(z.object({ sku: z.string() }))
    .query(async ({ input }) => {
      const db = await getDb();
      if (!db) return null;
      
      const [product] = await db
        .select()
        .from(products)
        .where(eq(products.sku, input.sku))
        .limit(1);
        
      return product || null;
    }),

  // Get all unique categories
  getCategories: publicProcedure.query(async () => {
    const db = await getDb();
    if (!db) return [];
    
    const result = await db
      .selectDistinct({ category: products.category })
      .from(products)
      .where(eq(products.inStock, 1));
      
    return result.map((r: any) => r.category);
  }),

  // Get scrape logs (admin only - we'll add auth later)
  getScrapeLogs: publicProcedure
    .input(
      z.object({
        limit: z.number().default(20),
      })
    )
    .query(async ({ input }) => {
      const db = await getDb();
      if (!db) return [];
      
      const logs = await db
        .select()
        .from(scrapeLogs)
        .orderBy(desc(scrapeLogs.createdAt))
        .limit(input.limit);
        
      return logs;
    }),

  // Get settings
  getSettings: publicProcedure.query(async () => {
    const db = await getDb();
    if (!db) return {};
    
    const allSettings = await db.select().from(settings);
    
    const settingsMap: Record<string, string> = {};
    allSettings.forEach((s: any) => {
      settingsMap[s.key] = s.value;
    });
    
    return settingsMap;
  }),

  // Update markup (admin only - we'll add auth later)
  updateMarkup: publicProcedure
    .input(
      z.object({
        markup: z.number().min(0).max(200),
      })
    )
    .mutation(async ({ input }) => {
      const db = await getDb();
      if (!db) return { success: false, error: "Database not available" };
      
      // Update or insert markup setting
      const [existing] = await db
        .select()
        .from(settings)
        .where(eq(settings.key, "default_markup"))
        .limit(1);
        
      if (existing) {
        await db
          .update(settings)
          .set({
            value: input.markup.toString(),
            updatedAt: new Date(),
          })
          .where(eq(settings.key, "default_markup"));
      } else {
        await db.insert(settings).values({
          key: "default_markup",
          value: input.markup.toString(),
          description: "Default markup percentage for all products",
          updatedAt: new Date(),
        });
      }
      
      // Recalculate all product prices with new markup
      const allProducts = await db.select().from(products);
      
      for (const product of allProducts) {
        const originalPrice = parseFloat(product.priceOriginal);
        const newPrice = (originalPrice * (1 + input.markup / 100)).toFixed(2);
        
        await db
          .update(products)
          .set({
            markup: input.markup.toString(),
            priceWithMarkup: newPrice,
            updatedAt: new Date(),
          })
          .where(eq(products.id, product.id));
      }
      
      return { success: true, updatedCount: allProducts.length };
    }),
});
