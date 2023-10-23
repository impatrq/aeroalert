
function refreshValues() {
    fetch('/update/info')
        .then(response => response.json())
            .then(jsonObject => {{

            //jsonObject = {'hum': 123123, 'temp': 1231231}
            //const jsonObject = JSON.parse(jsonData);
            // Get the reference to the div where you want to display the content
            const tabla = document.getElementById('tabla-de-valores');

            // Create an unordered list (ul) element to hold the variables and values
            const variableList = document.createElement('ul');

            // Loop through the variables in the JSON object and create list items (li) for each variable
            for (const variableName in jsonObject) {    
                if (jsonObject.hasOwnProperty(variableName)) {
                    const listItem = document.createElement('li');
                    
                    const variableSpan = document.createElement('span');
                    variableSpan.className = 'value';
                    variableSpan.textContent = variableName;
                    
                    const valueSpan = document.createElement('span');
                    valueSpan.textContent = jsonObject[variableName];
                    
                    listItem.appendChild(variableSpan);
                    listItem.appendChild(valueSpan);
                    
                    variableList.appendChild(listItem);
                }
            }
            tabla.appendChild(variableList);
        };})
};        


var vuelos = {
            '12323': {
                'variables': ['Hora', 'bpm_altos1', 'bpm_altos2', 'bpm_bajos1', 'bpm_bajos2', 'dormido1', 'dormido2', 'spo_bajos1', 'spo_bajos2', 'temp_alta1', 'temp_alta2', 'temp_baja1', 'temp_baja2', 'muerte1', 'muerte2', 'manual', 'pulsera_conectada', 'no_reaccion', 'pin_off'], 
                'datos con hora': [
                                    ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                                    ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                                    ], 
                'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}},
            
            '434545': {
                'variables': ['Hora', 'bpm_altos1', 'bpm_altos2', 'bpm_bajos1', 'bpm_bajos2', 'dormido1', 'dormido2', 'spo_bajos1', 'spo_bajos2', 'temp_alta1', 'temp_alta2', 'temp_baja1', 'temp_baja2', 'muerte1', 'muerte2', 'manual', 'pulsera_conectada', 'no_reaccion', 'pin_off'], 
                'datos con hora': [
                                    ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                                    ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                                    ], 
                'alertas': {'alert': 0, 'emergency': 1, 'solicitud': 1, 'sae_desactivado': 1}}}


// Supongamos que tienes un JSON llamado 'vuelos' con la información de los vuelos

// Obtén una referencia a la tabla HTML

function crearTablaVuelos(){
    const listaVuelos = document.getElementById("listaVuelos");
    // por cada vuelo
    for (const vuelo in vuelos) {

        // Crea una fila de tabla <tr> para cada vuelo
        const vueloRow = document.createElement("tr");
        vueloRow.id = `fila-${vuelo}`
        
        // Crea celdas de tabla <td> para cada fila
        
        
        const nroVueloCell = document.createElement("td");
        nroVueloCell.textContent = vuelo;
     

        const statusCell = document.createElement("td");
        if (vuelos[vuelo]['alertas']['emergency'] == 1){
            statusCell.textContent = "emergency"
            statusCell.style.backgroundColor = "red";
        }
        else if (vuelos[vuelo]['alertas']['alert'] == 1){
            statusCell.textContent = "alert"
            statusCell.style.backgroundColor = "yellow";
        }
        else {
            statusCell.textContent = "normal"
            statusCell.style.backgroundColor = "white"
        }
        

        
        const landingCell = document.createElement("td");
        if (vuelos[vuelo]['alertas']['solicitud'] == 1){
            landingCell.textContent = "Waiting"
            landingCell.style.backgroundColor = "yellow";
        }
        else {
            landingCell.textContent = "Done"
            landingCell.style.backgroundColor = "white";
        }
        

        const aesCell = document.createElement("td");
        if (vuelos[vuelo]['alertas']['sae_desactivado'] == 1){
            aesCell.textContent = "Aes Disabled"
            aesCell.style.backgroundColor = "red";
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
    }
}
function actualizarTablaVuelos(vuelos){
    for (const vuelo in vuelos) {
        const fila_de_vuelo = document.getElementById(`fila-${vuelo}`);
        

        if (vuelos[vuelo]['alertas']['emergency'] == 1){
            fila_de_vuelo.cells[1].textContent = "emergency"
            fila_de_vuelo.cells[1].style.backgroundColor = "red";
        }
        else if (vuelos[vuelo]['alertas']['alert'] == 1){
            fila_de_vuelo.cells[1].textContent = "alert"
            fila_de_vuelo.cells[1].style.backgroundColor = "yellow";
        }
        else {
            fila_de_vuelo.cells[1].textContent = "normal"
            fila_de_vuelo.cells[1].style.backgroundColor = "white"
        }



        if (vuelos[vuelo]['alertas']['solicitud'] == 1){
            fila_de_vuelo.cells[2].textContent = "Waiting"
            fila_de_vuelo.cells[2].style.backgroundColor = "yellow";
        }
        else {
            fila_de_vuelo.cells[2].textContent = "Done"
            fila_de_vuelo.cells[2].style.backgroundColor = "white";
        }



        if (vuelos[vuelo]['alertas']['sae_desactivado'] == 1){
            fila_de_vuelo.cells[3].textContent = "Aes Disabled"
            fila_de_vuelo.cells[3].style.backgroundColor = "red";
        }
        else {
            fila_de_vuelo.cells[3].textContent = "Active"
            fila_de_vuelo.cells[3].style.backgroundColor = "green";
        }
    };
}

function createFlights() {
    fetch('/update/flights')
    .then(response => response.json())
        .then(jsonObject => {
            var vuelos = jsonObject
            crearTablaVuelos(vuelos)
        })      
}

//constantemente
function updateFlights() {
    fetch('/update/flights')
    .then(response => response.json())
        .then(jsonObject => {
            var vuelos = jsonObject
            actualizarTablaVuelos(vuelos)
        })      
}



//constantemente se ejecuta
var interfaz = "flights"
var index_flights = 1
var index = 1

function update_key() {
    fetch('/update/keys')
        .then(response => response.json())
            .then(jsonObject => {
                key = jsonObject["key"]
                

                if (interfaz == "flights"){
                    if (key == "2") {       //flecha para arriba
                        if (index_flights != 1){
                            index_flights = index_flights - 1
                            cambiar_vuelo_seleccionado(index_flights)
                            // cuidado al cambiar los datos que no se deseleccione
                            // se tienen que cambiar los datos de la lista ya creada
                            // cantidad de filas segun  el largo de la lista de vuelos
                        }
                    }
                    else if (key == "8"){         //flecha para abajo
                        if (index_flights != max_vuelos){
                            index_flights = index_flights+1
                            cambiar_vuelo_seleccionado(index_flights)
                        }
                    }   

                    else if (key == "6"){         //enter o derecha 
                        cambiar_interfaz("flight", index_flights)
                        interfaz = "flight"
                    }
                    
                }

                else if (interfaz == "flight") {

                    if (key == "4"){                 //para atras o izquierda
                        cambiar_interfaz("flights", index)
                        interfaz = "flights"
                    }
                    else if (key == "6"){        //enter o derecha 
                        cambiar_interfaz("airports", index)
                    }

                    else if (key == "A"){
                        enviar_instruccion("aterriza",index_flights)
                    }
                    else if (inpt == "B"){
                        enviar_instruccion("no aterrizes",index_flights)
                    }
                }

                else if (interfaz == "airports"){
                    if (key == type(int)){              //cualquier numero para seleccionar airport
                        if (key <= max_airport){
                            enviar_airport(inpt)
                            cambiar_interfaz("flights", index_flights)
                            interfaz = "flights"
                        }   
                    }
                    if (key == "A"){
                        enviar_instruccion("aterriza",index_flights)
                    }
                    else if (key == "B"){
                        enviar_instruccion("no aterrizes",index_flights)
                    }
                    if (key== "C"){                   //para cancelar
                        cambiar_interfaz("flight", index_flights)
                        interfaz = "flight"            
                    }
                }

                if (key == "D"){
                    refreshPage()
                }
            })
}





function getVariables() {
    fetch('/get/names/variables')
        .then(response => response.json())
            .then(jsonObject => {
                var variables = jsonObject["variables"]
                return variables
            })
}


function getHistory(nro_vuelo) {
    fetch('/get/history/',nro_vuelo)
    .then(response => response.json())
        .then(jsonObject => {
            var historialVuelo = jsonObject
            //vuelo = {'datos con hora': [
            //                            ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
            //                            ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
            //                            ], 
            //         'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}}
            return historialVuelo
        });
}

function crearTablaDatosHora(nro_vuelo){
    
    // pone los nombres de las variables en la fila de arriba
    var variables = getVariables()      //["hora","bpm_altos"]  
    console.log(variables)
    const headVariables = document.getElementById("variables")
    

    variables.forEach(variable => {
        const variableCelda = document.createElement("th");
        variableCelda.textContent = variable
        variableCelda.style.backgroundColor = "blue"
        headVariables.appendChild(variableCelda);
    });


    // pone los valores con cada color en la tabla
    datos = getHistory(nro_vuelo)
    var datosYHora = datos['datos con hora']

    const tablaDatosHora = document.getElementById("datosHora")

    datosYHora.forEach(filaDatos => {
        console.log(filaDatos)

        const rowTablaDatos = document.createElement("tr")
        var indice = 0

        filaDatos.forEach(dato => {
            indice += 1

            const celdaDatos = document.createElement("td")
            celdaDatos.textContent = dato
            
            if (indice == 1){            // si es la hora
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
        })
        tablaDatosHora.appendChild(rowTablaDatos)
    })
}





function getAirports() {
    fetch('/get/airports')
        .then(response => response.json())
            .then(jsonObject => {

                jsonObject.forEach(function callback(currentValue, index, array) {
                    addToAirportsList(currentValue)
                    //add to list of airports
                    });
            
                });     
}



function sendInstruction(nro_vuelo, instruccion) {
    fetch('/send/',nro_vuelo,'/',instruccion)
    // "aterriza" o "no_aterrizes"
}

function sendInfoAirport(nro_vuelo, index) {
    fetch('/send/',nro_vuelo,'info_airport/',index)

}


            
function refreshDate() {
    var Dia = new Date();
    var m = Dia.getMonth() + 1;
    var mes = (m < 10) ? '0' + m : m;
    var mi = Dia.getMinutes();
    var min = (mi < 10) ? '0' + mi : mi;
    var s = Dia.getSeconds();
    var seg = (s < 10) ? '0' + s : s; 
    var h = Dia.getHours();
    var hour = (h < 10) ? '0' + h : h;
            
    document.getElementById('fecha').textContent = Dia.getDate() +"/"+ mes +"/"+ Dia.getFullYear(); 
    document.getElementById('hora').textContent = hour +":"+ min +":"+ seg;
};

//refreshValues();
refreshDate();
//setInterval(refreshValues, 1000000);
setInterval(refreshDate, 900);

