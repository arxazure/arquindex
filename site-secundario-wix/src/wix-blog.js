import { createClient, OAuthStrategy } from "@wix/sdk";
import { posts } from "@wix/blog";

const client = createClient({
  modules: { posts },
  auth: OAuthStrategy({
    clientId: "998a0ad6-f7b6-43e1-8879-ba46ebfef4b4"
  })
});

export async function listPublicWixPosts() {
  const result = await client.posts.listPosts({ paging: { limit: 12 } });
  return (result.posts || []).map(post => ({
    title: post.title || "Artigo",
    excerpt: post.excerpt || "",
    slug: post.slug || "",
    published: post.firstPublishedDate || null
  }));
}

function safeText(text) {
  return String(text || "").replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    '"': "&quot;", "'": "&#39;"
  }[char]));
}

export async function renderPublicWixPosts() {
  const host = document.querySelector("#wix-posts");
  if (!host) return;
  try {
    const posts = await listPublicWixPosts();
    host.replaceChildren();
    if (!posts.length) {
      host.textContent = "Novos artigos em preparação.";
      return;
    }
    for (const item of posts) {
      const card = document.createElement("article");
      card.className = "card";
      const title = document.createElement("h3");
      title.textContent = safeText(item.title).replace(/&amp;/g, "&");
      const excerpt = document.createElement("p");
      excerpt.textContent = item.excerpt;
      card.append(title, excerpt);
      host.append(card);
    }
  } catch (err) {
    console.error("Wix Blog unavailable", err);
    host.textContent = "A biblioteca está temporariamente indisponível.";
  }
}
renderPublicWixPosts();
