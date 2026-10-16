from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import LivroModel
from schemas import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.get("", response_model=List[LivroResponse])
def listar_livros_disponiveis(db: Session = Depends(get_db)):
    # Retorna apenas os livros onde disponivel == True
    return db.query(LivroModel).filter(LivroModel.disponivel == True).all()


@router.get("/{id}", response_model=LivroResponse)
def buscar_livro_por_id(id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroModel).filter(LivroModel.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )
    return livro


@router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(livro_data: LivroCreate, db: Session = Depends(get_db)):
    novo_livro = LivroModel(**livro_data.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@router.patch("/{id}", response_model=LivroResponse)
def atualizar_livro(
    id: int, livro_data: LivroUpdate, db: Session = Depends(get_db)
):
    livro = db.query(LivroModel).filter(LivroModel.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )

    dados_atualizacao = livro_data.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizacao.items():
        setattr(livro, chave, valor)

    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def remover_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroModel).filter(LivroModel.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )

    # Soft Delete: altera a disponibilidade para False
    livro.disponivel = False
    db.commit()
    return {"message": f"Livro ID {id} removido com sucesso (soft delete)"}