import mysql.connector
import sys
from datetime import datetime

# --- CONFIGURE suas credenciais ---
DB_HOST = "localhost"
DB_USER = "ADM"
DB_PASSWORD = "senha123"
DB_NAME = "projetodb"
# -----------------------

try:
    conexao = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
except mysql.connector.Error as e:
    print("Erro ao conectar ao banco:", e)
    sys.exit(1)

cursor = conexao.cursor()

# MENU
def menu():
    print("\n" + "=" * 50)
    print("MENU DO PROJETO - SISTEMA DE MONITORAMENTO INDUSTRIAL")
    print("=" * 50)
    print("\n1 - Cadastrar Máquina")
    print("2 - Cadastrar Sensor")
    print("3 - Cadastrar Operador")
    print("4 - Registrar Leitura")
    print("5 - Listar Máquinas")
    print("6 - Cadastrar Manutenção")
    print("0 - Sair")
    print("-" * 50)
    return input("Digite sua escolha (0-6): ")

# CADASTRAR MÁQUINA
def cadastrar_maquina():
    nome = input("Nome da máquina: ")
    local = input("Localização: ")

    cursor.execute(
        "INSERT INTO maquinas (nome, localizacao) VALUES (%s, %s)",
        (nome, local)
    )
    conexao.commit()

    print("✅ Máquina cadastrada!")

# CADASTRAR SENSOR
def cadastrar_sensor():
    tipo = input("Tipo do sensor: ")
    maquina_id = int(input("ID da máquina: "))

    cursor.execute(
        "INSERT INTO sensores (tipo, maquina_id) VALUES (%s, %s)",
        (tipo, maquina_id)
    )
    conexao.commit()

    print("✅ Sensor cadastrado!")

# CADASTRAR OPERADOR
def cadastrar_operador():
    nome = input("Nome do operador: ")
    turno = input("Turno: ")

    cursor.execute(
        "INSERT INTO operadores (nome, turno) VALUES (%s, %s)",
        (nome, turno)
    )
    conexao.commit()

    print("✅ Operador cadastrado!")

# REGISTRAR LEITURA
def registrar_leitura():
    sensor_id = int(input("ID do sensor: "))
    temp = float(input("Temperatura: "))
    data = datetime.now()

    cursor.execute(
        "INSERT INTO leituras (sensor_id, temperatura, data_hora) VALUES (%s, %s, %s)",
        (sensor_id, temp, data)
    )
    conexao.commit()

    leitura_id = cursor.lastrowid

    # CLASSIFICAÇÃO
    if temp <= 70:
        nivel = "NORMAL"
    elif temp <= 90:
        nivel = "ALERTA"
    else:
        nivel = "CRÍTICO"

    cursor.execute(
        "INSERT INTO alertas (leitura_id, nivel) VALUES (%s, %s)",
        (leitura_id, nivel)
    )
    conexao.commit()

    print("🔥 Status:", nivel)

# LISTAR MÁQUINAS
def listar_maquinas():
    cursor.execute("SELECT * FROM maquinas")
    dados = cursor.fetchall()

    for m in dados:
        print(m)

# CADASTRAR MANUTENÇÃO
def cadastrar_manutencao():
    cur = conexao.cursor()
    
    try:
        cur.execute("SELECT id, nome FROM maquinas ORDER BY id")
        maquinas = cur.fetchall()
        if not maquinas:
            print("Cadastre uma máquina primeiro.")
            return
        for m in maquinas: 
            print(f"{m[0]} - {m[1]}")
        maquina_id = int(input("ID da máquina: ").strip())

        cur.execute("SELECT id, nome FROM operadores ORDER BY id")
        operadores = cur.fetchall()
        operador_id = None
        if operadores:
            for o in operadores: 
                print(f"{o[0]} - {o[1]}")
            esc = input("ID do operador responsável (enter para nenhum): ").strip()
            if esc:
                operador_id = int(esc)

        descricao = input("Descrição da manutenção: ").strip()
        data_prevista = input("Data prevista (YYYY-MM-DD HH:MM) (enter para vazio): ").strip() or None

        cur.execute("INSERT INTO manutencoes (maquina_id, operador_id, descricao, data_prevista) VALUES (%s, %s, %s, %s)",
                    (maquina_id, operador_id, descricao, data_prevista))
        conexao.commit()
        print("Manutenção cadastrada com id", cur.lastrowid)
    except mysql.connector.Error as e:
        print("Erro ao cadastrar manutenção:", e)
    finally:
        cur.close()

# LOOP
while True:
    op = menu()

    if op == "1":
        cadastrar_maquina()

    elif op == "2":
        cadastrar_sensor()

    elif op == "3":
        cadastrar_operador()

    elif op == "4":
        registrar_leitura()

    elif op == "5":
        listar_maquinas()

    elif op == "6":
        cadastrar_manutencao()

    elif op == "0":
        print("Encerrando o sistema...")
        break

if __name__ == "__main__":
    try:
        menu()
    finally:
        try:
            conexao.close()
        except:
            pass