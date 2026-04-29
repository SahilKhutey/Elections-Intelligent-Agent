import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_endpoint(name, url, method="GET", data=None):
    print(f"Testing {name}...", end=" ", flush=True)
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print("[OK]")
            return True
        else:
            print(f"[FAIL] (Status: {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR]: {e}")
        return False

def run_validation():
    print("=== EIA Backend Validation ===\n")
    results = []
    
    # 1. Health Check
    results.append(test_endpoint("Root Health", "http://localhost:8000/"))
    
    # 2. Timeline
    results.append(test_endpoint("Timeline (EN)", f"{BASE_URL}/timeline?lang=en&location=India"))
    results.append(test_endpoint("Timeline (HI)", f"{BASE_URL}/timeline?lang=hi&location=India"))
    
    # 3. FAQ
    results.append(test_endpoint("FAQ Retrieval", f"{BASE_URL}/faq"))
    
    # 4. Notices
    results.append(test_endpoint("Notices List", f"{BASE_URL}/notices"))
    
    # 5. Query (Intent Detection)
    query_data = {"query": "How do I vote?", "lang": "en", "location": "India"}
    results.append(test_endpoint("Query API", f"{BASE_URL}/query", method="POST", data=query_data))
    
    # 6. Eligibility
    elig_data = {"age": 20, "citizenship": "India", "lang": "en"}
    results.append(test_endpoint("Eligibility Check", f"{BASE_URL}/eligibility", method="POST", data=elig_data))

    print("\n" + "="*30)
    if all(results):
        print("ALL TESTS PASSED! System is operational.")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED. Please check logs.")
        sys.exit(1)

if __name__ == "__main__":
    run_validation()
