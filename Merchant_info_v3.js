function extractMerchantInfo() {
  const text = document.body.innerText;

  function getValue(label) {
    const regex = new RegExp(label + "\\s*:?\\s*(.+)");
    const match = text.match(regex);
    return match ? match[1].trim() : "";
  }

  const merchantName = getValue("Merchant Name");
  const phone = getValue("Phone");
  let address = getValue("Address");

  // Normalize commas
  address = address.replace(/，/g, ",");

  // Parse address
  const addrRegex = /(.*?)[,，]\s*([A-Za-z\s]+)[,，]\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)/;
  const addrMatch = address.match(addrRegex);

  const addressLine = addrMatch ? addrMatch[1].trim() : "";
  const city = addrMatch ? addrMatch[2].trim() : "";
  const state = addrMatch ? addrMatch[3].trim() : "";
  const postalCode = addrMatch ? addrMatch[4].trim() : "";

  // Construct formatted text (no escaped characters)
  const jsonText = `      "ShipTo": {
        "Name": "${merchantName || " "}",
        "AttentionName": " ",
        "Phone": {
          "Number": "${phone || " "}"
        },
        "Address": {
          "AddressLine": [
            "${addressLine || " "}"
          ],
          "City": "${city || " "}",
          "StateProvinceCode": "${state || " "}",
          "PostalCode": "${postalCode || " "}",
          "CountryCode": "US"
        },
        "Residential": " "
      },`;

  // 👇 Log the formatted text directly (no quotes, no escapes)
  console.log(jsonText);

  return jsonText;
}

extractMerchantInfo();
