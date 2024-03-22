FROM continuumio/miniconda
RUN conda update -y conda
RUN conda config --add channels conda-forge
RUN conda install -y gdal rasterio geopandas

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

COPY . .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]