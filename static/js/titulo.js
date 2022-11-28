onload = function() {
    document.getElementById('id_title').addEventListener('keyup', function(e) {
        // recupera o campo username do formulário
        var campoTitulo = document.getElementById('id_title');
        // cria o objeto HTTP Request e abre a conexão
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "{% url 'verificaTitulo' %}?titulo=" +
            encodeURIComponent(campoTitulo.value), true);
        // Função de callback
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var resposta = JSON.parse(xmlhttp.responseText);
                if (resposta.existe) {
                    campoTitulo.style = "border: 4px solid #FF0000";
                    document.getElementById('idMsgErro').replaceChild(document.createTextNode("Título já existe"),
                        document.getElementById('idMsgErro').firstChild);
                } else {
                    campoTitulo.style = "border: 4px solid #00FF00";
                    document.getElementById('idMsgErro').replaceChild(document.createTextNode("OK"),
                        document.getElementById('idMsgErro').firstChild);
                }
            }
        };
        // Envia o Request
        xmlhttp.send(null);
    });
}