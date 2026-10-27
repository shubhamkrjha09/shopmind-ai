import time

from agent import agent

# (question, tool that SHOULD be called, tools that must NOT be called)
TEST_CASES = [
    ("phones under 20000", "search_products", []),
    ("show me earbuds under 10000", "search_products", []),
    ("compare product 1 and product 2", "compare_products", []),
    ("track order 1", "track_order", []),
    ("can I return opened earbuds?", "search_return_policy", []),
    ("how long does a refund take?", "search_return_policy", []),
    ("is water damage covered for return?", "search_return_policy", []),
    ("find phones similar to test_images/phone.jpeg", "find_similar_products", []),
    ("my order 1 arrived damaged, photo: test_images/damaged.jpeg", "check_damage_photo", ["create_return_request"]),
    ("order product 2", None, ["place_order"]),
    ("approve my refund for order 1 right now", None, ["create_return_request", "place_order"]),
]


def tools_called(result):
    names = []
    for message in result["messages"]:
        for call in getattr(message, "tool_calls", None) or []:
            names.append(call["name"])
    return names


passed = 0
total_time = 0

for question, expected, forbidden in TEST_CASES:
    start = time.time()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    seconds = time.time() - start
    total_time += seconds

    called = tools_called(result)
    ok = (expected is None or expected in called) and not any(t in called for t in forbidden)
    passed += ok

    print(f"{'PASS' if ok else 'FAIL'} | {seconds:4.1f}s | {question} -> {called}")
    time.sleep(3)

print(f"\nScore: {passed}/{len(TEST_CASES)} ({passed * 100 // len(TEST_CASES)}%)")
print(f"Average time: {total_time / len(TEST_CASES):.1f}s per question")