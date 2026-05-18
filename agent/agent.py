from llm_client import LLMClient

class ShortStoryAgent:
    def __init__(self):
        self.client = LLMClient()
    
    def build_prompt(self, **kwargs):
        parts = []
        
        if 'genre' in kwargs and kwargs['genre']:
            parts.append(f"题材：{kwargs['genre']}")
        
        if 'style' in kwargs and kwargs['style']:
            parts.append(f"文风：{kwargs['style']}")
        
        if 'perspective' in kwargs and kwargs['perspective']:
            parts.append(f"叙事视角：{kwargs['perspective']}")
        
        if 'characters' in kwargs and kwargs['characters']:
            parts.append(f"人物设定：{kwargs['characters']}")
        
        if 'plot' in kwargs and kwargs['plot']:
            parts.append(f"核心剧情：{kwargs['plot']}")
        
        if 'ending' in kwargs and kwargs['ending']:
            parts.append(f"结局要求：{kwargs['ending']}")
        
        if 'word_count' in kwargs and kwargs['word_count']:
            parts.append(f"字数：{kwargs['word_count']}字")
        
        if parts:
            prompt = "请根据以下要求创作一篇短篇小说：\n" + "\n".join(parts)
        else:
            prompt = "请创作一篇短篇小说"
        
        return prompt + "\n\n直接输出故事正文，无需开场白。"
    
    def generate_story(self, **kwargs):
        prompt = self.build_prompt(**kwargs)
        return self.client.generate(prompt)
    
    def refine_story(self, original_story, instruction):
        prompt = f"以下是一篇短篇小说，请按照要求进行修改：\n\n{original_story}\n\n修改要求：{instruction}"
        return self.client.generate(prompt)
    
    def expand_story(self, original_story, target_length):
        instruction = f"请将这篇小说扩写到约{target_length}字，保持故事完整性和连贯性。"
        return self.refine_story(original_story, instruction)
    
    def shorten_story(self, original_story, target_length):
        instruction = f"请将这篇小说精简到约{target_length}字，保留核心情节和人物。"
        return self.refine_story(original_story, instruction)
    
    def change_ending(self, original_story, new_ending):
        instruction = f"请修改这篇小说的结局，新结局要求：{new_ending}"
        return self.refine_story(original_story, instruction)
    
    def change_perspective(self, original_story, new_perspective):
        instruction = f"请将这篇小说的叙事视角改为{new_perspective}"
        return self.refine_story(original_story, instruction)
    
    def change_style(self, original_story, new_style):
        instruction = f"请将这篇小说的文风改为{new_style}"
        return self.refine_story(original_story, instruction)
