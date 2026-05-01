let offlineDB: Record<string, Record<string, string>> = {};

export async function loadOfflineDB() {
  if (Object.keys(offlineDB).length) return;

  try {
    const res = await fetch("/offline_qa.json");
    offlineDB = await res.json();
  } catch (err) {
    console.error("Failed to load offline DB:", err);
  }
}

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
