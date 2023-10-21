//        function refreshValues() {
//            fetch('/update/info')
//                .then(response => response.json())
//                .then(data => {{
//                    console.log(data);
//                    document.getElementById('valorHum').textContent = data.hum;
//                    document.getElementById('valorTemp').textContent = data.temp;
//                }})
//                .catch(error => console.error(error));
//                
    //    };
        
        
            //var tablajson = document.getElementById('tabla-de-valores');

            // Crear una nueva fila
            //var nuevaFila = tablajson.insertRow(-1);

            //Crear las celdas de la nueva fila
            //var celdaNueva = nuevaFila.insertCell(0);


            // Agregar los valores a las celdas
            //celdaNueva.innerHTML = oxigenoSangre;
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



//constantemente se ejecuta
function update_key() {
    fetch('/update/keys')
        .then(response => response.json())
            .then(jsonObject => {
                key = jsonObject["key"]
                
                if (key === "A") {

                }
                else if (key === "B") {

                }
                else if (key === "C") {

                }
                else if (key === "D") {

                }
                else if (key === "1") {

                }
                else if (key === "2") {

                }
                else if (key === "3") {

                }
                else if (key === "4") {

                }
                else if (key === "5") {

                }
                else if (key === "6") {

                }
                else if (key === "7") {

                }
                else if (key === "8") {

                }
                else if (key === "9") {

                }
                else if (key === "0") {

                }
                else if (key === "*") {

                }
                else if (key === "#") {

                }
            })
           
}
// constantemente excepto cuando esta en airports
function update_flights() {
    fetch('/update/flights')
        .then(response => response.json())
            .then(jsonObject => {
                var vuelos = jsonObject
                for (const vuelo in vuelos) {
                    if (vuelos.hasOwnProperty(vuelo)) {
                        console.log(vuelo) // nro de vuelo    
                        console.log(vuelos[vuelo]['alertas'])
                        // poner en lista de vuelos con alertas y eso
                    }
                }
            })      
}




function get_variables() {
    fetch('/get/names/variables')
        .then(response => response.json())
            .then(jsonObject => {
                variables = jsonObjectÑ["variables"]
                
                jsonObject.forEach(function callback(nombre, index, array) {
                    console.log("variable:",nombre)
                //lista con los nombres directamente
                // ponerlos en lista de historial de vuelo
                })
            })
}

function get_history(nro_vuelo) {
    fetch('/get/history/',nro_vuelo)
    .then(response => response.json())
        .then(jsonObject => {

            console.log(jsonObject)
            vuelo = jsonObject
            //para este vuelo historial de vuelo
            //vuelo = {'variables': ['Hora', 'bpm_altos1', 'bpm_altos2', 'bpm_bajos1', 'bpm_bajos2', 'dormido1', 'dormido2', 'spo_bajos1', 'spo_bajos2', 'temp_alta1', 'temp_alta2', 'temp_baja1', 'temp_baja2', 'muerte1', 'muerte2', 'manual', 'pulsera_conectada', 'no_reaccion', 'pin_off'], 
            //    'datos con hora': [
            //              ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
            //              ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
            //              ], 
            //           'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}}

            
            datos_hora = vuelo['datos con hora']    //datos 
            console.log(vuelo['alertas'])       //alertas
            datos_hora.forEach(function callback(currentValue, index, array) {
                console.log(currentValue)
                //add to list of airports
            });
        })
}    




function add_to_airports_list(currentValue) {
    console.log(currentValue)
}
function get_airports() {
    fetch('/get/airports')
        .then(response => response.json())
            .then(jsonObject => {

                jsonObject.forEach(function callback(currentValue, index, array) {
                    add_to_airports_list(currentValue)
                    //add to list of airports
                    });
            
                });     
}



function send_instruction(nro_vuelo, instruccion) {
    fetch('/send/',nro_vuelo,'/',instruccion)
    // "aterriza" o "no_aterrizes"
}

function send_info_airport(nro_vuelo, index) {
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

refreshValues();
refreshDate();
setInterval(refreshValues, 1000000);
setInterval(refreshDate, 900);
