import mysql.connector
import sys

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
        print("Leitura registrada com id", cur.lastrowid)
    except ValueError:
        print("Entrada numérica inválida.")
    except mysql.connector.Error as e:
        print("Erro ao registrar leitura:", e)
    finally:
        cur.close()

def cadastrar_alerta():
    cur = conexao.cursor()
    
    try:
        # Selecionar máquina
        cur.execute("SELECT id, nome FROM maquinas ORDER BY id")
        maquinas = cur.fetchall()
        maquina_id = None
        if maquinas:
            for m in maquinas: 
                print(f"{m[0]} - {m[1]}")
            esc = input("ID da máquina (enter para nenhum): ").strip()
            if esc:
                maquina_id = int(esc)

        # Selecionar sensor
        cur.execute("SELECT id, nome FROM sensores ORDER BY id")
        sensores = cur.fetchall()
        sensor_id = None
        if sensores:
            for s in sensores: 
                print(f"{s[0]} - {s[1]}")
            esc = input("ID do sensor (enter para nenhum): ").strip()
            if esc:
                sensor_id = int(esc)

        nivel = input("Nível do alerta: ").strip()
        descricao = input("Descrição: ").strip()

        cur.execute("INSERT INTO alertas (maquina_id, sensor_id, nivel, descricao) VALUES (%s, %s, %s, %s)",
                    (maquina_id, sensor_id, nivel, descricao))
        conexao.commit()
        print("Alerta cadastrado com id", cur.lastrowid)
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
                    SELECT a.id, m.nome AS maquina, s.nome AS sensor, a.nivel, a.descricao, a.data_hora
                    FROM alertas a
                    LEFT JOIN maquinas m ON a.maquina_id = m.id
                    LEFT JOIN sensores s ON a.sensor_id = s.id
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