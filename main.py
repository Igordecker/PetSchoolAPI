import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API de tutor e pets — Projeto Integrador II")


@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o banco de dados."},
    )


def representar_tutor(tutor):
    return {
        "cod_tutor": tutor["cod_tutor"],
        "nome": tutor["nome"],
        "cpf": tutor["cpf"],
        "telefone": tutor["telefone"],
        "observacao": tutor["observacao"],
        "data_de_nascimento": tutor["data_de_nascimento"],
        "cep": tutor["cep"],
        "rua": tutor["rua"],
        "bairro": tutor["bairro"],
        "cidade": tutor["cidade"],
        "uf": tutor["uf"]
    }
@app.get("/tutores")
def listar_tutores():
    sql = "SELECT cod_tutor, nome, cpf, telefone, observacao, data_de_nascimento, cep, rua, bairro, cidade, uf FROM tutores ORDER BY cod_tutor"
    tutores = executar_sql(sql)

    return {
        "dados": [representar_tutor(tutor) for tutor in tutores],
        "didatica": {"sql": sql, "parametros": []},
    }

@app.get("/tutores/{cod_tutor}")
def consultar_tutor(cod_tutor: int = Path(gt=0)):
    sql = "SELECT cod_tutor, nome, cpf, telefone, observacao, data_de_nascimento, cep, rua, bairro, cidade, uf FROM tutores WHERE cod_tutor = %s"
    parametros = (cod_tutor,)
    tutores = executar_sql(sql, parametros)

    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")

    return {
        "dados": representar_tutor(tutores[0]),
        "didatica": {"sql": sql, "parametros": list(parametros)},
    }

def representar_pet(pet):
    return {
        "cod_pet": pet["cod_pet"],
        "nome": pet["nome"],
        "especie": pet["especie"],
        "cod_tutor": pet["cod_tutor"],
    }
@app.get("/pets")
def listar_pets():
    sql = "SELECT cod_pet, nome, especie, cod_tutor FROM pets ORDER BY cod_pet"
    pets = executar_sql(sql)

    return {
        "dados": [representar_pet(pet) for pet in pets],
        "didatica": {"sql": sql, "parametros": []},
    }

@app.get("/pets/{cod_pet}")
def consultar_pet(cod_pet: int = Path(gt=0)):
    sql = "SELECT cod_pet, nome , especie, cod_tutor FROM pets WHERE cod_pet = %s"
    parametros = (cod_pet,)
    pets = executar_sql(sql, parametros)

    if not pets:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    return {
        "dados": representar_pet(pets[0]),
        "didatica": {"sql": sql, "parametros": list(parametros)},
    }
