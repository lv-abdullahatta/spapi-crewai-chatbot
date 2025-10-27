"""
Amazon SP-API Credential Validator
Tests if your SP-API credentials are working correctly
"""

import os
import json
import requests
from datetime import datetime, timedelta
import hashlib
import hmac
from urllib.parse import quote

# Your credentials (use environment variables in production!)
SP_API_REFRESH_TOKEN = os.getenv("SP_API_REFRESH_TOKEN", "Atzr|IwEBIC48BHZ4qtl05lVzIFmxdazmxsjrGkbGy1c4ewigkD4PUvMW7oss4BIbeqilv22AyIogeYTxSwezsQDwZ9CzgCfyAML8RfDXvvDffPWNvhDsUp1HMPLV1e6w0JtxyJU1_OayGxp08gSFVYCkUCZX3a7A_pEIrWyJLvy5hwp6J5WSrpU14Pqa-SVQP3GsSpnGkBOlthhvIiGkKmZzVkEzAjEsOxl4_A02JYbQuI3CC-ZpNPBYEtb-aiCq1TjvmsUkL9mP9vBPFYUwM04Kq0ruBGePo9DESIu1LihW9cPhLY-2WyKlKrNFUECIEhy0u-0OZKi36fnacfsDzY7EtS5_byoX")
SP_API_CLIENT_ID = os.getenv("SP_API_CLIENT_ID", "amzn1.application-oa2-client.6fbe2b3c64c84200ab5f3688101a9eaa")
SP_API_CLIENT_SECRET = os.getenv("SP_API_CLIENT_SECRET", "amzn1.oa2-cs.v1.7f5299cbce6429e61871f14268dcd312cb35f1facf3e851244d1e087ed14b9bc")
SP_API_REGION = os.getenv("SP_API_REGION", "us-east-1")
SP_API_MARKETPLACE_ID = os.getenv("SP_API_MARKETPLACE_ID", "ATVPDKIKX0DER")

# SP-API endpoints
LWA_TOKEN_URL = "https://api.amazon.com/auth/o2/token"
SP_API_ENDPOINTS = {
    "us-east-1": "https://sellingpartnerapi-na.amazon.com",
    "eu-west-1": "https://sellingpartnerapi-eu.amazon.com",
    "us-west-2": "https://sellingpartnerapi-fe.amazon.com"
}


class SPAPIValidator:
    """Validates Amazon SP-API credentials"""
    
    def __init__(self):
        self.access_token = None
        self.base_url = SP_API_ENDPOINTS.get(SP_API_REGION)
        
    def validate_credentials(self):
        """Run all validation checks"""
        print("=" * 70)
        print("Amazon SP-API Credential Validation")
        print("=" * 70)
        print()
        
        results = {
            "credential_format": self.check_credential_format(),
            "token_exchange": self.test_token_exchange(),
            "api_access": None
        }
        
        # Only test API if token exchange succeeded
        if results["token_exchange"]["success"]:
            results["api_access"] = self.test_api_access()
        
        # Summary
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        all_passed = True
        for check, result in results.items():
            if result and not result.get("success"):
                all_passed = False
        
        if all_passed:
            print("✓ All checks passed! Your credentials are working correctly.")
        else:
            print("✗ Some checks failed. Please review the details above.")
        
        return results
    
    def check_credential_format(self):
        """Check if credentials have correct format"""
        print("1. Checking Credential Format...")
        print("-" * 70)
        
        checks = []
        
        # Check Client ID format
        if SP_API_CLIENT_ID.startswith("amzn1.application-oa2-client."):
            print("  ✓ Client ID format is correct")
            checks.append(True)
        else:
            print("  ✗ Client ID format is incorrect")
            print(f"    Expected: amzn1.application-oa2-client.xxxxxxxx")
            print(f"    Got: {SP_API_CLIENT_ID[:20]}...")
            checks.append(False)
        
        # Check Client Secret format
        if SP_API_CLIENT_SECRET.startswith("amzn1.oa2-cs.v1."):
            print("  ✓ Client Secret format is correct")
            checks.append(True)
        else:
            print("  ✗ Client Secret format is incorrect")
            print(f"    Expected: amzn1.oa2-cs.v1.xxxxxxxx")
            print(f"    Got: {SP_API_CLIENT_SECRET[:20]}...")
            checks.append(False)
        
        # Check Refresh Token format
        if SP_API_REFRESH_TOKEN.startswith("Atzr|"):
            print("  ✓ Refresh Token format is correct")
            checks.append(True)
        else:
            print("  ✗ Refresh Token format is incorrect")
            print(f"    Expected: Atzr|xxxxxxxx")
            print(f"    Got: {SP_API_REFRESH_TOKEN[:10]}...")
            checks.append(False)
        
        # Check if any are empty
        if not SP_API_CLIENT_ID or not SP_API_CLIENT_SECRET or not SP_API_REFRESH_TOKEN:
            print("  ✗ One or more credentials are empty!")
            checks.append(False)
        
        success = all(checks)
        print()
        return {"success": success, "checks": checks}
    
    def test_token_exchange(self):
        """Test exchanging refresh token for access token"""
        print("2. Testing Token Exchange (LWA Authentication)...")
        print("-" * 70)
        
        try:
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": SP_API_REFRESH_TOKEN,
                "client_id": SP_API_CLIENT_ID,
                "client_secret": SP_API_CLIENT_SECRET
            }
            
            print("  → Requesting access token from Amazon...")
            response = requests.post(LWA_TOKEN_URL, data=payload, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)
                
                print(f"  ✓ Access token obtained successfully!")
                print(f"  ✓ Token expires in: {expires_in} seconds ({expires_in/60:.1f} minutes)")
                print(f"  ✓ Token type: {token_data.get('token_type')}")
                print()
                
                return {
                    "success": True,
                    "access_token": self.access_token[:20] + "...",
                    "expires_in": expires_in
                }
            else:
                print(f"  ✗ Token exchange failed!")
                print(f"  Status code: {response.status_code}")
                print(f"  Response: {response.text}")
                print()
                
                # Parse error
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error_description", error_data.get("error"))
                    print(f"  Error: {error_msg}")
                except:
                    pass
                
                print("\n  Common issues:")
                print("  - Invalid Client ID or Client Secret")
                print("  - Expired or revoked Refresh Token")
                print("  - Credentials from different application")
                print()
                
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text
                }
                
        except requests.exceptions.Timeout:
            print("  ✗ Request timed out")
            print()
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            print(f"  ✗ Exception occurred: {str(e)}")
            print()
            return {"success": False, "error": str(e)}
    
    def test_api_access(self):
        """Test making an actual SP-API call"""
        print("3. Testing SP-API Access (Making Test Call)...")
        print("-" * 70)
        
        if not self.access_token:
            print("  ✗ No access token available")
            print()
            return {"success": False, "error": "No access token"}
        
        try:
            # Test with getMarketplaceParticipations - simple endpoint
            endpoint = f"{self.base_url}/sellers/v1/marketplaceParticipations"
            
            headers = {
                "x-amz-access-token": self.access_token,
                "Content-Type": "application/json"
            }
            
            print(f"  → Testing endpoint: /sellers/v1/marketplaceParticipations")
            print(f"  → Region: {SP_API_REGION}")
            print(f"  → Base URL: {self.base_url}")
            print()
            
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print("  ✓ SP-API call successful!")
                
                if "payload" in data:
                    marketplaces = data["payload"]
                    print(f"  ✓ Found {len(marketplaces)} marketplace(s)")
                    
                    for mp in marketplaces:
                        participation = mp.get("participation", {})
                        marketplace = mp.get("marketplace", {})
                        print(f"    - {marketplace.get('name')} ({marketplace.get('id')})")
                        print(f"      Seller: {participation.get('isParticipating', False)}")
                
                print()
                return {
                    "success": True,
                    "marketplaces": len(marketplaces) if "payload" in data else 0
                }
            
            elif response.status_code == 403:
                print("  ✗ Access denied (403 Forbidden)")
                print("  This usually means:")
                print("  - Your app doesn't have required permissions")
                print("  - The seller hasn't authorized your app")
                print("  - AWS IAM role is not properly configured")
                print()
                return {"success": False, "status_code": 403, "error": "Forbidden"}
            
            elif response.status_code == 401:
                print("  ✗ Authentication failed (401 Unauthorized)")
                print("  The access token may be invalid or expired")
                print()
                return {"success": False, "status_code": 401, "error": "Unauthorized"}
            
            else:
                print(f"  ✗ API call failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                print()
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text
                }
                
        except requests.exceptions.Timeout:
            print("  ✗ Request timed out")
            print()
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            print(f"  ✗ Exception occurred: {str(e)}")
            print()
            return {"success": False, "error": str(e)}


def main():
    """Main validation function"""
    
    # Check if credentials are set
    if not SP_API_CLIENT_ID or not SP_API_CLIENT_SECRET or not SP_API_REFRESH_TOKEN:
        print("ERROR: Credentials not found!")
        print()
        print("Please set the following environment variables:")
        print("  - SP_API_CLIENT_ID")
        print("  - SP_API_CLIENT_SECRET")
        print("  - SP_API_REFRESH_TOKEN")
        print("  - SP_API_REGION (optional, defaults to us-east-1)")
        print()
        print("Or edit this script and add them directly (NOT RECOMMENDED for production)")
        return
    
    # Run validation
    validator = SPAPIValidator()
    results = validator.validate_credentials()
    
    # Additional recommendations
    print("\n" + "=" * 70)
    print("SECURITY RECOMMENDATIONS")
    print("=" * 70)
    print("1. NEVER share these credentials publicly")
    print("2. Store credentials in environment variables or secure vault")
    print("3. Rotate credentials regularly")
    print("4. Use IAM roles with least privilege")
    print("5. Monitor API usage for unusual activity")
    print()
    
    return results


if __name__ == "__main__":
    main()