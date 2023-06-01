from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status

from models import User
from database import get_db

from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user
from domain.question.question_router import router as question_router

router = APIRouter(
    prefix="/api/answer"
)


@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int, _answer_create: answer_schema.AnswerCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create, user=current_user)

    url = question_router.url_path_for(
        "question", question_id=question_id)
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    answer = answer_crud.get_answer(db, answer_id=_answer_update.id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    if answer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    answer_crud.update_answer(db=db, answer_update=_answer_update)


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    if db_answer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    answer_crud.delete_answer(db=db, db_answer=db_answer)


@router.post('/vote', status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote: answer_schema.AnswerVote, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    answer_crud.vote_answer(db=db, db_answer=db_answer, db_user=current_user)
