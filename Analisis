La base de datos que he usado para el grafo son los diccionarios porque permiten buscar o añadir estaciones en tiempo O(1). Tambien he usado sets para los
nodos visitados porque su búsqueda interna también es O(1).Además, heapq optimiza Dijkstra extrayendo el mínimo en O(logV), y deque agiliza el BFS.

La complejidad temporal, para añadir una conexión se usa O(1) ya que se inserta directamente en el diccionario. El algoritmo de Dijkstra usa O((V + E) \log V), 
siendo vértices (V) y aristas (E) con el heap, y comprobar la conectividad (BFS) O(V + E).

En la complejidad espacial, el grafo ocupa O(V + E) en memoria, ya que el espacio crece de forma proporcional a la cantidad de ciudades y rutas ya registradas.

Para mejorar, estaría bien que las rutas creadas fueran de ida y vuelta por defecto.
