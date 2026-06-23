// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";

// Update `site` to your final Cloudflare URL (workers.dev subdomain or custom
// domain). Used for canonical URLs and the sitemap.
const SITE = process.env.SITE_URL || "https://pqcfieldguide.com";

// https://astro.build
export default defineConfig({
  site: SITE,
  output: "static",
  markdown: {
    // GitHub-flavored markdown (tables, autolinked URLs) is on by default.
    rehypePlugins: [
      rehypeSlug,
      [
        rehypeAutolinkHeadings,
        {
          behavior: "append",
          properties: { className: ["heading-anchor"], ariaLabel: "Copy link to section" },
          content: { type: "text", value: "#" },
        },
      ],
    ],
  },
  integrations: [
    sitemap({ filter: (page) => !page.includes("/book-print") }),
  ],
});
