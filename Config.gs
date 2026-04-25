var CONFIG = {
  MODEL: 'google/gemini-flash-1.5',
  OPENROUTER_API_URL: 'https://openrouter.ai/api/v1/chat/completions',

  // Sender domains that count as your own products/services.
  // Emails from these domains can be classified as ai/product-release.
  // All other product launches → ai/news.
  OWN_DOMAINS: [
    // 'myproduct.com',
    // 'myapp.io',
  ],

  LABELS: [
    'ai/news',
    'ai/use-cases',
    'ai/product-release',
    'ai/tutorial',
    'ai/sales-promo',
    'non-ai',
    'ai/unclassified',
  ],

  CLASSIFIED_LABEL: 'classified',

  // Max emails to process per trigger run (stay under GAS 6-min limit)
  BATCH_SIZE: 50,
};
