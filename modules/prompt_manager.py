import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "templates", "prompt_templates.json")

class PromptManager:
    def __init__(self, template_path = DATA_DIR):
        
        with open(template_path, 'r', encoding= 'utf-8') as file:
            self.templates = json.load(file)

    def build_outline_prompt(self, content_type, topic, tone, target_audience):
        
        template = self.templates["outline"][content_type]["prompt"]
        final_prompt = template.format(topic = topic, tone = tone, target_audience = target_audience)

        return final_prompt
    
    def build_draft_prompt(self, content_type, topic, tone, target_audience, outline):
        
        template = self.templates["draft"][content_type]["prompt"]
        final_prompt = template.format(topic = topic, tone = tone, target_audience = target_audience, outline = outline)

        return final_prompt
    
    def build_refinement_prompt(self, content, refinement_type, target_audience):
        
        template = self.templates["refinement"][refinement_type]["prompt"]
        final_prompt = template.format(content = content, target_audience = target_audience)

        return final_prompt
    