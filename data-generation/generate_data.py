import pandas as pd
import numpy as np
import random
from faker import Faker
import os

fake = Faker()
np.random.seed(42)
random.seed(42)

N_CLIENTES = 10000
N_PRODUCTOS = 50
N_MOV = 500000
N_OBLIG = 30000
N_SUC = 200
N_COM = 80000

START_DATE = pd.Timestamp("2023-01-01")
END_DATE = pd.Timestamp("2024-01-01")

def random_dates(n):
    fechas = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    pesos = np.sin(np.linspace(0, 3*np.pi, len(fechas))) + 1.5
    probs = pesos / pesos.sum()
    return np.random.choice(fechas, size=n, p=probs)

def generate_time_components(n):
    horas = np.random.choice(
        [8,9,10,11,12,13,14,15,16,17,18,19,20],
        size=n,
        p=[0.04,0.06,0.09,0.08,0.11,0.12,0.1,0.08,0.07,0.07,0.08,0.06,0.04]
    )
    minutos = np.random.randint(0, 60, n)
    segundos = np.random.randint(0, 60, n)

    return [
        f"{h:02d}:{m:02d}:{s:02d}"
        for h, m, s in zip(horas, minutos, segundos)
    ]

def apply_nulls(df, pct=0.05):
    df = df.copy()
    for col in df.columns:
        if col.startswith("id"):
            continue
        if df[col].dtype == bool:
            continue
        if "fec" in col or "hra" in col:
            continue
        mask = np.random.rand(len(df)) < pct
        df.loc[mask, col] = None
    return df

def gen_clientes(n):
    return pd.DataFrame({
        "id_cli": np.arange(1, n+1),
        "nomb_cli": [fake.first_name() for _ in range(n)],
        "apell_cli": [fake.last_name() for _ in range(n)],
        "tip_doc": np.random.choice(["CC","CE"], n),
        "num_doc": np.random.randint(1e8,1e9,n),
        "fec_nac": pd.to_datetime("1970-01-01") + pd.to_timedelta(np.random.randint(0,18000,n), unit="D"),
        "fec_alta": random_dates(n),
        "cod_segmento": np.random.choice(["BASICO","ESTANDAR","PREMIUM","ELITE"], n, p=[0.4,0.3,0.2,0.1]),
        "score_buro": np.clip(np.random.normal(650,100,n),300,850).astype(int),
        "ciudad_res": [fake.city() for _ in range(n)],
        "depto_res": [fake.state() for _ in range(n)],
        "estado_cli": np.random.choice(["ACTIVO","INACTIVO"], n, p=[0.85,0.15]),
        "canal_adquis": np.random.choice(["APP","WEB","OFICINA"], n, p=[0.5,0.3,0.2])
    })

def gen_productos(n):
    return pd.DataFrame({
        "cod_prod": [f"P{i:03}" for i in range(1,n+1)],
        "desc_prod": [f"Producto_{i}" for i in range(n)],
        "tip_prod": np.random.choice(["CREDITO","AHORRO","TRANSACCIONAL"], n),
        "tasa_ea": np.round(np.random.uniform(0.01,0.35,n),4),
        "plazo_max_meses": np.random.choice([12,24,36,48,60], n),
        "cuota_min": np.random.randint(50000,300000,n),
        "comision_admin": np.random.randint(0,20000,n),
        "estado_prod": np.random.choice(["ACTIVO","INACTIVO"], n, p=[0.9,0.1])
    })

def gen_sucursales(n):
    return pd.DataFrame({
        "cod_suc": [f"S{i:03}" for i in range(1,n+1)],
        "nom_suc": [f"Sucursal_{i}" for i in range(n)],
        "tip_punto": np.random.choice(["OFICINA","CAJERO","CORRESPONSAL"], n, p=[0.4,0.3,0.3]),
        "ciudad": [fake.city() for _ in range(n)],
        "depto": [fake.state() for _ in range(n)],
        "latitud": np.random.uniform(-90,90,n),
        "longitud": np.random.uniform(-180,180,n),
        "activo": np.random.choice([True,False], n, p=[0.85,0.15])
    })

def gen_movimientos(n, cli, prod):
    fechas = random_dates(n)
    hra_mov = generate_time_components(n)

    vr_mov = np.random.lognormal(mean=10.5, sigma=0.7, size=n)
    vr_mov = np.clip(vr_mov, 1000, 50000000)
    vr_mov = np.round(vr_mov, -2)

    df = pd.DataFrame({
        "id_mov": np.arange(1,n+1),
        "id_cli": np.random.choice(cli.id_cli, n),
        "cod_prod": np.random.choice(prod.cod_prod, n),
        "num_cuenta": np.random.randint(1e7,1e8,n),
        "fec_mov": pd.to_datetime(fechas),
        "hra_mov": hra_mov,
        "vr_mov": vr_mov.astype(int),
        "tip_mov": np.random.choice(["PAGO","TRANSFERENCIA","RETIRO","COMPRA"], n),
        "cod_canal": np.random.choice(["APP","WEB","CAJERO","OFICINA"], n),
        "cod_ciudad": [fake.city() for _ in range(n)],
        "cod_estado_mov": "OK",
        "id_dispositivo": [fake.uuid4() for _ in range(n)]
    })

    return df

def generar_anomalias_movimientos(df):
    df = df.copy()

    duplicados = df.sample(200)
    df = pd.concat([df, duplicados], ignore_index=True)

    idx_neg = df.sample(100).index
    df.loc[idx_neg, "vr_mov"] *= -1

    idx_fecha = df.sample(100).index
    df.loc[idx_fecha, "fec_mov"] = pd.Timestamp("2099-01-01")
    df.loc[idx_fecha, "hra_mov"] = "00:00:00"

    return df

def gen_obligaciones(n, cli, prod):
    vr_aprobado = np.random.randint(1_000_000, 50_000_000, n)
    pct_desembolso = np.random.uniform(0.85, 1.0, n)
    vr_desembolsado = vr_aprobado * pct_desembolso

    pct_saldo = np.random.uniform(0.2, 1.0, n)
    sdo_capital = vr_desembolsado * pct_saldo

    plazo_meses = np.random.choice([12, 24, 36, 48, 60], n)
    vr_cuota = vr_desembolsado / plazo_meses

    fec_desembolso = random_dates(n)
    fec_venc = fec_desembolso + pd.to_timedelta(plazo_meses * 30, unit="D")

    vr_aprobado = np.round(vr_aprobado, -3)
    vr_desembolsado = np.round(vr_desembolsado, -3)
    sdo_capital = np.round(sdo_capital, -3)
    vr_cuota = np.round(vr_cuota, -3)

    dias_mora_act = np.random.choice([0,0,0,10,30,60,90,120], n)

    calif_riesgo = np.where(dias_mora_act == 0, "A",
                    np.where(dias_mora_act <= 30, "B",
                    np.where(dias_mora_act <= 60, "C",
                    np.where(dias_mora_act <= 90, "D", "E"))))

    num_cuotas_pend = (sdo_capital / vr_cuota).astype(int)
    num_cuotas_pend = np.clip(num_cuotas_pend, 1, 60)

    return pd.DataFrame({
        "id_oblig": np.arange(1, n+1),
        "id_cli": np.random.choice(cli.id_cli, n),
        "cod_prod": np.random.choice(prod.cod_prod, n),
        "vr_aprobado": vr_aprobado.astype(int),
        "vr_desembolsado": vr_desembolsado.astype(int),
        "sdo_capital": sdo_capital.astype(int),
        "vr_cuota": vr_cuota.astype(int),
        "fec_desembolso": pd.to_datetime(fec_desembolso),
        "fec_venc": pd.to_datetime(fec_venc),
        "dias_mora_act": dias_mora_act,
        "num_cuotas_pend": num_cuotas_pend,
        "calif_riesgo": calif_riesgo
    })

def gen_comisiones(n, cli, prod):
    vr_comision = np.random.uniform(1000,20000,n)
    vr_comision = np.round(vr_comision, -2)

    return pd.DataFrame({
        "id_comision": np.arange(1,n+1),
        "id_cli": np.random.choice(cli.id_cli,n),
        "cod_prod": np.random.choice(prod.cod_prod,n),
        "fec_cobro": pd.to_datetime(random_dates(n)),
        "vr_comision": vr_comision.astype(int),
        "tip_comision": np.random.choice(["ADMIN","RETIRO","TRANSFERENCIA"], n),
        "estado_cobro": np.random.choice(["COBRADO","PENDIENTE"], n)
    })

def validar_fk(df, col, ref_df, ref_col):
    invalid = ~df[col].isin(ref_df[ref_col])
    print(col, "invalidos:", invalid.sum())

def log_dataset(df, name):
    print(name)
    print("registros:", len(df))
    print("nulos:")
    print(df.isnull().sum())

def documentar_anomalias():
    print("ANOMALIAS GENERADAS:")
    print("1. Duplicados en TB_MOV_FINANCIEROS")
    print("2. Valores negativos en vr_mov")
    print("3. Fechas futuras en fec_mov")

def save(df, name):
    os.makedirs("output", exist_ok=True)
    df.to_csv(f"output/{name}.csv", index=False)
    df.to_parquet(f"output/{name}.parquet", index=False)
    df.to_json(f"output/{name}.json", orient="records")

if __name__ == "__main__":

    cli = gen_clientes(N_CLIENTES)
    prod = gen_productos(N_PRODUCTOS)
    suc = gen_sucursales(N_SUC)

    mov = gen_movimientos(N_MOV, cli, prod)
    mov = generar_anomalias_movimientos(mov)

    obl = gen_obligaciones(N_OBLIG, cli, prod)
    com = gen_comisiones(N_COM, cli, prod)

    cli = apply_nulls(cli)
    prod = apply_nulls(prod)
    suc = apply_nulls(suc)
    mov = apply_nulls(mov)
    obl = apply_nulls(obl)
    com = apply_nulls(com)

    validar_fk(mov, "id_cli", cli, "id_cli")
    validar_fk(obl, "cod_prod", prod, "cod_prod")

    log_dataset(cli, "TB_CLIENTES_CORE")
    log_dataset(mov, "TB_MOV_FINANCIEROS")

    documentar_anomalias()

    save(cli, "TB_CLIENTES_CORE")
    save(prod, "TB_PRODUCTOS_CAT")
    save(suc, "TB_SUCURSALES_RED")
    save(mov, "TB_MOV_FINANCIEROS")
    save(obl, "TB_OBLIGACIONES")
    save(com, "TB_COMISIONES_LOG")