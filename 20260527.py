import heapq
import os
from collections import deque

class RedTransporte:
    def __init__(self):
        # Diccionario para lista de adyacencia: {origen: {destino: minutos}}
        self.grafo = {}

    def cargar_red(self, archivo):
        """Carga la red desde un archivo de texto."""
        if not os.path.exists(archivo):
            print(f"Aviso: El archivo '{archivo}' no existe aún. Se creará al guardar.")
            return

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                lineas_cargadas = 0
                for linea in f:
                    linea = linea.strip()
                    if not linea: 
                        continue
                    partes = linea.split(',')
                    if len(partes) != 3:
                        continue # Ignorar líneas mal formadas
                    
                    # Usamos .title() para normalizar los nombres desde el archivo
                    origen = partes[0].strip().title()
                    destino = partes[1].strip().title()
                    minutos_str = partes[2].strip()
                    
                    try:
                        minutos = int(minutos_str)
                        if minutos > 0:
                            self.anadir_estacion(origen)
                            self.anadir_estacion(destino)
                            self._insertar_conexion(origen, destino, minutos)
                            lineas_cargadas += 1
                    except ValueError:
                        print(f"Error: Tiempo inválido en la línea '{linea}'.")
                        
            print(f"Red cargada correctamente. ({lineas_cargadas} conexiones).")
        except Exception as e:
            print(f"Error crítico al cargar el archivo: {e}")

    def guardar_red(self, archivo):
        """Guarda la red actual en un archivo de texto."""
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for origen, conexiones in self.grafo.items():
                    for destino, minutos in conexiones.items():
                        f.write(f"{origen},{destino},{minutos}\n")
            print("Red guardada correctamente en el archivo.")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def anadir_estacion(self, estacion):
        """Añade una nueva estación al grafo si no existe."""
        if estacion not in self.grafo:
            self.grafo[estacion] = {}
            return True
        return False

    def _insertar_conexion(self, origen, destino, minutos):
        """Método interno para insertar conexión sin imprimir mensajes."""
        self.grafo[origen][destino] = minutos

    def anadir_conexion(self, origen, destino, minutos):
        """Añade o actualiza una conexión validando los datos."""
        if origen not in self.grafo or destino not in self.grafo:
            print("Error: Ambas estaciones deben estar registradas antes de conectarlas.")
            return False
        
        if origen == destino:
            print("Error: El origen y destino no pueden ser la misma estación.")
            return False

        if minutos <= 0:
            print("Error: El tiempo de viaje debe ser un número positivo.")
            return False
        
        if destino in self.grafo[origen]:
            print(f"Aviso: La conexión {origen}->{destino} ya existía. Actualizando tiempo de {self.grafo[origen][destino]} a {minutos} min.")
        else:
            print(f"Conexión {origen}->{destino} añadida exitosamente.")
            
        self._insertar_conexion(origen, destino, minutos)
        return True

    def ver_estaciones(self):
        """Muestra todas las estaciones y sus conexiones directas."""
        if not self.grafo:
            print("La red de transporte está vacía.")
            return
        
        print("\n--- Estaciones y Conexiones ---")
        for estacion, conexiones in self.grafo.items():
            if not conexiones:
                print(f"[{estacion}] -> Sin conexiones de salida")
            else:
                conexiones_str = ", ".join([f"{dest} ({mins}m)" for dest, mins in conexiones.items()])
                print(f"[{estacion}] -> {conexiones_str}")

    def _calcular_dijkstra(self, origen, destino):
        """Método privado que ejecuta Dijkstra y retorna (camino_lista, tiempo_total)."""
        if origen not in self.grafo or destino not in self.grafo:
            return None, float('inf')

        cola_prioridad = [(0, origen)]
        tiempos_minimos = {nodo: float('inf') for nodo in self.grafo}
        tiempos_minimos[origen] = 0
        rutas = {nodo: [] for nodo in self.grafo}
        rutas[origen] = [origen]
        visitados = set()

        while cola_prioridad:
            tiempo_actual, nodo_actual = heapq.heappop(cola_prioridad)

            if nodo_actual in visitados:
                continue
                
            visitados.add(nodo_actual)

            if nodo_actual == destino:
                break

            for vecino, tiempo_viaje in self.grafo[nodo_actual].items():
                if vecino in visitados:
                    continue
                
                nuevo_tiempo = tiempo_actual + tiempo_viaje
                if nuevo_tiempo < tiempos_minimos[vecino]:
                    tiempos_minimos[vecino] = nuevo_tiempo
                    rutas[vecino] = rutas[nodo_actual] + [vecino]
                    heapq.heappush(cola_prioridad, (nuevo_tiempo, vecino))

        if tiempos_minimos[destino] == float('inf'):
            return None, float('inf')
        return rutas[destino], tiempos_minimos[destino]

    def dijkstra(self, origen, destino):
        """Muestra la ruta más rápida estándar entre dos estaciones."""
        camino, tiempo = self._calcular_dijkstra(origen, destino)
        if camino is None:
            print(f"No existe una ruta posible entre {origen} y {destino}.")
        else:
            camino_formateado = " -> ".join(camino)
            print(f"\nRuta más rápida encontrada:")
            print(f"Recorrido: {camino_formateado}")
            print(f"Tiempo total: {tiempo} minutos")

    def dijkstra_con_intermedia(self, origen, intermedia, destino):
        """Calcula la ruta obligando al trayecto a pasar por una estación intermedia."""
        if origen not in self.grafo or intermedia not in self.grafo or destino not in self.grafo:
            print("Error: Una o más estaciones especificadas no existen en la red.")
            return

        # Tramo 1: Origen -> Intermedia
        camino1, tiempo1 = self._calcular_dijkstra(origen, intermedia)
        if camino1 is None:
            print(f"No es posible viajar desde {origen} hasta la estación intermedia {intermedia}.")
            return

        # Tramo 2: Intermedia -> Destino
        camino2, tiempo2 = self._calcular_dijkstra(intermedia, destino)
        if camino2 is None:
            print(f"No es posible viajar desde la estación intermedia {intermedia} hasta el destino {destino}.")
            return

        # Combinamos los caminos evitando duplicar la estación intermedia en el medio
        camino_completo = camino1 + camino2[1:]
        tiempo_total = tiempo1 + tiempo2

        print(f"\nRuta más rápida con parada obligatoria en {intermedia}:")
        print(f"Recorrido: {' -> '.join(camino_completo)}")
        print(f"Tiempo total: {tiempo_total} minutos ({tiempo1}m hasta parada + {tiempo2}m hasta destino)")

    def estan_conectadas(self, origen, destino):
        """Comprueba si existe algún camino (directo o indirecto) usando BFS."""
        if origen not in self.grafo or destino not in self.grafo:
            print("Error: Una o ambas estaciones no existen en la red.")
            return False

        visitados = set()
        cola = deque([origen])

        while cola:
            nodo_actual = cola.popleft()
            
            if nodo_actual == destino:
                return True
                
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                for vecino in self.grafo[nodo_actual]:
                    if vecino not in visitados:
                        cola.append(vecino)
                        
        return False

def mostrar_menu():
    print("\n" + "="*40)
    print(" MENÚ: PLANIFICADOR DE RUTAS")
    print("="*40)
    print("1. Cargar red desde archivo")
    print("2. Añadir estacion")
    print("3. Añadir conexion")
    print("4. Ver estaciones y conexiones")
    print("5. Ruta mas rapida entre dos estaciones")
    print("6. Estan conectadas dos estaciones?")
    print("7. Ruta mas rapida pasando por estacion intermedia")
    print("8. Guardar y salir")
    print("="*40)

def mostrar_estaciones_disponibles(red):
    """Función de ayuda para listar las ciudades antes de pedir un input."""
    estaciones = list(red.grafo.keys())
    if not estaciones:
        print("\n[Aviso] Aún no hay estaciones registradas en la red.")
        return False
    
    print("\n--- Ciudades Disponibles ---")
    print(", ".join(estaciones))
    print("----------------------------")
    return True

def main():
    red = RedTransporte()
    archivo_datos = "red_transporte.txt"
    
    print("Inicializando sistema...")
    red.cargar_red(archivo_datos)

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-8): ").strip()

        try:
            if opcion == '1':
                archivo = input(f"Nombre del archivo (Enter para usar '{archivo_datos}'): ").strip()
                if not archivo: archivo = archivo_datos
                red.cargar_red(archivo)

            elif opcion == '2':
                est = input("Nombre de la nueva estación: ").strip().title()
                if not est:
                    print("Error: El nombre no puede estar vacío.")
                elif red.anadir_estacion(est):
                    print(f"Estación '{est}' añadida correctamente.")
                else:
                    print("La estación ya existe.")

            elif opcion == '3':
                if mostrar_estaciones_disponibles(red):
                    origen = input("Estación de origen: ").strip().title()
                    destino = input("Estación de destino: ").strip().title()
                    try:
                        minutos = int(input("Minutos de viaje: ").strip())
                        red.anadir_conexion(origen, destino, minutes=minutos)
                    except ValueError:
                        print("Error: Debes introducir un número entero para los minutos.")

            elif opcion == '4':
                red.ver_estaciones()

            elif opcion == '5':
                if mostrar_estaciones_disponibles(red):
                    origen = input("Estación de origen: ").strip().title()
                    destino = input("Estación de destino: ").strip().title()
                    red.dijkstra(origen, destino)

            elif opcion == '6':
                if mostrar_estaciones_disponibles(red):
                    origen = input("Estación de origen: ").strip().title()
                    destino = input("Estación de destino: ").strip().title()
                    conectadas = red.estan_conectadas(origen, destino)
                    if conectadas:
                        print(f"Sí, hay un camino que conecta {origen} con {destino}.")
                    else:
                        print(f"No, no existe conexión posible entre {origen} y {destino}.")

            elif opcion == '7':
                if mostrar_estaciones_disponibles(red):
                    origen = input("Estación de origen: ").strip().title()
                    intermedia = input("Estación intermedia obligatoria: ").strip().title()
                    destino = input("Estación de destino: ").strip().title()
                    red.dijkstra_con_intermedia(origen, intermedia, destino)

            elif opcion == '8':
                red.guardar_red(archivo_datos)
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción inválida. Por favor, introduce un número del 1 al 8.")
                
        except Exception as e:
            print(f"Se ha producido un error inesperado: {e}")

if __name__ == "__main__":
    main()