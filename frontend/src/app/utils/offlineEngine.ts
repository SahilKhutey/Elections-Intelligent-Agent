/**
 * Lightweight fuzzy-matching engine for offline query resolution.
 * Uses a pre-loaded JSON database for instant responses without server connectivity.
 */

let offlineDB: Record<string, Record<string, string>> = {};

/**
 * Asynchronously loads the offline knowledge base into memory.
 */
export async function loadOfflineDB() {
  if (Object.keys(offlineDB).length) return;

  try {
    const res = await fetch("/offline_qa.json");
    offlineDB = await res.json();
  } catch (err) {
    console.error("Failed to load offline DB:", err);
  }
}

/**
 * Searches the offline database for a relevant answer using keyword intersection.
 * @param query User's query string
 * @param lang Preferred language (en/hi)
 * @returns Matching answer or null if no match found
 */
export function findOfflineAnswer(query: string, lang: string = "en") {
  const qWords = query.toLowerCase().split(/\W+/).filter(w => w.length > 2);

  for (const key in offlineDB) {
    const keyWords = key.toLowerCase().split(/\W+/).filter(w => w.length > 2);
    
    // Check for word intersection (if any significant word matches)
    const hasMatch = keyWords.some(word => qWords.includes(word));
    
    if (hasMatch || query.toLowerCase().includes(key.toLowerCase())) {
      return offlineDB[key][lang];
    }
  }

  return null;
}
