/**
 * Simple localStorage-based caching for AI responses to ensure
 * consistency and reduce API calls for identical queries.
 */

export function saveToCache(query: string, response: string) {
  if (typeof window === 'undefined') return;
  const cache = JSON.parse(localStorage.getItem("qa_cache") || "{}");
  cache[query.toLowerCase()] = response;
  localStorage.setItem("qa_cache", JSON.stringify(cache));
}

/**
 * Retrieves a cached AI response for a given query string.
 * @param query The user's query
 * @returns The cached response string or null
 */
export function getFromCache(query: string) {
  if (typeof window === 'undefined') return null;
  const cache = JSON.parse(localStorage.getItem("qa_cache") || "{}");
  return cache[query.toLowerCase()] || null;
}
