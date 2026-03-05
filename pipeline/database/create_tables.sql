CREATE TABLE IF NOT EXISTS precatorios (

    id SERIAL PRIMARY KEY,

    posicao INTEGER,
    ente_devedor TEXT,
    ano INTEGER,
    natureza TEXT,
    data_entrada_oficio TEXT,
    numero_pje TEXT,
    tipo TEXT,
    valor NUMERIC,
    observacoes TEXT,

    UNIQUE (numero_pje, tipo)

);