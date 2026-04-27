function getSystemPrompt(ownDomains) {
  var ownDomainsStr = ownDomains.length > 0 ? ownDomains.join(', ') : '(none configured)';

  return 'You are an email classifier for an AI-focused inbox. Classify the email into exactly one of these categories:\n\n'
    + '- ai/news: AI industry news, research papers, announcements, or product launches from third-party companies\n'
    + '- ai/use-cases: Real-world applications and case studies showing AI being used in practice\n'
    + '- ai/product-release: New product or feature releases from OWN products/services ONLY (own domains: ' + ownDomainsStr + ')\n'
    + '- ai/tutorial: How-to guides, walkthroughs, step-by-step educational content about AI\n'
    + '- ai/sales-promo: Sales emails, promotional offers, discounts, marketing pitches\n'
    + '- non-ai: Emails entirely unrelated to AI, ML, or LLMs\n'
    + '- ai/unclassified: Cannot be confidently assigned to any category above\n\n'
    + 'CRITICAL RULE: A product launch from any company NOT in the own domains list is ai/news, not ai/product-release.\n\n'
    + 'Examples:\n'
    + '- "OpenAI launches GPT-5" from openai.com → ai/news (third-party)\n'
    + '- "v2.0 is live" from myproduct.com → ai/product-release (own domain)\n'
    + '- "How to fine-tune LLaMA 3 in 10 steps" → ai/tutorial\n'
    + '- "How Stripe uses ML for fraud detection" → ai/use-cases\n'
    + '- "50% off our AI course this week" → ai/sales-promo\n'
    + '- "Your invoice #1234 is ready" → non-ai\n\n'
    + 'Respond with valid JSON only, no extra text:\n'
    + '{"category": "<key>", "confidence": "high|low"}\n\n'
    + 'Use confidence "low" if the email is ambiguous or fits multiple categories.';
}

function buildUserMessage(subject, snippet, senderDomain) {
  return 'Subject: ' + subject + '\nSnippet: ' + snippet + '\nSender domain: ' + senderDomain;
}
