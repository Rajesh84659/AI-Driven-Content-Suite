from datetime import datetime
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

prompts_folder = os.path.join(DATA_DIR, "prompts")
outputs_folder = os.path.join(DATA_DIR, "outputs")
evaluations_folder = os.path.join(DATA_DIR, "evaluations")

def generate_metadata(base_folder, action, file_prefix):

    #Actual Folder to save
    actual_folder = os.path.join(base_folder, action)

    # Create folder
    os.makedirs(actual_folder, exist_ok=True)

    # Current date
    today = datetime.now().strftime("%Y%m%d")

    # Store all serial numbers
    numbers = []

    # Read all files
    for file in os.listdir(actual_folder):

        match = re.search(
            rf"{file_prefix}_{today}_(\d+)\.json",
            file
        )
        if match:
            numbers.append(int(match.group(1)))

    # Generate next number
    next_num = max(numbers, default=0) + 1

    # Filename
    filename = f"{file_prefix}_{today}_{next_num:03d}.json"

    # Full filepath
    filepath = os.path.join(actual_folder, filename)

    # Unique ID
    unique_id = f"{action.upper()}_{file_prefix.upper()}_{today}_{next_num:03d}"

    # Version
    version = f"v{1:03d}"

    return filepath, unique_id, version

def increment_version(version):

    try:
        num = int(version[1:])
        return f"v{num + 1:03d}"

    except:
        return "v001"

def save_prompt(action, content_type, topic, tone, target_audience, prompt):
    filepath, prompt_id, prompt_version = generate_metadata(prompts_folder, action, "prompt")

    # Insert data into Dictionary
    data = {
        "id" : prompt_id,
        "action" : action,
        "content_type" : content_type,
        "topic" : topic,
        "tone" : tone,
        "target_audience" : target_audience,
        "prompt_version" : prompt_version,
        "prompt" : prompt,
        "timestamp" : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    # Dump as JSON into dedicated file
    with open(filepath, 'w')  as f:
        json.dump(data, f, indent=4)

    #print("Prompt saved")

    return prompt_id

def save_output( action, parent_prompt_id, topic, content):
    filepath, output_id, output_version = generate_metadata(outputs_folder, action, "output")

    # Insert data into Dictionary
    data = {
        "id" : output_id,
        "parent_prompt_id" : parent_prompt_id,
        "action" : action,
        "output_version" : output_version,
        "topic" : topic,
        "content" : content,
        "timestamp" : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    # Dump as JSON into dedicated file
    with open(filepath, 'w')  as f:
        json.dump(data, f, indent=4)

    #print("Output Saved")

    return output_id, output_version

def save_refine_prompt(action, output_draft_id, refinement_type, prompt, output_draft_version):
    filepath, refinement_id, wrong_version = generate_metadata(prompts_folder, action, "prompt")
    refinement_version = increment_version(output_draft_version)

    data = {
        "id" : refinement_id,
        "parent_output_id" : output_draft_id,
        "action" : action,
        "refinement_type" : refinement_type,
        "prompt" : prompt,
        "version" : refinement_version,
        "timestamp" : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    # Dump as JSON into dedicated file
    with open(filepath, 'w')  as f:
        json.dump(data, f, indent=4)

    #print("Refinement Prompt Saved")

    return refinement_id, refinement_version

def save_refine_output(action, parent_prompt_id, topic, refinement_type, content, refine_prompt_version):
    filepath, refinement_id, wrong_version = generate_metadata(outputs_folder, action, "output")

    data = {
        "id" : refinement_id,
        "parent_prompt_id" :  parent_prompt_id,
        "action" : action,
        "topic" : topic,
        "refinement_type" : refinement_type,
        "content" : content,
        "version" : refine_prompt_version,
        "timestamp" : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    # Dump as JSON into dedicated file
    with open(filepath, 'w')  as f:
        json.dump(data, f, indent=4)

    #print("Refinement Output Saved")

# Create Evaluations Folder automatically
os.makedirs(evaluations_folder, exist_ok=True)

def generate_evaluation_id():

    files = os.listdir(evaluations_folder)
    count = len(files) + 1

    return f"eval_{count:03d}"

def save_evaluation(related_output_id, evaluation_data):

    # generate unique evaluation id
    evaluation_id = generate_evaluation_id()

    # final evaluation structure
    final_report = {
        "evaluation_id": evaluation_id,
        "related_output_id": related_output_id,
        "word_count": evaluation_data.get("word_count", 0),
        "readability": evaluation_data.get("readability", 0),
        "sentiment": evaluation_data.get("sentiment", "Neutral"),
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    file_name = f"{evaluation_id}.json"
    file_path = os.path.join(evaluations_folder, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(final_report, file, indent=4, ensure_ascii=False)

    return evaluation_id


# Testing the Methods
"""
prompt_id = save_prompt("draft", "There should be Content", " Topic is Selected", "Sweet tone", "Worst audience", "explain about Prompt Engineering...")
output_id, output_version = save_output("draft", prompt_id, " Topic is Selected", "The Prompt Engineering is nothing but English....")

refine_prompt_id, refine_prompt_version = save_refine_prompt("refinement", output_id, "Friendly type", "explain about Prompt Engineering...", output_version)
save_refine_output("refinement", refine_prompt_id, "No Topic is Selected", "Friendly type", "English is nothing but Prompt Engineering...", refine_prompt_version)
"""
"""
data = {
    "word_count": 576,
    "readability": "85%",
    "sentiment": "Neutral",
    "timestamp": "29-05-2026 11:46:53"
}
save_evaluation("8465", data)
"""