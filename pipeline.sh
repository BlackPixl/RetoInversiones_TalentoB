#!/bin/bash

echo "Cargando datos..."
python3 load_data.py
if [ $? -ne 0 ]; then
  echo "Error de ejecución en cargue de datos"
  exit 1
fi

echo "Limpiando datos..."
python3 cleanse_data.py
if [ $? -ne 0 ]; then
  echo "Error de ejecución en limpieza de datos"
  exit 1
fi

echo "fin de la ejecución"