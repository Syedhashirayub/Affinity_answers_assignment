import requests

def extract_pincode(address):
    # Here I extracted the 6-digit PIN code from the address
    words = address.split()
    for word in words:
        if word.isdigit() and len(word) == 6:
            return word
    return None

def fetch_pincode_details(pincode):
    # Here I am using the provided API 
    url = f"http://www.postalpincode.in/api/pincode/{pincode}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None

def check_address(address):
    pincode = extract_pincode(address)
    if not pincode:
        return False
    
    details = fetch_pincode_details(pincode)
    if not details or details['Status'] != "Success":
        return False

    # Checking if any part of the address matches the PostOffice details from the API
    for post_office in details['PostOffice']:
        if post_office['Name'].lower() in address.lower():
            return True
    return False

if __name__ == "__main__":
    address = input("Enter the address: ")
    if check_address(address):
        print("Address and PIN code match.")
    else:
        print("Address and PIN code do not match.")

"""
Test cases:

Positive Cases:

"2nd Phase, 374/B, 80 Feet Rd, Mysore Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bengaluru, Karnataka 560050"
"2nd Phase, 374/B, 80 Feet Rd, Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bengaluru, Karnataka 560050"
"kelabadi, durg,chhattisgarh 491001"
"padmanagpur,durg,chhattisgarh 491001"
"374/B, 80 Feet Rd, State Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bangalore. 560050"

Negative Cases:

"2nd Phase, 374/B, 80 Feet Rd, Mysore Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bengaluru, Karnataka 890095"
"Colony, Bengaluru, Karnataka 567550"
"padmanagpur, durg, chhattisgarh"              ->Addresses without a PIN code.
"padmanagpur,durg,chhattisgarh 500675 491001"  ->Addresses with multiple 6-digit numbers 
"chhattisgarh 491001"                          ->Addresses with a PIN code but no other details.

"""
