from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
import duckdb

app = FastAPI()

# Connect to your DuckDB file
con = duckdb.connect("SEEG-12-dados-nacionais.duckdb", read_only=True)

# 1) Health Check (always nice to have)
@app.get("/")
def read_root():
    return {"message": "SEEG v12 API is up and running!"}

# 2) Return rows with optional filters
#    For example, limit=10, Emissão/Remoção/Bunker=Emissão, Gás=CO2 (t), etc.
@app.get("/filter_data")
def filter_data(
    # essential
    start_year: int,
    end_year: int,
    limit: int = 10,
    emissao_type: Optional[str] = None,      # Emissão/Remoção/Bunker
    gas: Optional[str] = "CO2e (t) GWP-AR5", # Gás
    setor: Optional[str] = None,             # Setor de emissão
    estado: Optional[str] = None,            # Estado
    
    # LULUCF
    categoria: Optional[str] = None,         # Categoria emissora
    subcategoria: Optional[str] = None,      # Sub-categoria emissora
    atividade: Optional[str] = None,         # Atividade geral
    
    # other sectors
    recorte: Optional[str] = None,           # Recorte
    
    # others
    produto: Optional[str] = None,           # Produto ou sistema
    detalhamento: Optional[str] = None,      # Detalhamento
    bioma: Optional[str] = None              # Bioma  
):
    """
    Combine filters: Estado, Gás, Setor, and year range selection.
    Example: /filter_data?start_year=1970&end_year=1975&estado=Bahia
    """
    try:
        # Year columns
        all_years = [str(y) for y in range(1970, 2024)]
        selected_years = [y for y in all_years if start_year <= int(y) <= end_year]
        if not selected_years:
            return {"message": "No valid year columns in the requested range."}

        # 2. Define the core columns you always want to retrieve
        base_columns = [
            '"Emissão/Remoção/Bunker"',
            '"Gás"',
            '"Setor de emissão"',
            '"Estado"',
            '"Categoria emissora"',
            '"Sub-categoria emissora"',
            '"Atividade geral"',
            '"Recorte"',
            '"Produto ou sistema"',
            '"Detalhamento"',
            '"Bioma"'
        ]
        columns = base_columns + [f'"{year}"' for year in selected_years]
        
        query = f"SELECT {', '.join(columns)} FROM \"SEEG-12-dados-nacionais\" "

        # WHERE filters
        filters = []
        params = []
        if gas:
            filters.append('"Gás" = ?')
            params.append(gas)
        
        if setor:
            filters.append('"Setor de emissão" = ?')
            params.append(setor)
        
        if estado:
            filters.append('"Estado" = ?')
            params.append(estado)
        
        if categoria:
            filters.append('"Categoria emissora" = ?')
            params.append(categoria)
        
        if subcategoria:
            filters.append('"Sub-categoria emissora" = ?')
            params.append(subcategoria)
        
        if atividade:
            filters.append('"Atividade geral" = ?')
            params.append(atividade)
        
        if recorte:
            filters.append('"Recorte" = ?')
            params.append(recorte)
        
        if produto:
            filters.append('"Produto ou sistema" = ?')
            params.append(produto)
        
        if detalhamento:
            filters.append('"Detalhamento" = ?')
            params.append(detalhamento)
        
        if bioma:
            filters.append('"Bioma" = ?')
            params.append(bioma)            
            

        if filters:
            query += " WHERE " + " AND ".join(filters)

        # LIMIT
        query += f" LIMIT {limit}"

        # Run query
        df = con.execute(query, params).fetchdf()
        return df.to_dict("records")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 3) Get all unique values in a given column
@app.get("/unique_values/{column_name}")
def unique_values(column_name: str):
    """
    Return unique values from a specified column, for example:
    /unique_values/Gás
    /unique_values/Estado
    /unique_values/Setor%20de%20emissão
    """
    try:
        # Protect against injection (only allow known columns)
        allowed_columns = [
            "Emissão/Remoção/Bunker", "Gás", "Setor de emissão",
            "Estado", "Bioma", "Categoria emissora", "Sub-categoria emissora",
            "Produto ou sistema", "Detalhamento", "Recorte", "Atividade geral"
            # ... plus any others you trust
        ]
        if column_name not in allowed_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Column '{column_name}' not allowed or does not exist."
            )

        query = f'SELECT DISTINCT "{column_name}" FROM \"SEEG-12-dados-nacionais\" ORDER BY "{column_name}"'
        df = con.execute(query).fetchdf()
        values = df[column_name].fillna("N/A").unique().tolist()
        return {"column": column_name, "unique_values": values}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



        


