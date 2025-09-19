from fastapi import FastAPI,Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database  import engine, sessionLOcal
from sqlalchemy.orm import Session



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionLOcal()
    try: 
        yield db

    finally:
        db.close()


@app.post('/blog',status_code=status.HTTP_201_CREATED,response_model=schemas.showBlog,tags=["blog"])
def create_blog(request: schemas.Blog, db:Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog',status_code=status.HTTP_204_NO_CONTENT, tags=["blog"])
def destroy(id,db:Session= Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {'done'}

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,response_model=schemas.showBlog,tags=["blog"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available"
        )
    
    blog.update({'title': request.title, 'body': request.body})
    db.commit()

    return {"message": f"Blog {id} updated successfully"}

    


@app.get('/blog',response_model=schemas.showBlog, status_code=200,tags=["blog"])
def all(db:Session= Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs




@app.post('/user',status_code=200,response_model=schemas.showUser,tags=["user"])
def Create_user(requesst: schemas.User, db:Session= Depends(get_db)):
    new_user  = models.User(name=requesst.name, email=requesst.email, password=hashing.hash_password(requesst.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/user/{id}', status_code=200,response_model=schemas.showUser,tags=["user"])
def get_user(id:int, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                            f"the user with id {id} is not available")
    return user