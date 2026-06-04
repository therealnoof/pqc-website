import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const chapters = defineCollection({
  loader: glob({ pattern: "*.md", base: "./src/content/chapters" }),
  schema: z.object({
    title: z.string(),
    displayTitle: z.string(),
    section: z.string(),
    chapter: z.number().nullable(),
    order: z.number(),
    words: z.number(),
    readingMinutes: z.number(),
    excerpt: z.string(),
  }),
});

export const collections = { chapters };
