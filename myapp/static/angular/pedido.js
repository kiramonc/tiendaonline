angular
    .module("adminPedido", ['LocalStorageModule'])
    .config(['localStorageServiceProvider', function(localStorageServiceProvider){
        localStorageServiceProvider.setPrefix('ls');
    }])
    .controller("pedidoCtrl", function($http, localStorageService){
        var scope= this;
        if (localStorageService.get("ls.productos")) {
          scope.productos = localStorageService.get("ls.productos");
        } else {
          scope.productos=[];
        }
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

        scope.reset = function(){
            scope.productos=[];
            console.log("Carrito reseteado");
            localStorageService.remove("ls.productos");
        }

        scope.comprobarEstado = function(estado){
            if(estado=="Atendido"){
                return false;
            }
            return true;
        }
    })
