angular
    .module("adminPedido", [])
    .controller("pedidoCtrl", function($http){
        var scope = this;
        scope.productos = [];
        scope.fecha = "";
        scope.cliente = {};
        scope.url = "/pedido_data/"+document.getElementById("url").value;
        $http.get(scope.url).then(function (response) {
            scope.productos = response.data.productos;
            scope.fecha = response.data.fecha;
            scope.cliente = response.data.cliente;
        });

        scope.getTotal = function(){
            var total = 0;
            for(var i = 0; i < scope.productos.length; i++){
                var product = scope.productos[i];
                total += (product.precio * product.unidades);
            }
            return total;
        }


        scope.verDetalle= function(id){
            url = "/pedidos/"+id+"/detalle";
            window.location=url;
        }
    })
