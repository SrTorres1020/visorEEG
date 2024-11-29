import mne
import numpy as np
import mysql.connector
import time

def conectar_a_base_datos():
    """
    Establece una conexión a la base de datos SQL y retorna el objeto de conexión y el cursor.
    Returns:
        connection: Objeto de conexión si es exitosa, None en caso contrario.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="visualizador_eeg"
        )
        
        if connection.is_connected():
            print("Conectado a la base de datos.")
            return connection
        else:
            raise mysql.connector.Error("No se pudo conectar a la base de datos.")
    
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

import numpy as np

def guardar_datos_en_base_de_datos(datos_procesados, frecuencias, enfermedad_id):
    """
    Inserta los datos procesados directamente en la base de datos usando listas y diccionarios.
    """
    connection = conectar_a_base_datos()

    if connection:
        start_time = time.time()
        
        try:
            mycursor = connection.cursor()
            connection.start_transaction()

          
            fecha_sesion = datos_procesados['fecha']
            intervalo = float(datos_procesados['intervalo']) if isinstance(datos_procesados['intervalo'], np.float64) else datos_procesados['intervalo']

            
            mycursor.execute('''
                INSERT INTO api_paciente (nombre_paciente, enfermedad_ID)
                VALUES ('Paciente', %s )
            ''',(
                enfermedad_id,
            ))
            paciente_actual = mycursor.lastrowid

       
            mycursor.execute('''
                INSERT INTO api_sesion (fecha_sesion, paciente_ID, intervalo)
                VALUES (%s, %s, %s)
            ''', (
                fecha_sesion,
                paciente_actual,
                intervalo
            ))

            sesion_actual = mycursor.lastrowid

           
            canal_inserts = [(canal, sesion_actual) for canal in datos_procesados['canales']]
            mycursor.executemany('''
                INSERT INTO api_canal (nombre_canal, sesion_ID)
                VALUES (%s, %s)
            ''', canal_inserts)

        
            mycursor.execute("SELECT id, nombre_canal FROM api_canal WHERE sesion_ID = %s", (sesion_actual,))
            canal_ids = {canal: id for id, canal in mycursor.fetchall()}

           
            frecuencia_inserts = []
            for canal, frecuencia in zip(datos_procesados['canales'], frecuencias):
                for valor in frecuencia.values():
                    frecuencia_inserts.append((valor, canal_ids[canal]))

            mycursor.executemany('''
                INSERT INTO api_frecuencia (frecuencia, canal_iD)
                VALUES (%s, %s)
            ''', frecuencia_inserts)

            connection.commit()  
        
        except mysql.connector.Error as err:
            print(f"Error al guardar los datos: {err}")
            connection.rollback() 
        finally:
            mycursor.close()  
            connection.close()  
        
        elapsed_time = time.time() - start_time
        print(f"Tiempo de ejecución de la función: {elapsed_time:.2f} segundos")
    else:
        print("No se pudo conectar a la base de datos. No se guardaron los datos.")

def cargar_archivo_edf(ruta_archivo):
    """
    Carga un archivo EDF y extrae los datos relevantes.
    Args:
        ruta_archivo (str): Ruta al archivo EDF.
    Returns:
        dict: Diccionario con datos relevantes del archivo EDF.
    """
    datos_raw = mne.io.read_raw_edf(ruta_archivo, preload=True)

    datos = {
        'frecuencias': datos_raw.get_data(),  
        'canales': datos_raw.ch_names, 
        'unidades': datos_raw._orig_units, 
        'duracion': datos_raw.n_times / datos_raw.info['sfreq'],  
        'intervalo': datos_raw.times[1] - datos_raw.times[0], 
        'fecha': datos_raw.info['meas_date']  
    }

   
    datos['frecuencias'] = datos['frecuencias'].tolist()

  
    frecuencias_lista = []
    for canal_index, canal in enumerate(datos['canales']):
        frecuencias_canal = datos['frecuencias'][canal_index]
        frecuencias_diccionario = {f"punto_{i}": valor for i, valor in enumerate(frecuencias_canal)}
        frecuencias_lista.append(frecuencias_diccionario)

    return {
        'frecuencias': frecuencias_lista,  
        'canales': datos['canales'],  
        'unidades': datos['unidades'],  
        'duracion': datos['duracion'],  
        'intervalo': datos['intervalo'],  
        'fecha': datos['fecha']  
    }


