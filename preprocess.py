import json
import regex as re
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []
        for post in posts:
            sanitized_post_text = post['text'].encode('utf-8', 'replace').decode('utf-8')
            metadata = extract_metadata(sanitized_post_text)
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    if processed_file_path:
        with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
            json.dump(enriched_posts, outfile, indent=4)


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English 
    5. Provide relevant Hashtags

    Here is the actual post on which you need to perform this task:  
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"post": post})

    # Extract JSON using regex
    match = re.search(r'\{(?:[^{}]|(?R))*\}', response.content)

    try:
        json_string = match.group(0) if match else response.content
        json_parser = JsonOutputParser()
        res = json_parser.parse(json_string)
    except (OutputParserException, json.JSONDecodeError, AttributeError):
        raise OutputParserException(f"Invalid JSON output: {response.content}")

    return res


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)

    template = '''
    I will give you a list of tags. You need to unify them with the following rules:
    1. Merge similar tags into a single tag (e.g. "Jobseekers", "Job Hunting" → "Job Search").
    2. Use Title Case for unified tags.
    3. Return a valid JSON object with mappings: original → unified.
       For example: {{"Jobseekers": "Job Search", "Job Hunting": "Job Search"}}
    4. No explanation, no preamble.
    5. Provide relevant Hashtags

    Here is the list of tags:
    {tags}
    '''.replace("{", "{{").replace("}", "}}")  # Escape for PromptTemplate

    # Unescape actual {tags} placeholder
    template = template.replace("{{tags}}", "{tags}")

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"tags": unique_tags_list})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except (OutputParserException, json.JSONDecodeError):
        raise OutputParserException("Unable to parse unified tags.")

    return res


if __name__ == "__main__":
    process_posts('raw_posts.json', 'processed_posts.json')
    print(process_posts)
