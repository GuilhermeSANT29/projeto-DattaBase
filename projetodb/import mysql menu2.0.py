import mysql.connector
import sys
import json
import os
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

def cadastrar_maquina():
    nome = input("Nome da máquina: ").strip()
    if not nome:
        print("Nome inválido.")
        return
    cur = conexao.cursor()
    
    try:
        cur.execute("INSERT INTO maquinas (nome) VALUES (%s)", (nome,))
        conexao.commit()
        print("Máquina cadastrada com id", cur.lastrowid)
    except mysql.connector.Error as e:
        if e.errno == 1062:
            print("Já existe uma máquina com esse nome.")
        else:
            print("Erro ao cadastrar máquina:", e)
    finally:
        cur.close()

def cadastrar_sensor():
    nome = input("Nome do sensor: ").strip()
    if not nome:
        print("Nome inválido.")
        return
    tipo = input("Tipo (opcional): ").strip() or None
    cur = conexao.cursor()
    
    try:
        # Mostrar máquinas para associação (opcional)
        cur.execute("SELECT id, nome FROM maquinas ORDER BY id")
        maquinas = cur.fetchall()
        maquina_id = None
        if maquinas:
            print("Máquinas disponíveis:")
            for m in maquinas:
                print(f"{m[0]} - {m[1]}")
            esc = input("ID da máquina associada (enter para nenhuma): ").strip()
            if esc:
                try:
                    maquina_id = int(esc)
                except ValueError:
                    print("ID inválido. Sem associação.")
                    maquina_id = None

        cur.execute("INSERT INTO sensores (nome, tipo, maquina_id) VALUES (%s, %s, %s)",
                    (nome, tipo, maquina_id))
        conexao.commit()
        print("Sensor cadastrado com id", cur.lastrowid)
    except mysql.connector.Error as e:
        print("Erro ao cadastrar sensor:", e)
    finally:
        cur.close()

def cadastrar_operador():
    nome = input("Nome do operador: ").strip()
    if not nome:
        print("Nome inválido.")
        return
    cargo = input("Cargo (opcional): ").strip() or None
    cur = conexao.cursor()
    
    try:
        cur.execute("INSERT INTO operadores (nome, cargo) VALUES (%s, %s)", (nome, cargo))
        conexao.commit()
        print("Operador cadastrado com id", cur.lastrowid)
    except mysql.connector.Error as e:
        print("Erro ao cadastrar operador:", e)
    finally:
        cur.close()

def registrar_leitura():
    cur = conexao.cursor()
    
    try:
        # Escolher máquina
        cur.execute("SELECT id, nome FROM maquinas ORDER BY id")
        maquinas = cur.fetchall()
        if not maquinas:
            print("Nenhuma máquina cadastrada.")
            return
        for m in maquinas:
            print(f"{m[0]} - {m[1]}")
        maquina_id = int(input("ID da máquina: ").strip())

        # Escolher sensor
        cur.execute("SELECT id, nome FROM sensores WHERE maquina_id = %s OR maquina_id IS NULL ORDER BY id", (maquina_id,))
        sensores = cur.fetchall()
        if not sensores:
            print("Nenhum sensor disponível para essa máquina.")
            return
        for s in sensores:
            print(f"{s[0]} - {s[1]}")
        sensor_id = int(input("ID do sensor: ").strip())

        # Escolher operador (opcional)
        cur.execute("SELECT id, nome FROM operadores ORDER BY id")
        operadores = cur.fetchall()
        operador_id = None
        if operadores:
            for o in operadores:
                print(f"{o[0]} - {o[1]}")
            esc = input("ID do operador (enter para nenhum): ").strip()
            if esc:
                operador_id = int(esc)

        valor_str = input("Valor da leitura (ex: 12.34): ").strip().replace(",", ".")
        valor = float(valor_str)

        cur.execute(
            "INSERT INTO leituras (maquina_id, sensor_id, operador_id, valor) VALUES (%s, %s, %s, %s)",
            (maquina_id, sensor_id, operador_id, valor)
        )
        conexao.commit()
        leitura_id = cur.lastrowid
        print("Leitura registrada com id", leitura_id)

        # Análise de qualidade: Classificação automática de alertas
        if valor <= 70:
            nivel = "NORMAL"
        elif 71 <= valor <= 90:
            nivel = "ALERTA"
        else:
            nivel = "CRÍTICO"

        if nivel != "NORMAL":
            cur.execute("INSERT INTO alertas (leitura_id, nivel, descricao) VALUES (%s, %s, %s)",
                        (leitura_id, nivel, f"Leitura crítica: {valor}°C"))
            conexao.commit()
            alerta_id = cur.lastrowid
            print(f"Alerta automático gerado: {nivel}")

        # Salvar dados complementares em JSON
        os.makedirs("dados_json", exist_ok=True)
        dados_leitura = {
            "id": leitura_id,
            "maquina_id": maquina_id,
            "sensor_id": sensor_id,
            "operador_id": operador_id,
            "valor": valor,
            "data_hora": str(datetime.now())
        }
        with open("dados_json/leituras.json", "a", encoding="utf-8") as f:
            json.dump(dados_leitura, f, ensure_ascii=False)
            f.write("\n")

        if nivel != "NORMAL":
            dados_alerta = {
                "id": alerta_id,
                "leitura_id": leitura_id,
                "nivel": nivel,
                "descricao": f"Leitura crítica: {valor}°C",
                "data_hora": str(datetime.now())
            }
            with open("dados_json/alertas.json", "a", encoding="utf-8") as f:
                json.dump(dados_alerta, f, ensure_ascii=False)
                f.write("\n")
    except ValueError:
        print("Entrada numérica inválida.")
    except mysql.connector.Error as e:
        print("Erro ao registrar leitura:", e)
    finally:
        cur.close()

def cadastrar_alerta():
    cur = conexao.cursor()
    
    try:
        # Selecionar leitura
        cur.execute("SELECT id, valor FROM leituras ORDER BY id")
        leituras = cur.fetchall()
        if not leituras:
            print("Nenhuma leitura cadastrada.")
            return
        for l in leituras:
            print(f"{l[0]} - Valor: {l[1]}")
        leitura_id = int(input("ID da leitura associada: ").strip())

        nivel = input("Nível do alerta: ").strip()
        descricao = input("Descrição: ").strip()

        cur.execute("INSERT INTO alertas (leitura_id, nivel, descricao) VALUES (%s, %s, %s)",
                    (leitura_id, nivel, descricao))
        conexao.commit()
        alerta_id = cur.lastrowid
        print("Alerta cadastrado com id", alerta_id)

        # Salvar em JSON
        os.makedirs("dados_json", exist_ok=True)
        dados_alerta = {
            "id": alerta_id,
            "leitura_id": leitura_id,
            "nivel": nivel,
            "descricao": descricao,
            "data_hora": str(datetime.now())
        }
        with open("dados_json/alertas.json", "a", encoding="utf-8") as f:
            json.dump(dados_alerta, f, ensure_ascii=False)
            f.write("\n")
    except mysql.connector.Error as e:
        print("Erro ao cadastrar alerta:", e)
    finally:
        cur.close()

def cadastrar_manutencao():
    cur = conexao.cursor()
    
    try:
        # Selecionar máquina
        cur.execute("SELECT id, nome FROM maquinas ORDER BY id")
        maquinas = cur.fetchall()
        if not maquinas:
            print("Cadastre uma máquina primeiro.")
            return
        for m in maquinas: 
            print(f"{m[0]} - {m[1]}")
        maquina_id = int(input("ID da máquina: ").strip())

        # Selecionar operador
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

def listar_dados():
    while True:
        print("\n1 - Máquinas")
        print("2 - Sensores")
        print("3 - Operadores")
        print("4 - Leituras")
        print("5 - Alertas")
        print("6 - Manutenções")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        cur = conexao.cursor()
        
        try:
            if op == "1":
                cur.execute("SELECT * FROM maquinas ORDER BY id")
            elif op == "2":
                cur.execute("SELECT id, nome, tipo, maquina_id FROM sensores ORDER BY id")
            elif op == "3":
                cur.execute("SELECT id, nome, cargo FROM operadores ORDER BY id")
            elif op == "4":
                cur.execute("""
                    SELECT l.id, m.nome AS maquina, s.nome AS sensor, o.nome AS operador, l.valor, l.data_hora
                    FROM leituras l
                    LEFT JOIN maquinas m ON l.maquina_id = m.id
                    LEFT JOIN sensores s ON l.sensor_id = s.id
                    LEFT JOIN operadores o ON l.operador_id = o.id
                    ORDER BY l.id
                """)
            elif op == "5":
                cur.execute("""
                    SELECT a.id, l.id AS leitura_id, l.valor, a.nivel, a.descricao, a.data_hora
                    FROM alertas a
                    LEFT JOIN leituras l ON a.leitura_id = l.id
                    ORDER BY a.id
                """)
            elif op == "6":
                cur.execute("""
                    SELECT mt.id, m.nome AS maquina, o.nome AS operador, mt.descricao, mt.data_prevista, mt.momento
                    FROM manutencoes mt
                    LEFT JOIN maquinas m ON mt.maquina_id = m.id
                    LEFT JOIN operadores o ON mt.operador_id = o.id
                    ORDER BY mt.id
                """)
            elif op == "0":
                return
            else:
                print("Opção inválida.")
                continue
            
            rows = cur.fetchall()
            if not rows:
                print("Nenhum registro.")
            else:
                for r in rows:
                    print(" | ".join(str(x) for x in r))
        except mysql.connector.Error as e:
            print("Erro ao listar dados:", e)
        finally:
            cur.close()

def menu():
    while True:
        print("\n1 - Cadastrar Máquina")
        print("2 - Cadastrar Sensor")
        print("3 - Cadastrar Operador")
        print("4 - Registrar Leitura")
        print("5 - Listar Dados")
        print("6 - Cadastrar Alerta")
        print("7 - Cadastrar Manutenção")
        print("0 - Sair")

        op = input("Escolha: ").strip()

        if op == "1":
            cadastrar_maquina()
        elif op == "2":
            cadastrar_sensor()
        elif op == "3":
            cadastrar_operador()
        elif op == "4":
            registrar_leitura()
        elif op == "5":
            listar_dados()
        elif op == "6":
            cadastrar_alerta()
        elif op == "7":
            cadastrar_manutencao()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    try:
        menu()
    finally:
        try:
            conexao.close()
        except:
            pass