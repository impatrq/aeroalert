
//var vuelos = {
//            '12323': {
//                'datos con hora': [
//                                    ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
//                                    ], 
//                'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}},
//            
//            '434545': {
//                'datos con hora': [
//                                    ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
//                                    ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
//                                    ], 
//                'alertas': {'alert': 0, 'emergency': 1, 'solicitud': 1, 'sae_desactivado': 1}}}


// Supongamos que tienes un JSON llamado 'vuelos' con la información de los vuelos

// Obtén una referencia a la tabla HTML
//------------------------------------------------------------------
AbortSignal.timeout ??= function timeout(ms) {
    const ctrl = new AbortController()
    setTimeout(() => ctrl.abort(), ms)
    return ctrl.signal
}
  

function crearTablaVuelos(flights){
    const listaVuelos = document.getElementById("listaVuelos");
    // por cada vuelo
    for (const flight in flights) {
        var audioAlert = document.getElementById("audioAlert");
        var audioEmergency = document.getElementById("audioEmergency");
        
        // Crea una fila de tabla <tr> para cada flight
        const vueloRow = document.createElement("tr");
        vueloRow.id = `fila-${flight}`
        
        // Crea celdas de tabla <td> para cada fila
        
        
        const nroVueloCell = document.createElement("td");
        nroVueloCell.textContent = flight;
     
        
        const statusCell = document.createElement("td");
        if (flights[flight]["alertas"]['emergency'] == 1){
            statusCell.textContent = "Emergency"
            statusCell.style.backgroundColor = "red";
            audioEmergency.play()
        }
        else if (flights[flight]["alertas"]['alert'] == 1){
            statusCell.textContent = "Alert"
            statusCell.style.backgroundColor = "yellow";
            audioAlert.play()
        }
        else {
            statusCell.textContent = "Normal"
            statusCell.style.backgroundColor = "white"
        }
        

        
        const landingCell = document.createElement("td");
        if (flights[flight]["alertas"]['solicitud'] == 1){
            landingCell.textContent = "Waiting"
            landingCell.style.backgroundColor = "yellow";
        }
        else {
            landingCell.textContent = "Done"
            landingCell.style.backgroundColor = "white";
        }
        

        const aesCell = document.createElement("td");
        if (flights[flight]["alertas"]['sae_desactivado'] == 1){
            aesCell.textContent = "Aes Disabled"
            aesCell.style.backgroundColor = "red";
            //audioEmergency.play()
        }
        else {
            aesCell.textContent = "Active"
            aesCell.style.backgroundColor = "green";
        }

        
        // Agrega las celdas a la fila
        vueloRow.appendChild(nroVueloCell);
        vueloRow.appendChild(statusCell);
        vueloRow.appendChild(landingCell);
        vueloRow.appendChild(aesCell);

        // Agrega la fila a la tabla
        listaVuelos.appendChild(vueloRow);

        cambiarVueloSeleccionado(0)
    }
}

function actualizarTablaVuelos(flights){
    var audioAlert = document.getElementById("audioAlert");
    var audioEmergency = document.getElementById("audioEmergency");
    //{'12323': {'alert': 1, 'emergency': 0, 'solicitud': 0, 'sae_desactivado': 1},
    // '122324324': {'alert': 1, 'emergency': 0, 'solicitud': 0, 'sae_desactivado': 1}}
    for (const flight in flights) {

        const fila_de_vuelo = document.getElementById(`fila-${flight}`);
        

        if (flights[flight]["alertas"]['emergency'] == 1){
            fila_de_vuelo.cells[1].textContent = "Emergency"
            fila_de_vuelo.cells[1].style.backgroundColor = "red";
            audioEmergency.play()
        }
        else if (flights[flight]["alertas"]['alert'] == 1){
            fila_de_vuelo.cells[1].textContent = "Alert"
            fila_de_vuelo.cells[1].style.backgroundColor = "yellow";
            audioAlert.play()
        }
        else {
            fila_de_vuelo.cells[1].textContent = "Normal"
            fila_de_vuelo.cells[1].style.backgroundColor = "white"
        }



        if (flights[flight]["alertas"]['solicitud'] == 1){
            fila_de_vuelo.cells[2].textContent = "Waiting"
            fila_de_vuelo.cells[2].style.backgroundColor = "yellow";
        }
        else {
            fila_de_vuelo.cells[2].textContent = "Done"
            fila_de_vuelo.cells[2].style.backgroundColor = "white";
        }



        if (flights[flight]["alertas"]['sae_desactivado'] == 1){
            fila_de_vuelo.cells[3].textContent = "AES Disabled"
            fila_de_vuelo.cells[3].style.backgroundColor = "red";
            audioEmergency.play()
        }
        else {
            fila_de_vuelo.cells[3].textContent = "Active"
            fila_de_vuelo.cells[3].style.backgroundColor = "green";
        }
    };
}

var vuelos
//una vez
function createFlights() {
    fetch('/update/flights', { signal: AbortSignal.timeout(5000) })
    .then(response => response.json())
        .then(jsonObject => {
            //{'12323': {'alert': 1, 'emergency': 0, 'solicitud': 0, 'sae_desactivado': 1},
            // '122324324': {'alert': 1, 'emergency': 0, 'solicitud': 0, 'sae_desactivado': 1}}
            vuelos = jsonObject
            console.log("create flights: ", vuelos)

            crearTablaVuelos(jsonObject)
            
        })      
}
createFlights()


function updateFlights() {
    fetch('/update/flights', { signal: AbortSignal.timeout(5000) })
    .then(response => response.json())
        .then(jsonObject => {
            actualizarTablaVuelos(jsonObject)

            vuelos = jsonObject
            console.log("update flights: ", vuelos)

            return jsonObject
        })      
}

setInterval(() => {
    updateFlights()
}, 5000);
//--------------------------------------------------------------------------


function cambiarVueloSeleccionado(indiceVuelo){
    
    const tableFlights = document.getElementById("listaVuelos");
    var rows = tableFlights.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++){
        if (rows[indiceVuelo] == rows[i]){
            rows[indiceVuelo].style = "border: 3px solid black;"
            continue
        }
        else{
            rows[i].style= "border:none;"
        }
    }
}

//----------------------------------------------




function crearTablaDatosHora(nro_vuelo){
    // pone los nombres de las variables en la fila de arriba
    //["hora","bpm_altos"] 
    fetch('/get/names/variables', { signal: AbortSignal.timeout(5000) })
        .then(response => response.json())
            .then(jsonObject => {
                var variables = jsonObject["variables"]
                
                const headVariables = document.getElementById("variables")
                headVariables.innerHTML = ""
                
                variables.forEach(variable => {
                    const variableCelda = document.createElement("th");
                    variableCelda.textContent = variable
                    variableCelda.style.backgroundColor = "blue"
                    headVariables.appendChild(variableCelda);
                });


                // pone los valores con cada color en la tabla
                // despues de poner los nombres de las variables agrega los datos
                fetch('/get/history/'+ String(nro_vuelo), { signal: AbortSignal.timeout(4000) })
                    .then(respuesta => respuesta.json())
                        .then(respuestaJson => {
                            //vuelo = {'datos con hora': [
                            //                            ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                            //                            ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                            //                            ], 
                            //         'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}}
                            datos = respuestaJson
                            const dataTiempo = datos['datos con hora']
                            const datosYHora = dataTiempo.reverse()

                            const tablaDatosHora = document.getElementById("datosHora")
                            tablaDatosHora.innerHTML = ""

                            datosYHora.forEach(filaDatos => {

                                const rowTablaDatos = document.createElement("tr")
                                var indice = 0

                                filaDatos.forEach(dato => {
                                    indice += 1

                                    const celdaDatos = document.createElement("td")
                                    
                                    celdaDatos.textContent = dato
                                    if (indice == 1){
                                        celdaDatos.style.backgroundColor = "orange"
                                    }
                                    else if (indice == 17){      // si es el de pulsera conectada
                                        if (dato == 0){
                                            celdaDatos.style.backgroundColor = "red"
                                        }
                                        else {
                                            celdaDatos.style.backgroundColor = "green"
                                        }
                                    }
                                    else if (dato == 1){
                                        celdaDatos.style.backgroundColor = "red"
                                    }
                                    else{
                                        celdaDatos.style.backgroundColor = "green"
                                    }

                                    rowTablaDatos.appendChild(celdaDatos)
                                });

                            tablaDatosHora.appendChild(rowTablaDatos)
                            }); 
                        });
            });
}

//------------------------------------------
var airportsQuantity = 0
function crearTablaAirports() {
    fetch('/get/airports', { signal: AbortSignal.timeout(5000) })
        .then(response => response.json())
            .then(jsonObject => {
                console.log("get aeropuertos respuesta: ", jsonObject)
                
                //{"airports":[ {"nombre":"Ezeiza", "coordenadas": ["34°49'25″, 58°31'44″"]},
                //              {"nombre":"Aeroparque", "coordenadas": ["34°33'27″ 58°24'43″"]} ] }
                const response = jsonObject['airports']
                
                
                aeropuertos = response
                airportsQuantity = aeropuertos.length;
                // [ {"nombre":"Ezeiza", "coordenadas": ["34°49'25″, 58°31'44″"]},
                //   {"nombre":"Aeroparque", "coordenadas": ["34°33'27″ 58°24'43″"]} ]
                const tableAeropuertos= document.getElementById("tablaAeropuertos")
                indiceAirport = 0
                aeropuertos.forEach(aeropuerto => {
                    
                    const filaAeropuerto = document.createElement("tr")
                    var nombreAeropuerto = aeropuerto["nombre"]
                    var coordsAeropuerto = aeropuerto["coordenadas"]
                    
                    indiceAirport += 1
                    const index = document.createElement("td")
                    index.textContent = indiceAirport
                    const airNombre = document.createElement("td")
                    airNombre.textContent = nombreAeropuerto
                    const airCoords = document.createElement("td")
                    airCoords.textContent = coordsAeropuerto

                    
                    filaAeropuerto.appendChild(index)
                    filaAeropuerto.appendChild(airNombre)
                    filaAeropuerto.appendChild(airCoords)


                    tableAeropuertos.appendChild(filaAeropuerto)
                });
            });
}

crearTablaAirports()

//---------------------------------------------------------------------------------



function cambiarInterfaz(nuevaInterfaz,nro_vuelo){
    displayFlights = document.getElementById("VUELOS")
    displayHistory = document.getElementById("HISTORY")
    displayAirports = document.getElementById("AIRPORTS")
    if (nuevaInterfaz == "flights"){
        displayFlights.style = "display:;"
        displayHistory.style = "display:none;"
        displayAirports.style = "display:none;"
    }
    else if (nuevaInterfaz == "flight"){
        crearTablaDatosHora(nro_vuelo)
        displayHistory.style = "display:;"
        displayFlights.style = "display:none;"
        displayAirports.style = "display:none;"
    }
    else if (nuevaInterfaz == "airports"){
        displayAirports.style = "display:;"
        displayFlights.style = "display:none;"
        displayHistory.style = "display:none;"
    }
}





//done
function sendInstruction(nro_vuelo, instruccion) {
    fetch('/send/'+nro_vuelo+'/'+instruccion)
    console.log("enviado:", nro_vuelo, "instruccion:", instruccion)
    return
}

function sendInfoAirport(nro_vuelo, index) {
    fetch('/send/'+nro_vuelo+'/info_airport/'+index)
    console.log("enviado:", nro_vuelo, "indice:", index)
    return
}


var interfaz = "flights"
var index_flights = 0



//constantemente se ejecuta
function getKey() {
    fetch('/get/key', { signal: AbortSignal.timeout(2000) })
        .then(response => response.json())
            .then(jsonObject => {
                console.log('\n\n')
                key = jsonObject["key"]
                console.log("key: ",key)
            
                console.log("index flights: ", index_flights)
                const nros_vuelo = Object.keys(vuelos) 
                const nro_vuelo = nros_vuelo[index_flights]
                console.log("nro_vuelo: ", nro_vuelo)


                //no tienee que ser esto sino el nro del vuelo tipo keyname o algo asi
                //{'datos con hora': [
                //                    ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                //                   ], 
                //        'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}}
    
                
                if (key != ""){
                    if (interfaz == "flights"){
                        if (key == "C") {       //flecha para arriba
                            if (index_flights > 0){
                                index_flights = index_flights - 1
                                cambiarVueloSeleccionado(index_flights)    
                            }
                        }
                        else if (key == "D"){         //flecha para abajo
                            if (index_flights <  ((nros_vuelo.length)-1)){
                                index_flights = index_flights+1
                                cambiarVueloSeleccionado(index_flights)
                            }
                        }  

                        else if (key == "#"){         //enter o derecha 
                            cambiarInterfaz("flight", nro_vuelo)
                            interfaz = "flight"
                        }
                    }

                    else if (interfaz == "flight") {

                        if (key == "*"){                 //para atras o izquierda
                            cambiarInterfaz("flights")
                            interfaz = "flights"
                        }
                        else if (key == "#"){        //enter o derecha 
                            cambiarInterfaz("airports")
                            interfaz = "airports"
                        }

                        else if (key == "A"){
                            sendInstruction(nro_vuelo, "aterriza")
                            cambiarInterfaz("airports")
                            interfaz = "airports"
                        }
                        else if (key == "B"){
                            sendInstruction(nro_vuelo, "no aterrizes")
                        }
                    }

                    else if (interfaz == "airports"){
                        console.log("cantidad de aeropuertos: ", airportsQuantity)
                        if (!isNaN(key)){               //cualquier numero para seleccionar airport
                            if (key <= airportsQuantity){
                                var indice = key-1
                                sendInfoAirport(nro_vuelo, indice)   //en la tabla se muestran con un indice mayor
                                cambiarInterfaz("flights")
                                interfaz = "flights"
                            }   
                        }
                        else if (key == "A"){
                            sendInstruction(nro_vuelo, "aterriza")
                        }
                        else if (key == "B"){
                            sendInstruction(nro_vuelo,"no aterrizes")
                        }

                        else if (key== "*"){                   //para cancelar
                            cambiarInterfaz("flight", nro_vuelo)
                            interfaz = "flight"            
                        }
                    }

                    if (key == "0"){
                        location.reload()               //recargar la pagina
                    }
                }
            });

}
console.log("por hacer getKey")
setInterval(getKey, 3000);




