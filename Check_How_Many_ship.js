(() => {
  // Step 1: Find all rows (skip the header row)
  const rows = Array.from(document.querySelectorAll('table tr')).slice(1);

  // Step 2: Extract the column headers (optional, in case we need dynamic indexing)
  const headers = Array.from(document.querySelectorAll('table th')).map(th => th.innerText.trim());

  // Get column indexes based on header names
  const merchantNumberIndex = headers.findIndex(h => /Merchant Number/i.test(h));
  const merchantNameIndex   = headers.findIndex(h => /Merchant Name/i.test(h));
  const lastCommentIndex    = headers.findIndex(h => /Last Comment/i.test(h));

  if (merchantNumberIndex === -1 || merchantNameIndex === -1 || lastCommentIndex === -1) {
    console.error('❌ Could not find required columns. Please verify column header text.');
    console.log('Headers found:', headers);
    return;
  }

  // Step 3: Extract data for rows that match condition
  const results = rows
    .map(row => {
      const cells = row.querySelectorAll('td');
      return {
        merchantNumber: cells[merchantNumberIndex]?.innerText.trim() || '',
        merchantName: cells[merchantNameIndex]?.innerText.trim() || '',
        lastComment: cells[lastCommentIndex]?.innerText.trim() || ''
      };
    })
 .filter(row => /Please\s+(ship\s+out|provide)/i.test(row.lastComment));
 
  // Step 4: Copy to clipboard
  const json = JSON.stringify(results, null, 2);
  console.log('✅ Found', results.length, 'matching records');
  console.table(results);

  try {
    navigator.clipboard.writeText(json);
    console.log('✅ JSON copied to clipboard');
  } catch (e) {
    console.warn('⚠️ Could not copy automatically, here is your JSON:');
    console.log(json);
  }
})();
