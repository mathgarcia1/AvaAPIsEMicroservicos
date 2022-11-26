from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

app = FastAPI();

def ultimoDaFila():
    ClienteAux = None
    for Cliente in dbclientes:
        if (Cliente.Atendido) == False:
            ClienteAux = Cliente
    return ClienteAux.posicao

#modelo do objeto
class Cliente(BaseModel):
    id: Optional[int] = 0
    nome: str = Field(..., max_length = 20)
    tipoAtendimento: str = Field(..., max_lenght = 1)
    posicao: int
    dataEntrada: Optional[datetime] = datetime.now()
    Atendido: Optional[bool] = False

#carregando bd
dbclientes = [
    Cliente(id=1, nome="Matheus", tipoAtendimento="P", posicao=1,dataEntrada=datetime.now()),
    Cliente(id=2, nome="Jorge", tipoAtendimento="P", posicao=2,dataEntrada=datetime.now()),
    Cliente(id=3, nome="Bianca", tipoAtendimento="N", posicao=3,dataEntrada=datetime.now())
]


@app.get("/fila")
async def getfila():
    Clientes = [Cliente for Cliente in dbclientes if Cliente.Atendido == False]
    if len(Clientes) == 0:
        return {"Fila": ""}
    else:
        return {"Fila": Clientes}

@app.get("/fila/{id}")
async def getfilabyid(id: int, response: Response):
    # else raise HTTPException(status_code=404, detail="Pessoa nao encontrada") 
    Clientes = [Cliente for Cliente in dbclientes if Cliente.id==id]
    if len(Clientes) > 0:
        return {"Fila": Clientes}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Fila": f"Cliente com id={id} não encontrado na fila"}

@app.post("/fila", status_code=status.HTTP_201_CREATED)
async def addcliente(cliente: Cliente, response: Response):
    if (cliente.tipoAtendimento == "P" or cliente.tipoAtendimento == "N") == False:
        response.status_code = 400
        return {"Tipo de atendimento pode ser apenas Prioritario(P) e Não Prioritario(N)"} 
    ultimo = ultimoDaFila()
    cliente.id = dbclientes[-1].id + 1
    cliente.posicao = ultimo + 1
    cliente.dataEntrada = datetime.now()
    dbclientes.append(cliente)
    return {"Fila": f"Cliente entrou na fila na posição {cliente.posicao}"}

@app.put("/fila")
async def updatefila():
    for Cliente in dbclientes:
        if Cliente.posicao == 1:
            Cliente.Atendido = True
            Cliente.posicao = 0
        else:
            Cliente.posicao = Cliente.posicao - 1
    return {"Fila": "Atualizada"}

@app.delete("/fila/{id}")
async def deletefilabyclienteid(id: int, response: Response):
    # else raise HTTPException(status_code=404, detail="Pessoa nao encontrada")     
    Clientes = [Cliente for Cliente in dbclientes if Cliente.id==id]
    if len(Clientes) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Fila": f"Cliente com id={id} não encontrado na fila"}
    dbclientes.remove(Cliente[0])
    return {"Fila": f"Cliente com id={id} foi removido"}
    