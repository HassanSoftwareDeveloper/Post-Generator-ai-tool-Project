from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


TONE_INSTRUCTIONS = {
    "Professional":              "Write in a polished, formal professional tone suitable for executives and senior professionals.",
    "Expert Opinion":            "Write as an industry expert sharing a unique, forward-thinking perspective that challenges conventional wisdom.",
    "Teach Me Something":        "Write in a clear, structured teaching style that breaks down a complex topic into easy-to-understand insights.",
    "Facts & Numbers":           "Write using statistics, facts, and evidence to back every claim. Lead with a surprising data point.",
    "Straight to the Point":     "Write with confidence and authority. State opinions as facts. No hedging language.",
    "Uplifting":                 "Write in an uplifting, emotionally resonant tone that motivates the reader to take action or believe in themselves.",
    "Tell a Story":              "Write as a narrative story with a clear beginning, conflict, and resolution. Make it personal and vivid.",
    "Real & Honest":             "Write with raw honesty and vulnerability. Share a struggle, failure, or lesson learned. Be real, not polished.",
    "Push Me to Act":            "Write with high energy and drive. Use short punchy sentences. Push the reader to act now.",
    "I Understand You":          "Write with deep understanding and compassion. Acknowledge the reader's pain points and speak to their emotions.",
    "Chill & Friendly":          "Write like you're texting a smart friend. Relaxed, no jargon, conversational and warm.",
    "Just Talking":              "Write as if having a one-on-one conversation. Ask questions, use 'you', keep it flowing naturally.",
    "Clever & Witty":            "Write with clever wordplay, dry humor, and sharp observations. Smart and entertaining.",
    "Make Me Laugh":             "Write with genuine humor and light-heartedness. Make the reader laugh or smile while delivering value.",
    "Feels Like Me":             "Write about universal experiences that make the reader think 'this is exactly me'. Use everyday language.",
    "Bold & Controversial":      "Write a bold, provocative take that challenges the status quo. Start with a statement most people disagree with.",
    "My Strong Opinion":         "Write with a strong personal opinion. Take a clear stance and defend it confidently.",
    "Here's the Problem & Fix":  "Write by first clearly stating a painful problem, then presenting a clear, actionable solution.",
    "Step by Step":              "Write as a step-by-step guide. Use numbered steps or clear structure. Practical and actionable.",
    "Quick List":                "Write as a numbered or bulleted list of insights, tips, or lessons. Each point should be punchy and standalone.",
    "Short & Powerful":          "Write with extreme brevity. Every word must earn its place. Short sentences. High impact. No fluff.",
    "Poetic":                    "Write with lyrical, rhythmic language. Use metaphors, imagery, and a flowing structure.",
    "What's Trending":           "Write as a sharp commentary on a current trend or news event. Give your unique take on why it matters.",
    "Behind the Scenes":         "Write as an insider revealing what really happens behind closed doors. Make it feel exclusive and candid.",
    "Take Action Now":           "Write with the primary goal of driving a specific action. Every line should build toward a compelling CTA.",
}

def get_length_str(length):
    if length == "Short":
        return "8 to 12 lines"
    if length == "Medium":
        return "15 to 22 lines"
    if length == "Long":
        return "28 to 40 lines"


def get_structure_guide(length):
    if length == "Short":
        return """
POST STRUCTURE (Short):
- Line 1: One punchy hook sentence that stops the scroll
- Lines 2-8: Core message in 2-3 short paragraphs, 1-2 sentences each
- Last line: A question or one-liner that invites a reaction
- Then one blank line
- Then hashtags on a new line
"""
    if length == "Medium":
        return """
POST STRUCTURE (Medium):
- Line 1: A bold or curious hook
- Lines 2-5: Set the context or tell the beginning of a story
- Lines 6-14: The main insight, lesson, or argument — broken into small paragraphs
- Lines 15-20: A takeaway or reflection
- Last line: End with a question or call to thought
- Then one blank line
- Then hashtags on a new line
"""
    if length == "Long":
        return """
POST STRUCTURE (Long):
- Line 1-2: A strong hook — a story opening, a bold claim, or a surprising fact
- Lines 3-10: Build the story or argument with real detail and emotion
- Lines 11-20: The turning point — the lesson, the shift, the insight
- Lines 21-30: Practical takeaways or deeper reflection
- Lines 31-38: Wrap up with something memorable
- Last line: A genuine question or invitation to share their experience
- Then one blank line
- Then hashtags on a new line
"""


def generate_post(length, language, tag, tone="Professional"):
    prompt = get_prompt(length, language, tag, tone)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, tone="Professional"):
    length_str = get_length_str(length)
    tone_instruction = TONE_INSTRUCTIONS.get(tone, f"Write in a {tone} tone.")
    structure_guide = get_structure_guide(length)

    prompt = f'''
You are a real person writing a post — not an AI, not a content tool.
Write exactly like a human who is sitting down, thinking out loud, and typing naturally.

HUMAN WRITING RULES:
- Never start with "I am excited to share", "In today's world", "As a professional", or any cliche AI opener
- Use short sentences. Then a longer one. Mix it up naturally.
- Add a line break after every 1-2 sentences — like real posts look
- Occasionally start a sentence with "And", "But", "So", "Because" — humans do this
- Use contractions: don't, can't, I've, you're, it's, we're
- Include one small imperfect thought — a hesitation, a side note, a "honestly" or "look" or "here's the thing"
- No corporate buzzwords: leverage, synergy, ecosystem, paradigm, utilize, robust
- Wrap key phrases, important insights, or powerful statements in "double quotes" to make them stand out
- The post should feel like it was written in one sitting, not edited 10 times

{structure_guide}

HASHTAG RULES:
- After the post body, add exactly one blank line
- Then add 5 to 8 relevant hashtags on a single line
- Hashtags must directly relate to the topic "{tag}" and the specific content of the post
- Mix broad hashtags with specific niche ones
- No generic filler hashtags like #Life #Good #Post #Motivation unless they are genuinely relevant

POST REQUIREMENTS:
1) Topic: {tag}
   - Treat this as the user's exact intent. If it's a phrase, a question, or a sentence — honor it fully.
   - Extract the core theme, emotion, and angle from it and build the entire post around that.
   - Do not generalize or water it down. Stay specific to what the user wrote.
2) Length: {length_str}
3) Language: {language}. Write the ENTIRE post in {language}. Do not mix languages unless it is a mixed dialect like Hinglish or Spanglish.
4) Tone: {tone_instruction}

No preamble. No title. Start the post immediately.
'''

    english_family = {"English", "Hinglish (Hindi + English)", "Spanglish (Spanish + English)"}
    if language in english_family:
        examples = few_shot.get_filtered_posts(length, "English", tag)
        if len(examples) > 0:
            prompt += "\nHere are some real human-written posts on this topic. Match their natural voice and rhythm:\n"
        for i, post in enumerate(examples):
            prompt += f'\n--- Example {i+1} ---\n{post["text"]}\n'
            if i == 1:
                break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))
