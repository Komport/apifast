from main import new_blog
from fastapi import FastAPI,Depends, status,Response, HTTPException
from sqlalchemy.orm.session import Session
from . import schemas,models
from .database import SessionLocal, engine



app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/create')
def create_blog(response: schemas.Blog,db: Session = Depends(get_db)):
    new_blog = models.Blog(title=response.title, body = response.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get('/getblog/{id}', status_code=status.HTTP_200_OK)
def get_blog_byid(response: Response,id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail={'data':f'Blog post with id {id} not found'})
        #response.status_code = status.HTTP_404_NOT_FOUND
        return {'data':f'Blog post with id {id} not found'}
    return blog

@app.get('/getblog')
def get_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.delete('/delete/{id}')
def delete_blog(response: Response, id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).delete()
    db.commit()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":f"Record with id {id} not found"}
    return {"data":f"Record with id {id} deleted"}

@app.put('/update/{id}')
def update_blog_byid(request: schemas.Blog, id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).update(request)
    db.commit()

    return {'response':'update ok'}