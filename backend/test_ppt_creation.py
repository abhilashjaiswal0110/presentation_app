#!/usr/bin/env python3
"""
Test script to verify PPT creation functionality end-to-end.
"""
import httpx
import json
import asyncio
import sys

API_BASE = "http://localhost:8000"

async def test_create_presentation():
    """Test creating a simple presentation via the agent."""
    print("Testing PPT creation functionality...")
    print("-" * 50)

    # Prepare form data for agent request
    form_data = {
        "instructions": "Create a simple presentation with title 'Test Presentation' and 2 slides: slide 1 about AI, slide 2 about Machine Learning",
        "is_continuation": "false",
    }

    print("\n1. Sending request to agent to create presentation...")

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            # Make streaming request to agent
            async with client.stream(
                "POST",
                f"{API_BASE}/agent-stream",
                data=form_data
            ) as response:
                if response.status_code != 200:
                    print(f"ERROR: Agent request failed with status {response.status_code}")
                    return False

                user_session_id = None
                slide_count = 0

                # Process SSE stream
                print("\n2. Processing agent stream...")
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix
                        try:
                            data = json.loads(data_str)
                            msg_type = data.get("type")

                            if msg_type == "init":
                                print(f"   [OK] Agent initialized")
                            elif msg_type == "status":
                                print(f"   -> {data.get('message')}")
                            elif msg_type == "tool_use":
                                friendly = data.get('friendly', [])
                                if friendly:
                                    for desc in friendly:
                                        print(f"   [TOOL] {desc}")
                            elif msg_type == "assistant":
                                text = data.get('text', '')
                                if text:
                                    preview = text[:80].replace('\n', ' ')
                                    print(f"   [AGENT] {preview}...")
                            elif msg_type == "complete":
                                user_session_id = data.get('user_session_id')
                                slide_count = data.get('slide_count', 0)
                                print(f"\n   [OK] Agent completed!")
                                print(f"   Session ID: {user_session_id}")
                                print(f"   Slides created: {slide_count}")
                            elif msg_type == "error":
                                print(f"\n   [ERROR] Error: {data.get('error')}")
                                return False
                        except json.JSONDecodeError:
                            pass

                if not user_session_id:
                    print("ERROR: No session ID received from agent")
                    return False

                if slide_count == 0:
                    print("ERROR: No slides were created")
                    return False

                print(f"\n3. Retrieving session data...")
                # Get session to verify it exists
                session_response = await client.get(f"{API_BASE}/session/{user_session_id}")
                if session_response.status_code != 200:
                    print(f"ERROR: Could not retrieve session: {session_response.status_code}")
                    return False

                session_data = session_response.json()
                presentation = session_data.get('presentation')
                if not presentation:
                    print("ERROR: No presentation in session")
                    return False

                print(f"   [OK] Presentation title: {presentation.get('title')}")
                print(f"   [OK] Number of slides: {len(presentation.get('slides', []))}")

                # List slides
                print(f"\n4. Verifying slides...")
                for i, slide in enumerate(presentation.get('slides', [])):
                    preview = slide.get('html', '')[:60].replace('\n', ' ')
                    print(f"   Slide {i+1}: {preview}...")

                # Test export functionality
                print(f"\n5. Testing PPTX export...")
                export_response = await client.get(f"{API_BASE}/session/{user_session_id}/export")
                if export_response.status_code != 200:
                    print(f"ERROR: Export failed with status {export_response.status_code}")
                    print(f"Response: {export_response.text}")
                    return False

                pptx_size = len(export_response.content)
                print(f"   [OK] PPTX exported successfully!")
                print(f"   File size: {pptx_size:,} bytes")

                # Verify it's a valid PPTX file (starts with PK zip signature)
                if export_response.content[:4] == b'PK\x03\x04':
                    print(f"   [OK] Valid PPTX file format confirmed")
                else:
                    print(f"   [WARN] Warning: File may not be valid PPTX format")

                print("\n" + "=" * 50)
                print("[SUCCESS] ALL TESTS PASSED!")
                print("=" * 50)
                return True

        except httpx.TimeoutException:
            print("ERROR: Request timed out")
            return False
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = asyncio.run(test_create_presentation())
    sys.exit(0 if success else 1)
