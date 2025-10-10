import requests

version = "v2409"
# this is sandbox url
# url = "https://wwwcie.ups.com/api/shipments/" + version + "/ship"


url = "https://onlinetools.ups.com/api/shipments/" + version + "/ship"

query = {
  "additionaladdressvalidation": "string"
}

payload = {
  "ShipmentRequest": {
    "Request": {
      "SubVersion": "1801",
      "RequestOption": "nonvalidate",
      "TransactionReference": {
        "CustomerContext": ""
      }
    },
    "Shipment": {
      "Description": "Ship WS test",
      "Shipper": {
        "Name": "Epay World & AIYA Technology",
        "AttentionName": " ",
        "TaxIdentificationNumber": "123456",
        "Phone": {
          "Number": "888-998-8638",
          "Extension": " "
        },
        "ShipperNumber": " ",
        "FaxNumber": "8002222222",
        "Address": {
          "AddressLine": [
            "132 32nd Street STE # 107"
          ],
          "City": "Brooklyn",
          "StateProvinceCode": "NY",
          "PostalCode": "11232",
          "CountryCode": "US"
        }
      },
      "ShipTo": {
        "Name": "Epay World & AIYA Technology",
        "AttentionName": "Deployment",
        "Phone": {
          "Number": "888-998-8638"
        },
        "FaxNumber": "1234567890",
        "Address": {
          "AddressLine": [
            "132 32nd Street STE # 107"
          ],
          "City": "Brooklyn",
          "StateProvinceCode": "NY",
          "PostalCode": "11232",
          "CountryCode": "US"
        }
        
        
      },


      ####change here #####
      "ShipFrom": {
        "Name": "BUFFET CITY",
        "AttentionName": " ",
        "Phone": {
          "Number": "7574883888"
        },
        "Address": {
          "AddressLine": [
            "4300 PORTSMOUTH BLVD SUITE 118"
          ],
          "City": "CHESAPEAKE",
          "StateProvinceCode": "VA",
          "PostalCode": "23321-2137",
          "CountryCode": "US"
        },
        "Residential": " "
      },


      
      "PaymentInformation": {
        "ShipmentCharge": {
          "Type": "01",
          "BillShipper": {
            "AccountNumber": " "
          }
        }
      },
      "Service": {
        "Code": "03",
        "Description": "Express"
      },
      "Package": {
        "Description": " ",
        "Packaging": {
          "Code": "02",
          "Description": "Nails"
        },
        "Dimensions": {
          "UnitOfMeasurement": {
            "Code": "IN",
            "Description": "Inches"
          },
          "Length": "12",
          "Width": "8",
          "Height": "5"
        },
        "PackageWeight": {
          "UnitOfMeasurement": {
            "Code": "LBS",
            "Description": "Pounds"
          },
          "Weight": "3"
        },

    "PackageServiceOptions": {
    "DeclaredValue": {
      "CurrencyCode": "USD",
      "MonetaryValue": "499.00"
    }
      }
        
      }
    },
    "LabelSpecification": {
      "LabelImageFormat": {
        "Code": "GIF",
        "Description": "GIF"
      },
      "HTTPUserAgent": "Mozilla/4.5"
    }
  }
}

headers = {
  "Content-Type": "application/json",
  "transId": "string",
  "transactionSrc": "testing",

  # place your UPS API token here
  "Authorization": "Bearer xxxx"
}

response = requests.post(url, json=payload, headers=headers, params=query)

data = response.json()
# print(data)

try:
    shipment_results = data["ShipmentResponse"]["ShipmentResults"]

    tracking_number = shipment_results["PackageResults"][0]["TrackingNumber"]
    total_charges = shipment_results["ShipmentCharges"]["TotalCharges"]["MonetaryValue"]
    weight = shipment_results["BillingWeight"]["Weight"]

    # Get from payload (since these were sent in your request)
    ship_from = payload["ShipmentRequest"]["Shipment"]["ShipFrom"]
    merchant_name = ship_from.get("Name", " ")
    address_line = ship_from["Address"]["AddressLine"][0]
    city = ship_from["Address"]["City"]
    state = ship_from["Address"]["StateProvinceCode"]
    postal_code = ship_from["Address"]["PostalCode"]

    # Declared value (if provided)
    declared_value = (
        payload["ShipmentRequest"]["Shipment"]
        .get("Package", {})
        .get("PackageServiceOptions", {})
        .get("DeclaredValue", {})
        .get("MonetaryValue", "N/A")
    )

    print("📦 UPS Shipment Summary:")
    print("------------------------")
    print(f"Merchant Name: {merchant_name}")
    print(f"Destination: {address_line}, {city}, {state} {postal_code}")
    
    print(f"Total Charges (USD): {total_charges}")
    print(f"Weight (LBS): {weight}")
    print(f"Declared Value (USD): {declared_value}")
    print(f"Return label created.\nTracking #: {tracking_number}\nPlease call and send the PDF file of return label and EPW Returning Policy Form to merchant And inform merchant to return the old device within 10 days.\nPlease check ss for required documents.")


except (KeyError, IndexError) as e:
    print("⚠️ Some data could not be found in the response:", e)