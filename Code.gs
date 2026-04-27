// Run once manually to create all Gmail labels before setting up triggers.
function setup() {
  CONFIG.LABELS.forEach(function(name) { getOrCreateLabel(name); });
  getOrCreateLabel(CONFIG.CLASSIFIED_LABEL);
  Logger.log('Setup complete — all labels created.');
}

// Triggered every 10 minutes. Fetches unclassified inbox emails and labels them.
function classifyEmails() {
  var apiKey = PropertiesService.getScriptProperties().getProperty('OPENROUTER_API_KEY');
  if (!apiKey) {
    Logger.log('ERROR: OPENROUTER_API_KEY missing from Script Properties.');
    return;
  }

  var threads = GmailApp.search('in:inbox -label:classified', 0, CONFIG.BATCH_SIZE);
  if (threads.length === 0) return;

  var classifiedLabel = getOrCreateLabel(CONFIG.CLASSIFIED_LABEL);

  threads.forEach(function(thread) {
    try {
      var message = thread.getMessages()[0];
      var subject = message.getSubject() || '(no subject)';
      var plainBody = message.getPlainBody() || message.getBody().replace(/<[^>]+>/g, '');
      var snippet = plainBody.trim().substring(0, 200);
      var senderDomain = extractDomain(message.getFrom());

      var category = classify(apiKey, subject, snippet, senderDomain);

      thread.addLabel(getOrCreateLabel(category));
      thread.addLabel(classifiedLabel);
      incrementCounter(category);

      Logger.log('Classified: "' + subject + '" → ' + category);
    } catch (e) {
      Logger.log('Error processing thread: ' + e.message);
    }
  });
}

function classify(apiKey, subject, snippet, senderDomain) {
  try {
    var raw = callOpenRouter(apiKey, subject, snippet, senderDomain);
    var parsed = JSON.parse(raw);

    if (!parsed.category || CONFIG.LABELS.indexOf(parsed.category) === -1) {
      return 'ai/unclassified';
    }

    if (parsed.confidence === 'low') {
      return 'ai/unclassified';
    }

    // Safety net: model may ignore the own-domain rule, so enforce it here too.
    if (parsed.category === 'ai/product-release' && CONFIG.OWN_DOMAINS.indexOf(senderDomain) === -1) {
      return 'ai/news';
    }

    return parsed.category;
  } catch (e) {
    Logger.log('classify() error for "' + subject + '": ' + e.message);
    return 'ai/unclassified';
  }
}

function callOpenRouter(apiKey, subject, snippet, senderDomain) {
  var payload = {
    model: CONFIG.MODEL,
    messages: [
      { role: 'system', content: getSystemPrompt(CONFIG.OWN_DOMAINS) },
      { role: 'user',   content: buildUserMessage(subject, snippet, senderDomain) },
    ],
    max_tokens: 60,
    temperature: 0,
  };

  var response = UrlFetchApp.fetch(CONFIG.OPENROUTER_API_URL, {
    method: 'POST',
    contentType: 'application/json',
    headers: { 'Authorization': 'Bearer ' + apiKey },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  });

  var code = response.getResponseCode();
  if (code !== 200) {
    throw new Error('OpenRouter returned ' + code + ': ' + response.getContentText());
  }

  var data = JSON.parse(response.getContentText());
  return data.choices[0].message.content.trim();
}

function getOrCreateLabel(name) {
  var label = GmailApp.getUserLabelByName(name);
  if (!label) label = GmailApp.createLabel(name);
  return label;
}

function extractDomain(fromAddress) {
  var match = fromAddress.match(/@([\w.-]+)/);
  return match ? match[1].toLowerCase() : '';
}

function incrementCounter(category) {
  var props = PropertiesService.getScriptProperties();
  var key = 'count_' + category;
  var current = parseInt(props.getProperty(key) || '0', 10);
  props.setProperty(key, String(current + 1));
}
