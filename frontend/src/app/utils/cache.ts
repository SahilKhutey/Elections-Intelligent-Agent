export function saveToCache(query: string, response: string) {
  if (typeof window === 'undefined') return;
  const cache = JSON.parse(localStorage.getItem("qa_cache") || "{}");
  cache[query.toLowerCase()] = response;
  localStorage.setItem("qa_cache", JSON.stringify(cache));
}

export function getFromCache(query: string) {
  if (typeof window === 'undefined') return null;
  const cache = JSON.parse(localStorage.getItem("qa_cache") || "{}");
  return cache[query.toLowerCase()] || null;
}
