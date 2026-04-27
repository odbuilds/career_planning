// Triggered once per day (set to ~8am in your timezone).
// Reads daily email counts, sends a summary to Telegram, then resets counters.
function sendDailySummary() {
  var props = PropertiesService.getScriptProperties();
  var botToken = props.getProperty('TELEGRAM_BOT_TOKEN');
  var chatId = props.getProperty('TELEGRAM_CHAT_ID');

  if (!botToken || !chatId) {
    Logger.log('Telegram credentials not set — skipping daily summary.');
    return;
  }

  var counts = {};
  var total = 0;

  CONFIG.LABELS.forEach(function(label) {
    var n = parseInt(props.getProperty('count_' + label) || '0', 10);
    counts[label] = n;
    total += n;
  });

  if (total === 0) {
    Logger.log('No emails processed today — skipping Telegram summary.');
    return;
  }

  var lines = [
    '📬 *email-classify daily summary*',
    'Processed: *' + total + ' emails*',
    '',
  ];

  CONFIG.LABELS
    .slice()
    .sort(function(a, b) { return counts[b] - counts[a]; })
    .forEach(function(label) {
      if (counts[label] > 0) {
        lines.push('`' + padRight(label, 22) + '` ' + counts[label]);
      }
    });

  var ok = postToTelegram(botToken, chatId, lines.join('\n'));

  if (ok) {
    CONFIG.LABELS.forEach(function(label) {
      props.deleteProperty('count_' + label);
    });
    Logger.log('Daily summary sent. Counters reset.');
  }
}

function postToTelegram(botToken, chatId, text) {
  var url = 'https://api.telegram.org/bot' + botToken + '/sendMessage';
  var response = UrlFetchApp.fetch(url, {
    method: 'POST',
    contentType: 'application/json',
    payload: JSON.stringify({ chat_id: chatId, text: text, parse_mode: 'Markdown' }),
    muteHttpExceptions: true,
  });

  var code = response.getResponseCode();
  if (code !== 200) {
    Logger.log('Telegram error ' + code + ': ' + response.getContentText());
    return false;
  }
  return true;
}

function padRight(str, len) {
  while (str.length < len) str += ' ';
  return str;
}
