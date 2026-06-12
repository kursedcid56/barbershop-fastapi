from  .. import models, schemas, utils, oauth2
from ..utils import hash_password
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import  SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List
import ollama
router = APIRouter(
    prefix="/services",
    tags=['Service']
)

@router.get("/", response_model=List[schemas.ServiceOut])
def root(db:Session = Depends(get_db)):
    service = db.query(models.Service).all()
    return service

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ServiceBase)
def create_service(service: schemas.ServiceCreate, db:Session = Depends(get_db), 
                   current_user: models.User = Depends(oauth2.allow_admin_only)):
    new_service = models.Service(**service.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service

@router.get("/{id}", response_model=schemas.ServiceResponse)
def get_service(id: int, db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.allow_all)):
    service = db.query(models.Service).filter(models.Service.id == id).first()
    if service == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"service with id: {id} does not exist")
    return service

@router.put("/{id}",response_model=schemas.ServiceResponse)
def update_service(id: int,service: schemas.ServiceUpdate ,db: Session = Depends(get_db), 
                   current_user: models.User = Depends(oauth2.allow_admin_only)):
    service_query = db.query(models.Service).filter(models.Service.id == id)

    service_in_db = service_query.first()
    if service_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service whith id: {id} does not exist")
    service_query.update(service.model_dump(), synchronize_session = False)

    db.commit()
    return service_query.first()
@router.delete("/{id}")
def delete_service(id: int,db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.allow_admin_only)):
    deleted_service = db.query(models.Service).filter(models.Service.id == id)

    service_in_db = deleted_service.first()
    if service_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service with id:{id} does not exist")
    deleted_service.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/consult", response_model=schemas.ConsultOut)
def consult_haircut(
    input_data:schemas.ConsultRequest,
    db:Session = Depends(get_db)):
    service_in_db = db.query(models.Service).all()

    menu_text = ""
    for service in service_in_db:
        menu_text += f"Gói:{service.name} | Giá:{service.price}đ | Thời gian:{service.duration_minutes} phút. \n"
    prompt = f"""
    Mày là một anh thợ cắt tóc Barber có 10 năm kinh nghiệm, cực kỳ sành điệu và thân thiện.
    Hãy xưng hô với khách là 'bro' hoặc 'anh' và gọi mình là 'em' hoặc 'tiệm'.

    Đây là danh sách các gói dịch vụ ĐANG CÓ THỰC TẾ tại tiệm của em:
    {menu_text}

    Khách hàng bước vào tiệm và hỏi câu này: "{input_data.question}"

    Nhiệm vụ của mày:
    1. Dựa vào danh sách dịch vụ trên, hãy tư vấn và gợi ý cho khách gói dịch vụ phù hợp nhất với câu hỏi của họ.
    2. Tuyệt đối KHÔNG ĐƯỢC tự bịa ra dịch vụ nào khác ngoài danh sách trên.
    3. Trả lời ngắn gọn, chất chơi, thuyết phục khách chốt lịch.
    """    
    try:
        response = ollama.generate(model="llama3.2:1b", prompt=prompt)
        AI_advice = response.get("response", "")
        return {"advice":{AI_advice}}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống: {str(e)}"

        )




