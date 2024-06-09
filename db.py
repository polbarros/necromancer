'''Este archivo contiene la configuración de la base de datos'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# El engine permite a SQLAlquemy comunicarse a la base de datos en un dialecto concreto.
# Con la siguiente línea también creamos la BD en caso de no existir.
engine = create_engine('sqlite:///database/necro.db',
                       connect_args={"check_same_thread": False})

# Advertencia: crear el engine no conecta inmediatamente con la DB, eso lo hacemos luego.

# Ahora creamos la sesión, lo que nos permite realizar transacciones (operaciones) en la DB
'''Desde el punto de vista de SQLAlquemy, una sesión registra una lista de objetos creados, modificados
o eliminados dentro de una misma transacción, de manera que, cuando se confirma la transacción, se reflejan
en la base de datos todas las operaciones involucradas'''
Session = sessionmaker(bind=engine)  # Poner la primera letra en mayúscula para crear una clase temporal.
session = Session()

'''En el fichero models.py, en los modelos (clases), donde queremos que se transformen en tablas, 
le añadiremos esta clase como superclase de los modelos y esto se encargará de mapear y vincular 
cada clase heredera de Base a cada tabla de la BD.'''
Base = declarative_base()
