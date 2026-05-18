from agent import ShortStoryAgent

def print_menu():
    print("\n=== 短篇小说创作助手 ===")
    print("1. 生成新故事")
    print("2. 修改故事")
    print("3. 扩写故事")
    print("4. 精简故事")
    print("5. 更换结局")
    print("6. 切换视角")
    print("7. 调整文风")
    print("8. 退出")
    print("==========================")

def get_story_inputs():
    inputs = {}
    print("\n请输入故事创作参数（按回车跳过可选参数）：")
    inputs['genre'] = input("题材（悬疑/治愈/都市/奇幻/古风/校园/暗黑/温情/科幻/现实向）：")
    inputs['style'] = input("文风（文艺/直白/口语/细腻/冷峻等）：")
    inputs['perspective'] = input("叙事视角（第一人称/第三人称）：")
    inputs['characters'] = input("人物设定：")
    inputs['plot'] = input("核心剧情：")
    inputs['ending'] = input("结局要求：")
    inputs['word_count'] = input("目标字数（500-3000）：")
    return inputs

def main():
    agent = ShortStoryAgent()
    current_story = ""
    
    while True:
        print_menu()
        choice = input("请选择操作（1-8）：")
        
        try:
            if choice == '1':
                inputs = get_story_inputs()
                print("\n正在生成故事...")
                current_story = agent.generate_story(**inputs)
                print("\n" + "="*50)
                print(current_story)
                print("="*50)
                
            elif choice == '2':
                if not current_story:
                    print("请先生成一个故事！")
                    continue
                instruction = input("请输入修改要求：")
                current_story = agent.refine_story(current_story, instruction)
                print("\n修改完成：")
                print("="*50)
                print(current_story)
                print("="*50)
                
            elif choice == '3':
                if not current_story:
                    print("请先生成一个故事！")
                    continue
                target = input("目标字数：")
                current_story = agent.expand_story(current_story, target)
                print("\n扩写完成：")
                print("="*50)
                print(current_story)
                print("="*50)
                
            elif choice == '4':
                if not current_story:
                    print("请先生成一个故事！")
                    continue
                target = input("目标字数：")
                current_story = agent.shorten_story(current_story, target)
                print("\n精简完成：")
                print("="*50)
                print(current_story)
                print("="*50)
                
            elif choice == '5':
                if not current_story:
                    print("请先生成一个故事！")
                    continue
                ending = input("新结局要求：")
                current_story = agent.change_ending(current_story, ending)
                print("\n结局已修改：")
                print("="*50)
                print(current_story)
                print("="*50)
                
            elif choice == '6':
                if not current_story:
                    print("请先生成一个故事！")
                    continue
                perspective = input("新视角（第一人称/第三人称）：")
                current_story = agent.change_perspective(current_story, perspective)
                print("\n视角已切换：")
                print("="*50)
                print(current_story)
                print("="*50)
                
            elif choice == '7':
                if not current_story:
                    print("请先生成一个故事！")
                    continue
                style = input("新文风：")
                current_story = agent.change_style(current_story, style)
                print("\n文风已调整：")
                print("="*50)
                print(current_story)
                print("="*50)
                
            elif choice == '8':
                print("感谢使用短篇小说创作助手！")
                break
                
            else:
                print("无效选择，请输入1-8之间的数字")
                
        except Exception as e:
            print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    main()
