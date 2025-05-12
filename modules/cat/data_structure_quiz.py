import pandas as pd
import random
from typing import List, Dict, Tuple, Optional, Any

class DataStructureQuiz:
    def __init__(self, excel_path: str = "d:/traeCode/data/data.xlsx"):
        """
        初始化数据结构测验类
        
        Args:
            excel_path: Excel文件路径
        """
        self.excel_path = excel_path
        self.questions = self._load_questions()
        self.current_difficulty = "medium"  # 初始难度为中等
        self.score = 0
        self.total_questions = 20
        self.answered_questions = []
        self.current_question_index = 0
        self.current_difficulty_level = 5  # 初始难度级别为5
        
    def _load_questions(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        从Excel文件加载题目
        
        Returns:
            按难度分类的题目字典
        """
        try:
            df = pd.read_excel(self.excel_path)
            questions = {"easy": [], "medium": [], "hard": []}
            
            # 打印Excel文件中的列名，以便了解实际结构
            print(f"Excel文件中的列名: {df.columns.tolist()}")
            
            # 难度映射：将数字映射到难度级别
            difficulty_map = {1: "easy", 2: "medium", 3: "hard"}
            
            for _, row in df.iterrows():
                try:
                    # 获取难度值并转换为字符串类型的难度级别
                    difficulty_value = row["difficulty"]
                    if isinstance(difficulty_value, int):
                        difficulty = difficulty_map.get(difficulty_value, "medium")
                    else:
                        difficulty = str(difficulty_value).lower()
                    
                    # 尝试使用Excel中的实际列名构建问题
                    question = {
                        "question": row["question"],
                        "options": [row["option_a"], row["option_b"], row["option_c"], row["option_d"]],
                        "correct_answer": row["correct_answer"],
                        "difficulty": difficulty,
                        "bloom_level": row["bloom_level"]
                    }
                    
                    if difficulty in questions:
                        questions[difficulty].append(question)
                    else:
                        # 如果难度不在预定义的类别中，默认为中等难度
                        questions["medium"].append(question)
                except KeyError as e:
                    print(f"警告: 行 {_+1} 缺少列 {e}，跳过此题目")
            
            # 打印每个难度级别的题目数量
            for difficulty, qs in questions.items():
                print(f"{difficulty} 难度题目数量: {len(qs)}")
                
            return questions
        except Exception as e:
            print(f"加载题目时出错: {e}")
            import traceback
            traceback.print_exc()
            return {"easy": [], "medium": [], "hard": []}
    
    def get_next_question(self) -> Optional[Dict[str, Any]]:
        """
        获取下一个问题
        
        Returns:
            问题字典或None（如果没有更多问题）
        """
        if self.current_question_index >= self.total_questions:
            return None
        
        # 从当前难度级别中选择一个未回答过的问题
        available_questions = [q for q in self.questions[self.current_difficulty] 
                              if q not in self.answered_questions]
        
        # 如果当前难度没有可用问题，尝试其他难度
        if not available_questions:
            if self.current_difficulty == "easy":
                available_questions = [q for q in self.questions["medium"] 
                                      if q not in self.answered_questions]
            elif self.current_difficulty == "medium":
                # 先尝试简单题，再尝试困难题
                available_questions = [q for q in self.questions["easy"] 
                                      if q not in self.answered_questions]
                if not available_questions:
                    available_questions = [q for q in self.questions["hard"] 
                                          if q not in self.answered_questions]
            else:  # hard
                available_questions = [q for q in self.questions["medium"] 
                                      if q not in self.answered_questions]
        
        # 如果仍然没有可用问题，从所有未回答的问题中选择
        if not available_questions:
            all_questions = []
            for difficulty in ["easy", "medium", "hard"]:
                all_questions.extend([q for q in self.questions[difficulty] 
                                     if q not in self.answered_questions])
            
            if all_questions:
                available_questions = all_questions
            else:
                # 如果所有问题都已回答，重置已回答问题列表
                self.answered_questions = []
                for difficulty in ["easy", "medium", "hard"]:
                    available_questions.extend(self.questions[difficulty])
        
        if available_questions:
            question = random.choice(available_questions)
            self.answered_questions.append(question)
            self.current_question_index += 1
            return question
        
        return None
    
    def answer_question(self, answer: str, question: Dict[str, Any]) -> bool:
        """
        回答问题并调整难度 - 采用计算机自适应测试(CAT)方式
        
        Args:
            answer: 用户的答案
            question: 当前问题
            
        Returns:
            答案是否正确
        """
        is_correct = answer.lower() == question["correct_answer"].lower()
        
        # 根据回答调整难度
        if is_correct:
            self.score += 5
            # 如果答对了，根据当前难度级别增加难度
            if self.current_difficulty_level < 10:
                # 难度越高，增加的幅度越小，体现CAT特性
                if self.current_difficulty_level >= 8:
                    self.current_difficulty_level += 1  # 高难度区间增加1级
                else:
                    self.current_difficulty_level += 2  # 中低难度区间增加2级
                    
                # 确保不超过最大难度
                self.current_difficulty_level = min(10, self.current_difficulty_level)
        else:
            # 如果答错了，根据当前难度级别降低难度
            if self.current_difficulty_level > 1:
                # 难度越低，减少的幅度越小，体现CAT特性
                if self.current_difficulty_level <= 3:
                    self.current_difficulty_level -= 1  # 低难度区间减少1级
                else:
                    self.current_difficulty_level -= 2  # 中高难度区间减少2级
                    
                # 确保不低于最小难度
                self.current_difficulty_level = max(1, self.current_difficulty_level)
        
        # 根据新的难度级别更新当前难度类别
        if self.current_difficulty_level <= 3:
            self.current_difficulty = "easy"
        elif self.current_difficulty_level <= 7:
            self.current_difficulty = "medium"
        else:
            self.current_difficulty = "hard"
        
        return is_correct
    
    def get_final_result(self) -> Tuple[int, str]:
        """
        获取最终测试结果
        
        Returns:
            总分和测试者的Bloom分类级别
        """
        bloom_levels = {}
        
        for question in self.answered_questions:
            bloom_level = question["bloom_level"]
            if bloom_level in bloom_levels:
                bloom_levels[bloom_level] += 1
            else:
                bloom_levels[bloom_level] = 1
        
        # 确定测试者属于哪一类Bloom级别（选择出现次数最多的级别）
        dominant_bloom_level = None
        max_count = 0
        
        for level, count in bloom_levels.items():
            if count > max_count:
                max_count = count
                dominant_bloom_level = level
        
        return self.score, dominant_bloom_level

def run_quiz() -> None:
    """
    运行数据结构测验
    """
    quiz = DataStructureQuiz()
    
    print("欢迎参加数据结构测验！")
    print("本测验共20道题目，每题5分，满分100分。")
    print("测验采用计算机自适应测试(CAT)方式，难度会根据您的回答动态调整。")
    print("请输入选项字母(A/B/C/D)作为您的答案。\n")
    
    # 难度映射：将文本难度转换为1-10的数值
    difficulty_to_number = {
        "easy": lambda: random.randint(1, 3),      # 简单题目对应1-3
        "medium": lambda: random.randint(4, 7),    # 中等题目对应4-7
        "hard": lambda: random.randint(8, 10)      # 困难题目对应8-10
    }
    
    question_num = 1
    while True:
        question = quiz.get_next_question()
        if not question:
            break
        
        # 获取难度的数值表示
        difficulty_level = difficulty_to_number.get(question['difficulty'], lambda: 5)()
        
        # 显示题目信息，包括1-10的难度标注
        print(f"\n问题 {question_num}/{quiz.total_questions}:")
        print(f"[难度: {difficulty_level}] {question['question']}")
        
        for i, option in enumerate(question["options"]):
            print(f"{chr(65+i)}. {option}")
        
        while True:
            answer = input("\n您的答案是: ").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                break
            else:
                print("无效输入，请输入A、B、C或D。")
        
        is_correct = quiz.answer_question(answer, question)
        
        if is_correct:
            print("回答正确！")
        else:
            print(f"回答错误。正确答案是: {question['correct_answer']}")
        
        question_num += 1
    
    score, dominant_bloom_level = quiz.get_final_result()
    
    print("\n测验结束！")
    print(f"您的总分是: {score}")
    print(f"根据您的答题情况，您属于Bloom分类级别: {dominant_bloom_level}")

if __name__ == "__main__":
    run_quiz()