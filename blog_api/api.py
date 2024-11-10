from fastapi import FastAPI, Body, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .models import Blog, BlogSummaryForList, BlogFullInfo
from .database_handler import BlogDB, get_database
from datetime import datetime


app = APIRouter()


@app.get('/blogs', response_model=List[BlogSummaryForList])
def get_blogs(db: Session = Depends(get_database)):
    blogs = db.query(BlogDB).with_entities(BlogDB.id, BlogDB.article_title).all()
    return blogs


@app.get('/blogs/{blog_id}')
def get_current_blog(blog_id: int, db: Session = Depends(get_database)):
    blog = db.query(BlogDB).filter(BlogDB.id == blog_id).first()
    return blog


@app.post('/blogs', status_code=status.HTTP_201_CREATED)
def create_blog(data: Blog = Body(), db: Session = Depends(get_database)):
    new_blog = BlogDB(
        article_title=data.article_title,
        publishing_date=datetime.now().date(),
        content=data.content
    )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blogs/{blog_id}', response_model=dict)
def delete_blog(blog_id: int, db: Session = Depends(get_database)):
    del_blog = db.query(BlogDB).filter(BlogDB.id == blog_id).first()
    db.delete(del_blog)
    db.commit()
    return {'message': f"blog with id {del_blog.id} has been deleted!"}


@app.patch('/blogs/{blog_id}', response_model=BlogFullInfo)
def update_blog(blog_id: int, data : Blog = Body(), db: Session = Depends(get_database)):
    blog = db.query(BlogDB).filter(BlogDB.id == blog_id).first()

    blog.article_title = data.article_title or blog.article_title
    blog.content = data.content or blog.content

    db.commit()
    db.refresh(blog)
    return blog

