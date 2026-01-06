"""
Test script for Video Downloader API
"""
import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "test-api-key-123"

def test_health_check():
    """Test health check endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_missing_api_key():
    """Test authentication - missing API key"""
    print("Testing authentication (missing API key)...")
    response = requests.post(
        f"{BASE_URL}/download",
        json={"url": "https://www.youtube.com/watch?v=test"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 401

def test_invalid_api_key():
    """Test authentication - invalid API key"""
    print("Testing authentication (invalid API key)...")
    response = requests.post(
        f"{BASE_URL}/download",
        headers={"X-API-Key": "wrong-key"},
        json={"url": "https://www.youtube.com/watch?v=test"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 403

def test_download_short_video():
    """Test downloading a short video (Me at the zoo - first YouTube video)"""
    print("Testing video download (short video)...")
    print("Downloading: https://www.youtube.com/watch?v=jNQXAC9IVRw")
    
    response = requests.post(
        f"{BASE_URL}/download",
        headers={"X-API-Key": API_KEY},
        json={"url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data.get('title')}")
        print(f"Source: {data.get('source')}")
        print(f"Total Size: {data.get('total_size_mb')} MB")
        print(f"Duration: {data.get('duration_seconds')} seconds")
        print(f"Number of chunks: {len(data.get('chunks', []))}")
        
        for chunk in data.get('chunks', []):
            print(f"  Chunk {chunk['index']}: {chunk['size_mb']} MB (data length: {len(chunk['data'])} chars)")
        print()
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Video Downloader API - Test Suite")
    print("=" * 60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Missing API Key", test_missing_api_key()))
    results.append(("Invalid API Key", test_invalid_api_key()))
    results.append(("Download Video", test_download_short_video()))
    
    # Summary
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
