from fastapi import APIRouter, HTTPException, Depends, Request, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uuid
import logging
from src.modules.cat.data_structure_quiz import DataStructureQuiz

router = APIRouter(
    prefix="/quiz",
    tags=["计算机自适应测试"],
    responses={404: {"description": "Not found"}}
)

# 存储用户会话
quiz_sessions = {}


class AnswerRequest(BaseModel):
    answer: str
    session_id: str


class QuizResponse(BaseModel):
    question: str
    options: List[str]
    question_number: int
    total_questions: int
    difficulty_level: int
    session_id: str


class ResultResponse(BaseModel):
    is_correct: bool
    correct_answer: Optional[str] = None
    message: str
    next_question: Optional[QuizResponse] = None
    is_completed: bool = False
    score: Optional[int] = None
    bloom_level: Optional[str] = None


@router.post("/start")
async def start_quiz(
        request: Request,
        logger: logging.Logger,
        requestId: str = Header(None, alias="requestId")
):
    """开始一个新的测验会话"""
    try:
        # 记录请求信息
        headers = request.headers
        logger.info("Request ID: %s, 开始新测验会话, 请求头信息:\n%s", requestId or "unknown", headers)

        # 创建测验对象
        quiz = DataStructureQuiz()
        session_id = str(uuid.uuid4())

        # 获取第一个问题
        question = quiz.get_next_question()

        if question is None:
            logger.error("Request ID: %s, 无法获取题目，请检查题库", requestId or "unknown")
            raise HTTPException(status_code=500, detail="无法获取题目，请检查题库")

        quiz_sessions[session_id] = {
            "quiz": quiz,
            "current_question": question,
            "question_num": 1
        }

        response = QuizResponse(
            question=question["question"],
            options=question["options"],
            question_number=1,
            total_questions=quiz.total_questions,
            difficulty_level=quiz.current_difficulty_level,
            session_id=session_id
        )

        logger.info("Request ID: %s, 测验会话已创建, session_id: %s, 第一题: %s",
                    requestId or "unknown", session_id, question["question"])

        return response
    except Exception as e:
        logger.error("Request ID: %s, 创建测验会话失败: %s", requestId or "unknown", str(e))
        import traceback
        logger.error("详细错误: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"创建测验会话失败: {str(e)}")


@router.post("/answer", response_model=ResultResponse)
async def submit_answer(
        request: Request,
        req_body: AnswerRequest,
        logger: logging.Logger,
        requestId: str = Header(None, alias="requestId")
):
    """提交答案并获取下一个问题"""
    try:
        # 记录请求信息
        logger.info("Request ID: %s, 提交答案请求, session_id: %s, answer: %s",
                    requestId or "unknown", req_body.session_id, req_body.answer)

        session_id = req_body.session_id
        if session_id not in quiz_sessions:
            logger.warning("Request ID: %s, 会话不存在: %s", requestId or "unknown", session_id)
            raise HTTPException(status_code=404, detail="会话不存在，请重新开始测验")

        session = quiz_sessions[session_id]
        quiz = session["quiz"]
        current_question = session["current_question"]

        # 验证和处理答案
        answer = req_body.answer.strip().upper()
        is_correct = quiz.answer_question(answer, current_question)
        logger.info("Request ID: %s, 回答%s, 问题: %s",
                    requestId or "unknown", "正确" if is_correct else "错误", current_question["question"])

        # 获取下一个问题
        next_question = quiz.get_next_question()
        session["current_question"] = next_question
        session["question_num"] += 1

        # 检查测验是否完成
        is_completed = next_question is None

        result = ResultResponse(
            is_correct=is_correct,
            correct_answer=current_question["correct_answer"],
            message="回答正确！" if is_correct else "回答错误。",
            is_completed=is_completed
        )

        if is_completed:
            # 测验结束，返回最终结果
            score, bloom_level = quiz.get_final_result()
            result.score = score
            result.bloom_level = bloom_level
            logger.info("Request ID: %s, 测验完成, session_id: %s, 得分: %s, Bloom等级: %s",
                        requestId or "unknown", session_id, score, bloom_level)
            # 清理会话
            quiz_sessions.pop(session_id, None)
        else:
            # 返回下一个问题
            result.next_question = QuizResponse(
                question=next_question["question"],
                options=next_question["options"],
                question_number=session["question_num"],
                total_questions=quiz.total_questions,
                difficulty_level=quiz.current_difficulty_level,
                session_id=session_id
            )
            logger.info("Request ID: %s, 提供下一题, 问题编号: %s, 难度: %s",
                        requestId or "unknown", session["question_num"], quiz.current_difficulty_level)

        return result

    except HTTPException:
        # 直接重新抛出HTTP异常
        raise
    except Exception as e:
        logger.error("Request ID: %s, 处理答案时发生错误: %s", requestId or "unknown", str(e))
        import traceback
        logger.error("详细错误: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"处理答案时发生错误: {str(e)}")
