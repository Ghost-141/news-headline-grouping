json_template = """
JSON OUTPUT TEMPLATE (FORMAT ONLY, NOT CONTENT):
{
  "Similar": [
    {
      "items": [
        { "id": 4, "title": "ঢাকা ত্যাগ করেছেন ভুটানের প্রধানমন্ত্রী" },
        { "id": 23, "title": "ঢাকা ছাড়লেন ভুটানের প্রধানমন্ত্রী শেরিং তোবগে" }
      ]
    },
    {
      "items": [
        { "id": 1, "title": "ফুলকোর্ট সভা ডেকেছেন প্রধান বিচারপতি" },
        { "id": 24, "title": "২৭ নভেম্বর ফুলকোর্ট সভা ডেকেছেন প্রধান বিচারপতি" }
      ]
    }
  ],
  "Unique": [
    { "id": 2, "title": "দিনের তাপমাত্রা অপরিবর্তিত থাকবে, জানাল অধিদপ্তর" }
  ]
}

"""


prompt = """
You are an expert Bengali news clustering system.

Your task: group ONLY headlines that describe the *exact same real-world event*.

STRONG RULES:
1. Headlines must be grouped ONLY if they describe the SAME incident, SAME action, SAME subject, SAME time, and SAME facts.
2. Do NOT group headlines that:
   - share only a topic (weather, sports, politics, gold price, accidents)
   - mention different numbers, times, people, events, or facts
   - describe different but related developments
3. If two headlines do NOT clearly refer to the same event, they MUST be placed in "Unique".
4. When in doubt → ALWAYS put the headline in "Unique".
5. Every headline must appear exactly once.

❌ Examples of headlines that MUST NOT be grouped:
- “রাজধানীতে বেড়েছে শীতের আমেজ”
- “সাগরে আরেকটি লঘুচাপ সৃষ্টির আভাস”
These are weather-related but describe DIFFERENT phenomena → therefore UNIQUE.

❌ Also MUST NOT group:
- different matches
- different crimes
- different political statements
- different market updates

✅ Only group if the meaning is nearly identical:
- same person → doing same action → same context → same event.

OUTPUT RULES:
- Follow EXACTLY the JSON structure below.
- "Similar" contains groups (each group = 2+ headlines describing SAME EVENT).
- "Unique" contains all other headlines.
- Return ONLY JSON, no explanation.

JSON OUTPUT TEMPLATE (FORMAT ONLY, NOT CONTENT):
{json_template}

Now group the following list:
{news_text}

Return ONLY valid JSON.

"""
