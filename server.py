"""
Servidor API local para conectar o App Gestão de Relatórios ao PostgreSQL.
Instalação das dependências:
    pip install fastapi uvicorn psycopg2-binary pydantic
Execução:
    python server.py
    ou
    uvicorn server:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

# 1. Cria a instância do FastAPI primeiro
app = FastAPI(title="API Gestão de Relatórios - PostgreSQL Local")

# 2. Habilita CORS para requisições do frontend local ou remoto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de conexão com o banco
DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE", "congregacao_db"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "4862"),  # Substitua pela sua senha real do PostgreSQL se for diferente
    "host": os.getenv("PGHOST", "localhost"),
    "port": int(os.getenv("PGPORT", "5432")),
}

def decode_pg_error(e: Exception) -> str:
    """Decodifica com segurança qualquer erro vindo do PostgreSQL/Windows evitando quebra por cp1252/utf-8."""
    try:
        # Se for string comum
        return str(e)
    except UnicodeDecodeError:
        try:
            # Tenta decodificar a mensagem binária bruta usando cp1252 (padrão Windows PT-BR)
            if hasattr(e, 'args') and e.args:
                raw_bytes = e.args[0]
                if isinstance(raw_bytes, bytes):
                    return raw_bytes.decode('cp1252', errors='replace')
                return str(raw_bytes).encode('latin1', errors='replace').decode('cp1252', errors='replace')
        except Exception:
            pass
        return "Falha de autenticação ou conexão com o PostgreSQL (verifique usuário, senha e se o banco 'congregacao_db' existe)."

@contextmanager
def get_db():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        conn.set_client_encoding('UTF8')
        yield conn
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        err_msg = decode_pg_error(e)
        print(f"[ERRO POSTGRESQL]: {err_msg}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {err_msg}")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def init_db():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # 1. Tabela de Grupos
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS grupos (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL UNIQUE,
                        overseer VARCHAR(255) DEFAULT '',
                        assistant VARCHAR(255) DEFAULT '',
                        meeting_place VARCHAR(255) DEFAULT '',
                        active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    INSERT INTO grupos (name) VALUES
                        ('Grupo 1'), ('Grupo 2'), ('Grupo 3'),
                        ('Grupo 4'), ('Grupo 5'), ('Grupo 6')
                    ON CONFLICT (name) DO NOTHING;
                ''')

                # 2. Tabela de Publicadores
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS publicadores (
                        id VARCHAR(50) PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        group_id INT REFERENCES grupos(id) ON UPDATE CASCADE ON DELETE SET NULL,
                        "group" VARCHAR(50) NOT NULL,
                        default_priv VARCHAR(100) NOT NULL,
                        gender VARCHAR(20) DEFAULT 'Masculino',
                        birth_date VARCHAR(20) DEFAULT '',
                        baptism_date VARCHAR(20) DEFAULT '',
                        hope VARCHAR(50) DEFAULT 'Outras Ovelhas',
                        active BOOLEAN DEFAULT TRUE,
                        obs TEXT
                    );
                ''')

                # 3. Tabela de Relatórios
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS relatorios (
                        id SERIAL PRIMARY KEY,
                        publisher_name VARCHAR(255) NOT NULL,
                        group_id INT REFERENCES grupos(id) ON UPDATE CASCADE ON DELETE SET NULL,
                        "group" VARCHAR(50) NOT NULL,
                        month VARCHAR(50) NOT NULL,
                        service_year VARCHAR(20) DEFAULT '',
                        privilege VARCHAR(100) NOT NULL,
                        hours INT DEFAULT 0,
                        revisitas INT DEFAULT 0,
                        estudos INT DEFAULT 0,
                        worked VARCHAR(10) DEFAULT 'Sim',
                        obs TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT unique_pub_month_year UNIQUE (publisher_name, month, service_year)
                    );
                ''')
                conn.commit()
    except Exception as e:
        print(f"[Aviso] Inicialização de tabelas adiada: {e}")

@app.on_event("startup")
def on_startup():
    init_db()

# Modelos Pydantic
class GroupModel(BaseModel):
    id: Optional[int] = None
    name: str
    overseer: Optional[str] = ""
    assistant: Optional[str] = ""
    meeting_place: Optional[str] = ""
    active: bool = True

class PublisherModel(BaseModel):
    id: str
    name: str
    group_id: Optional[int] = None
    group: str
    defaultPriv: str
    gender: Optional[str] = "Masculino"
    birthDate: Optional[str] = ""
    baptismDate: Optional[str] = ""
    hope: Optional[str] = "Outras Ovelhas"
    active: bool = True
    obs: Optional[str] = ""

class ReportModel(BaseModel):
    id: Optional[int] = None
    name: str
    group_id: Optional[int] = None
    group: str
    month: str
    service_year: Optional[str] = ""
    privilege: str
    hours: int = 0
    revisitas: int = 0
    estudos: int = 0
    worked: str = "Sim"
    obs: Optional[str] = ""

# ----------------- ENDPOINTS -----------------

@app.get("/")
def root():
    return {
        "status": "online",
        "mensagem": "API Gestão de Relatórios ativa",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
def health_check():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
    return {"status": "ok", "database": "PostgreSQL conectado com sucesso"}

# 1. GRUPOS
@app.get("/api/groups")
def list_groups():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, overseer, assistant, meeting_place, active FROM grupos WHERE active = TRUE ORDER BY name')
            return cur.fetchall()

@app.post("/api/groups")
def save_group(grp: GroupModel):
    with get_db() as conn:
        with conn.cursor() as cur:
            if grp.id:
                cur.execute('''
                    UPDATE grupos
                    SET name = %s, overseer = %s, assistant = %s, meeting_place = %s, active = %s
                    WHERE id = %s RETURNING id
                ''', (grp.name, grp.overseer, grp.assistant, grp.meeting_place, grp.active, grp.id))
            else:
                cur.execute('''
                    INSERT INTO grupos (name, overseer, assistant, meeting_place, active)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE SET
                        overseer = EXCLUDED.overseer,
                        assistant = EXCLUDED.assistant,
                        meeting_place = EXCLUDED.meeting_place,
                        active = EXCLUDED.active
                    RETURNING id
                ''', (grp.name, grp.overseer, grp.assistant, grp.meeting_place, grp.active))
            new_id = cur.fetchone()['id']
            conn.commit()
            return {"status": "success", "id": new_id, "name": grp.name}

# 2. PUBLICADORES
@app.get("/api/publishers")
def list_publishers():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT p.id, p.name, p.group_id, p."group", p.default_priv AS "defaultPriv",
                       p.gender, p.birth_date AS "birthDate", p.baptism_date AS "baptismDate",
                       p.hope, p.active, p.obs
                FROM publicadores p
                ORDER BY p."group", p.name
            ''')
            return cur.fetchall()

@app.post("/api/publishers")
def create_or_update_publisher(pub: PublisherModel):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO publicadores (id, name, group_id, "group", default_priv, gender, birth_date, baptism_date, hope, active, obs)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    group_id = EXCLUDED.group_id,
                    "group" = EXCLUDED."group",
                    default_priv = EXCLUDED.default_priv,
                    gender = EXCLUDED.gender,
                    birth_date = EXCLUDED.birth_date,
                    baptism_date = EXCLUDED.baptism_date,
                    hope = EXCLUDED.hope,
                    active = EXCLUDED.active,
                    obs = EXCLUDED.obs
            ''', (pub.id, pub.name, pub.group_id, pub.group, pub.defaultPriv, pub.gender, pub.birthDate, pub.baptismDate, pub.hope, pub.active, pub.obs))
            conn.commit()
    return {"status": "success", "publisher": pub}

# 3. RELATÓRIOS
@app.get("/api/reports")
def list_reports(month: Optional[str] = None, service_year: Optional[str] = None):
    with get_db() as conn:
        with conn.cursor() as cur:
            query = '''
                SELECT id, publisher_name AS name, group_id, "group", month, service_year, privilege, hours, revisitas, estudos, worked, obs
                FROM relatorios WHERE 1=1
            '''
            params = []
            if month and month != "all":
                query += ' AND month = %s'
                params.append(month)
            if service_year and service_year != "all":
                query += ' AND service_year = %s'
                params.append(service_year)
            query += ' ORDER BY "group", publisher_name'

            cur.execute(query, tuple(params))
            return cur.fetchall()

@app.post("/api/reports")
def save_report(report: ReportModel):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO relatorios (publisher_name, group_id, "group", month, service_year, privilege, hours, revisitas, estudos, worked, obs)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (publisher_name, month, service_year) DO UPDATE SET
                    group_id = EXCLUDED.group_id,
                    "group" = EXCLUDED."group",
                    privilege = EXCLUDED.privilege,
                    hours = EXCLUDED.hours,
                    revisitas = EXCLUDED.revisitas,
                    estudos = EXCLUDED.estudos,
                    worked = EXCLUDED.worked,
                    obs = EXCLUDED.obs
                RETURNING id
            ''', (report.name, report.group_id, report.group, report.month, report.service_year, report.privilege, report.hours, report.revisitas, report.estudos, report.worked, report.obs))

            new_id = cur.fetchone()['id']
            conn.commit()
            return {"status": "success", "id": new_id}

@app.delete("/api/reports/{report_id}")
def delete_report(report_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM relatorios WHERE id = %s", (report_id,))
            conn.commit()
    return {"status": "deleted", "id": report_id}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 50)
    print("Iniciando API Gestão de Relatórios...")
    print(f"Tentando conectar ao banco '{DB_CONFIG['dbname']}' em {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
    try:
        test_conn = psycopg2.connect(**DB_CONFIG)
        test_conn.close()
        print(">> PostgreSQL Conectado com sucesso!")
    except Exception as err:
        friendly_err = decode_pg_error(err)
        print(f"[!] AVISO: Não foi possível conectar ao PostgreSQL: {friendly_err}")
        print(">> Verifique se o serviço do Postgres está rodando e se a senha em DB_CONFIG está correta.\n")

    print("Subindo servidor em: http://127.0.0.1:8000")
    print("=" * 50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)