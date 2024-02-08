from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import get_db
from app.example_module.apis import router as example_router

app = FastAPI(
    title="Heavyweight(FastAPI)",
    docs_url="/",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}, # Hides Schemas Menu in DocsF
)

# Variables
origins = ["*"]

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check
@app.get("/health", status_code=200, include_in_schema=False)
def health_check(db=Depends(get_db)):
    """This is the health check endpoint"""
    return {"status": "ok"}
# Rota para receber o JSON via método POST
@app.post("/api_financiamento")
async def receber_json(dados_json: dict):
    print(f'Dados recebidos: {dados_json}')
    data = dados_json
    # identificar a proposta que foi enviada para adicionar ao array de buffer
    numero_proposta = data.get('numero_proposta', 'Proposta não especificada')
    Handler.buffer.append(numero_proposta)

    # Semafaro para limitar processos simultaneos na API
    with semaphore:
        status_santander = None
        status_btg = None
        status_bv = None
        # Seção crítica: Apenas 2 threads podem entrar aqui simultaneamente
        instances_running = semaphore._value
        cpf = data.get('cpf', 'CPF não especificado')
        valor_proposta = data.get('valor_proposta', 'Valor não especificado')
        print(f'Buffer: {Handler.buffer}')

        print(
            f'\x1b[31m>>> NOVA CHAMADA DE API RECEBIDA <<<<\x1b[32m\n\n    vagas disponíveis no buffer: {instances_running} \n\n'
            f'Proposta recebida: \x1b[31m{numero_proposta}\x1b[32m\n'
            f'CPF: \x1b[31m{cpf}\x1b[32m\n'
            f'Valor da Proposta: \x1b[31m R$ {valor_proposta}\x1b[32m\n'
        )
        # Chama a função para verificar a disponibilidade do ChromeDriver
        # check_chromedriver_availability()
        
        # Chama a função para verificar a instalação do Chrome
        check_chrome_installation()
        # driver = abrir_navegador()    

        return {"mensagem": "JSON recebido com sucesso", "dados": dados_json}

# Routers
app.include_router(example_router, prefix="/example", tags=["Example Docs"])
app.include_router(api_financiamento, prefix="/api_financiamento", tags=["API Financiamento"])
app.include_router(health, prefix="/health", tags=["health"])

if __name__ == "__main__":
    # Executa o aplicativo usando o servidor Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
