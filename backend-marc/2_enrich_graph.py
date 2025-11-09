import requests
import json
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKELETON_FILE = os.path.join(SCRIPT_DIR, 'skeleton_graph.json')
FINAL_GRAPH_FILE = os.path.join(SCRIPT_DIR, 'project_graph_ENRICHED.json')
MODEL_NAME = 'nemotron:70b'
OLLAMA_ENDPOINT = 'http://204.52.27.219:11434/api/generate'
SAVE_INTERVAL = 5  # Save more frequently
MAX_RETRIES = 3
TIMEOUT = 300  # 5 minutes timeout for large models

SYSTEM_PROMPT = """
You are an expert senior software architect. Your task is to analyze a code snippet
and provide a structured JSON analysis. Your response MUST be a single, minified JSON
object. Do not include any preamble, postamble, or markdown code blocks.
The JSON object must have these exact keys:
- "purpose": A concise, one-sentence summary of what this function's primary goal is.
- "inputs": An array of objects. Each object should have "name" and "description". If no inputs, return an empty array.
- "outputs": A string describing what this function returns. If it returns nothing (void), describe that.
- "dependencies": An array of strings, listing any key libraries or modules used within this function.
"""

def save_graph(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"  ✓ Checkpoint saved")
    except Exception as e:
        print(f"  ✗ CRITICAL ERROR: Failed to save graph: {e}")

def test_ollama_connection():
    """Test if Ollama server is reachable."""
    print("=" * 70)
    print("Testing Ollama connection...")
    print("=" * 70)
    print(f"Endpoint: {OLLAMA_ENDPOINT}")
    print(f"Model: {MODEL_NAME}")
    
    try:
        # First try to list models
        test_url = OLLAMA_ENDPOINT.replace('/api/generate', '/api/tags')
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print("✓ Ollama server is reachable!")
            models = response.json().get('models', [])
            print(f"✓ Found {len(models)} models on server")
            
            # Check if our model is available
            model_names = [m.get('name', '') for m in models]
            if MODEL_NAME in model_names:
                print(f"✓ Model '{MODEL_NAME}' is available!")
            else:
                print(f"⚠ Warning: Model '{MODEL_NAME}' not found in available models")
                print(f"Available models: {', '.join(model_names[:5])}")
                user_input = input("\nContinue anyway? (y/n): ")
                if user_input.lower() != 'y':
                    return False
        
        # Now test the generate endpoint with a simple request
        print("\nTesting /api/generate endpoint...")
        test_payload = {
            "model": MODEL_NAME,
            "prompt": "Say 'test' in JSON format: {\"response\": \"test\"}",
            "stream": False,
            "options": {"num_predict": 10}
        }
        response = requests.post(OLLAMA_ENDPOINT, json=test_payload, timeout=30)
        
        if response.status_code == 200:
            print("✓ /api/generate endpoint is working!")
            return True
        else:
            print(f"✗ /api/generate returned status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("✗ Connection timeout - server may be slow or unreachable")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Connection error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def call_ollama_with_retry(code_snippet, max_retries=MAX_RETRIES):
    """Call Ollama API with retry logic."""
    # Truncate very long snippets
    if len(code_snippet) > 3000:
        code_snippet = code_snippet[:3000] + "\n... (truncated for token limit)"
    
    user_prompt = f"Code Snippet:\n```\n{code_snippet}\n```"
    
    api_payload = {
        "model": MODEL_NAME,
        "system": SYSTEM_PROMPT,
        "prompt": user_prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 500  # Limit response length
        }
    }
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                wait_time = 5 * attempt
                print(f"    Retry {attempt + 1}/{max_retries} after {wait_time}s delay...")
                time.sleep(wait_time)
            
            response = requests.post(
                OLLAMA_ENDPOINT, 
                json=api_payload, 
                timeout=TIMEOUT
            )
            response.raise_for_status()
            response_data = response.json()
            summary_json_string = response_data.get("response", "")
            
            if not summary_json_string:
                raise ValueError("Empty response from Ollama")
            
            # Try to parse JSON, cleaning up if needed
            clean_response = summary_json_string.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            clean_response = clean_response.strip()
            
            summary_object = json.loads(clean_response)
            return summary_object
            
        except requests.exceptions.Timeout:
            print(f"    ⏱ Timeout on attempt {attempt + 1}")
            if attempt == max_retries - 1:
                raise
        except requests.exceptions.ConnectionError as e:
            print(f"    ✗ Connection error on attempt {attempt + 1}: {str(e)[:50]}")
            if attempt == max_retries - 1:
                raise
        except json.JSONDecodeError as e:
            print(f"    ✗ JSON parse error: {str(e)[:50]}")
            print(f"    Raw response: {summary_json_string[:200]}")
            if attempt == max_retries - 1:
                raise
        except Exception as e:
            print(f"    ✗ Error on attempt {attempt + 1}: {str(e)[:50]}")
            if attempt == max_retries - 1:
                raise
    
    raise Exception("Max retries exceeded")

def main():
    print("\n" + "=" * 70)
    print("CODE ENRICHMENT TOOL - NVIDIA Nemotron via Ollama")
    print("=" * 70 + "\n")
    
    # Test connection first
    if not test_ollama_connection():
        print("\n❌ Cannot connect to Ollama server. Please check:")
        print("   1. Is the NVIDIA GPU instance running?")
        print("   2. Is Ollama server running on the instance?")
        print("   3. Is the firewall allowing connections on port 11434?")
        print("   4. Can you ping 204.52.27.219?")
        print("\nYou can test manually with:")
        print(f"   curl {OLLAMA_ENDPOINT.replace('/api/generate', '/api/tags')}")
        return
    
    print("\n" + "=" * 70)
    
    if os.path.exists(FINAL_GRAPH_FILE):
        print(f"📂 Loading existing graph to resume...")
        with open(FINAL_GRAPH_FILE, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
    elif os.path.exists(SKELETON_FILE):
        print(f"📂 Loading skeleton from {SKELETON_FILE}...")
        with open(SKELETON_FILE, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
    else:
        print(f"❌ ERROR: Cannot find {SKELETON_FILE}")
        print("Please run 1_build_skeleton.py first.")
        return

    functions_to_process = [
        (key, info) for key, info in graph_data["functions"].items()
        if info.get("summary") is None
    ]
    
    if not functions_to_process:
        print("✅ All functions are already processed!")
        return

    total_count = len(functions_to_process)
    print(f"\n📊 Found {total_count} functions to process")
    print(f"💾 Saving checkpoints every {SAVE_INTERVAL} functions")
    print(f"⏱️  Timeout: {TIMEOUT}s per function")
    print(f"🔄 Max retries: {MAX_RETRIES}")
    print("=" * 70 + "\n")
    
    start_time = time.time()
    processed_count = 0
    error_count = 0
    errors = []

    for i, (function_key, function_info) in enumerate(functions_to_process):
        print(f"[{i+1}/{total_count}] {function_key}")
        code_snippet = function_info["code_snippet"]
        
        try:
            summary_object = call_ollama_with_retry(code_snippet)
            graph_data["functions"][function_key]["summary"] = summary_object
            processed_count += 1
            print(f"  ✓ Success ({processed_count}/{total_count})")
            
            # Checkpoint save
            if processed_count % SAVE_INTERVAL == 0:
                save_graph(graph_data, FINAL_GRAPH_FILE)
            
        except Exception as e:
            error_count += 1
            error_msg = f"{function_key}: {str(e)[:80]}"
            errors.append(error_msg)
            print(f"  ✗ FAILED: {str(e)[:80]}")
            
            # Save progress even on error
            if error_count % SAVE_INTERVAL == 0:
                save_graph(graph_data, FINAL_GRAPH_FILE)
            
            # Optional: stop after too many consecutive errors
            if error_count >= 5 and processed_count == 0:
                print("\n❌ Too many errors. Stopping to prevent waste.")
                print("Please check the Ollama server status.")
                break

    end_time = time.time()
    elapsed = end_time - start_time
    
    print("\n" + "=" * 70)
    print("ENRICHMENT COMPLETE")
    print("=" * 70)
    print(f"⏱️  Total time: {elapsed:.2f}s ({elapsed/60:.1f} min)")
    print(f"✅ Processed: {processed_count}/{total_count}")
    print(f"❌ Errors: {error_count}")
    if processed_count > 0:
        print(f"📈 Success rate: {(processed_count/total_count)*100:.1f}%")
        print(f"⚡ Avg time per function: {elapsed/processed_count:.1f}s")
    print("=" * 70)
    
    if errors:
        print("\n❌ Failed functions:")
        for err in errors[:10]:  # Show first 10
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    
    print(f"\n💾 Saving final results...")
    save_graph(graph_data, FINAL_GRAPH_FILE)
    print("✅ Done!\n")

if __name__ == "__main__":
    main()