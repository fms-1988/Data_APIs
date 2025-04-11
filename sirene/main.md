## SIRENE v7 API Documentation (MCTI)

The SIRENE v7 API provides access to emissions data from the [SIRENE project](https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene), maintained by the Brazilian Ministry of Science, Technology and Innovation (MCTI). The API supports filtering by sector, NFR code/description, and greenhouse gas type over a range of years (1990–2022).

All endpoints are available under the same host: [https://api_seeg.carbonprice.top](https://api_seeg.carbonprice.top)

---

### Endpoints for SIRENE Data

---

### 1. Filter Data

- **Endpoint:** `GET /sirene/filter_data`
- **Description:**  
  Retrieve emissions data from the MCTI/SIRENE database with optional filters.

- **Query Parameters:**
  - **start_year** (*int*, **required**)  
    Filter for the starting year of emissions data (1990–2022).
  
  - **end_year** (*int*, **required**)  
    Filter for the ending year of emissions data (1990–2022).

  - **limit** (*int*, *optional*, default: 10)  
    Maximum number of rows to return. To get all results, use a high value (e.g., 100000).
  
  - **setor_nfr** (*str*, *optional*)  
    Filter by the NFR sector. Maps to column `"setor_nfr"`.
  
  - **nfr_code** (*str*, *optional*)  
    Filter by the NFR code. Maps to column `"nfr_code"`.
  
  - **nfr_description** (*str*, *optional*)  
    Filter by the description of the NFR code. Maps to column `"nfr_description"`.
  
  - **gas** (*str*, *optional*, default: `"CO2e_GWP_AR5"`)  
    Filter by the gas type. Maps to column `"gas"`.

- **Example Request:**

  Get N2O data for the "Energia" sector between 2005 and 2010:
  
  ```
  GET https://api_seeg.carbonprice.top/sirene/filter_data?start_year=2005&end_year=2010&setor_nfr=Energia&gas=N2O
  ```

- **Unlimited Search Example:**

  Get all CO2e emissions from all sectors between 2000 and 2020:

  ```
  GET https://api_seeg.carbonprice.top/sirene/filter_data?start_year=2000&end_year=2020&gas=CO2e_GWP_AR5&limit=100000
  ```

---

### 2. Get Unique Values

- **Endpoint:** `GET /sirene/unique_values/{column_name}`
- **Description:**  
  Returns all unique values for a given column.

- **Allowed Column Names:**
  - `setor_nfr`
  - `nfr_code`
  - `nfr_description`
  - `gas`

- **Example Request:**

  Get all available gases in the SIRENE database:
  
  ```
  GET https://api_seeg.carbonprice.top/sirene/unique_values/gas
  ```

- **Response Example:**
  ```json
  {
    "column": "gas",
    "unique_values": ["CO2", "CH4", "N2O", "CO2e_GWP_AR5", ...]
  }
  ```
