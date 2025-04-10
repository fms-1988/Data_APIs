# SEEG v12 API Documentation

The SEEG v12 API provides access to environmental data from the SEEG project version 12. The original dataset is available on the [SEEG project website](https://seeg.eco.br/linha/), and the API can be accessed via [api_seeg.carbonprice.top](https://api_seeg.carbonprice.top).

The API uses DuckDB to query the SEEG-12-dados-nacionais database in read-only mode. It includes endpoints for a simple health check, filtering data with various parameters, and retrieving unique values from specific columns.

---

## Endpoints

### 1. Health Check

- **Endpoint:** `GET /`
- **Description:**  
  Checks that the API is up and running.
- **Response Example:**
  ```json
  {
    "message": "SEEG v12 API is up and running!"
  }
  ```

---

### 2. Filter Data

- **Endpoint:** `GET /filter_data`
- **Description:**  
  Retrieve data rows filtered by a combination of parameters such as year range, state, emission sector, gas type, and more.

- **Query Parameters:**
  - **start_year** (*int*, **required**): The start year for filtering the data.
  - **end_year** (*int*, **required**): The end year for filtering the data.
  - **limit** (*int*, *optional*, default: 10): The maximum number of records to return.
  - **emissao_type** (*str*, *optional*): Filter for emission type (e.g., "Emissão", "Remoção", "Bunker").
  - **gas** (*str*, *optional*, default: `"CO2e (t) GWP-AR5"`): Filter for the type of gas.
  - **setor** (*str*, *optional*): Filter for the emission sector.
  - **estado** (*str*, *optional*): Filter for the state.
  - **categoria** (*str*, *optional*): Filter for the emitter category (specific to LULUCF).
  - **subcategoria** (*str*, *optional*): Filter for the emitter sub-category (specific to LULUCF).
  - **atividade** (*str*, *optional*): Filter for the general activity (specific to LULUCF).
  - **recorte** (*str*, *optional*): Filter for other sectors.
  - **produto** (*str*, *optional*): Filter for product or system.
  - **detalhamento** (*str*, *optional*): Filter for detailed classification.
  - **bioma** (*str*, *optional*): Filter for the biome.

- **Example Request:**

  Retrieve records for Minas Gerais in the "Agropecuária" sector, filtering for the gas "N2O (t)" between the years 2005 and 2010, and limiting the result to 15 records:
  
  ```
  GET https://api_seeg.carbonprice.top/filter_data?start_year=2005&end_year=2010&estado=Minas%20Gerais&setor=Agropecu%C3%A1ria&gas=N2O%20(t)&limit=15
  ```

- **Unlimited Search:**

  The API uses a `limit` parameter to control the number of returned records. To effectively “unlimit” your search, set the `limit` to a value that exceeds the expected number of matching records. For instance, if you expect fewer than 100,000 rows, you can use:
  
  ```
  GET https://api_seeg.carbonprice.top/filter_data?start_year=2005&end_year=2010&limit=100000
  ```
  
  *Note:* Currently, the API always applies a `LIMIT` clause. Adjust the `limit` parameter to a sufficiently high number if you wish to retrieve all results, or consider modifying the API code to remove the limit if necessary.

---

### 3. Unique Values

- **Endpoint:** `GET /unique_values/{column_name}`
- **Description:**  
  Retrieve all unique values from a specified column in the database.
  
- **Path Parameter:**
  - **column_name** (*str*): Name of the column for which you want unique values. Allowed column names include:
    - "Emissão/Remoção/Bunker"
    - "Gás"
    - "Setor de emissão"
    - "Estado"
    - "Bioma"
    - "Categoria emissora"
    - "Sub-categoria emissora"
    - "Produto ou sistema"
    - "Detalhamento"
    - "Recorte"
    - "Atividade geral"

- **Example Request:**

  To retrieve all unique gas types:
  
  ```
  GET https://api_seeg.carbonprice.top/unique_values/Gás
  ```
  
- **Response Example:**
  ```json
  {
    "column": "Gás",
    "unique_values": ["CO2e (t) GWP-AR5", "N2O (t)", "..."]
  }
  ```

---

## Additional Notes

- **Database Connection:**  
  The API connects to the `SEEG-12-dados-nacionais.duckdb` database file in read-only mode.

- **Error Handling:**  
  The API uses HTTP exceptions to return informative error messages when invalid parameters are provided or when a query fails. These errors include a descriptive message in the response’s `detail` field.

- **Usage Recommendations:**  
  When using the `/filter_data` endpoint, always ensure that the `start_year` and `end_year` parameters fall within the valid range (1970–2023). Additionally, if filtering by columns that are specific to certain sectors (e.g., LULUCF-related fields), ensure that your query parameters align with the expected dataset structure.
  If your parameter contains **spaces** or **special characters** like parentheses `(`, `)`, or accents, you need to **URL-encode** them. For example:  
  - `Bahia` is fine (no spaces).  
  - `Minas Gerais` should be `Minas%20Gerais`.  
  - `CO2 (t)` might become `CO2%20(t)`.

---

This documentation should help you integrate with the SEEG v12 API and utilize its endpoints for retrieving environmental data. For further information on the original data, please visit the [SEEG project website](https://seeg.eco.br/linha/).
