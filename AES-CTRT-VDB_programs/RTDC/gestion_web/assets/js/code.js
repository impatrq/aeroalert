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
            })
}
// constantemente excepto cuando esta en airports
function update_flights() {
    fetch('/update/flights')
        .then(response => response.json())
            .then(jsonObject => {

            })
}




function get_variables() {
    fetch('/get/names/variables')
        .then(response => response.json())
            .then(jsonObject => {

            })
}

function get_history(nro_vuelo) {
    fetch('get/history/',nro_vuelo)
    .then(response => response.json())
        .then(jsonObject => {

    })    
}

function get_airports() {
    fetch('/get/airports')
        .then(response => response.json())
            .then(jsonObject => {
                jsonObject.forEach(element => {
                    //append a loista
                }); 
            })    
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

