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
        scope.prod = [];
        scope.pedido = {};
        scope.cliente = {};
        scope.url = "/pedido_data/"+document.getElementById("url").value;
        $http.get(scope.url).then(function (response) {
            scope.prod = response.data.productos;
            scope.pedido = response.data.pedido;
            scope.cliente = response.data.cliente;
        });

        scope.getTotal = function(){
            var total = 0;
            for(var i = 0; i < scope.prod.length; i++){
                var product = scope.prod[i];
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
            if(estado==1){
                return false;
            }
            return true;
        }
    })
    .filter('estadoPedido', function(){
        return function(input){
            if(input == 0){
                return "En espera";
            }else{
                return "Atendido";
            }
        }
    })
    .filter('estadoUser', function(){
        return function(input){
            console.log(input)
            if(input == true){
                return "Activo";
            }else{
                return "Inactivo";
            }
        }
    });

angular
    .module("lPedido", ['LocalStorageModule'])
    .config(['localStorageServiceProvider', function(localStorageServiceProvider){
        localStorageServiceProvider.setPrefix('ls');
    }])
    .controller("pController", function($http, localStorageService){
        var scope= this;
        if (localStorageService.get("ls.productos")) {
          scope.productos = localStorageService.get("ls.productos");
        } else {
          scope.productos=[];
        }
        scope.productos = [];
        scope.pedidos = [];

        scope.url = "/pedidos_get";
        $http.get(scope.url).then(function (response) {
            scope.pedidos = response.data.pedidos;
            console.log(scope.pedidos)
        });

        scope.verDetalle= function(id){
            url = "/pedidos/"+id+"/detalle";
            window.location=url;
        }

        scope.reset = function(){
            scope.productos=[];
            console.log("Carrito reseteado");
            localStorageService.remove("ls.productos");
        }
    })
    .filter('estadoPedido', function(){
        return function(input){
            if(input == 0){
                return "En espera";
            }else{
                return "Atendido";
            }
        }
    });

angular
    .module("listPedidoAdmin", [])
    .controller("pCtrl", function($scope, $http){
        $scope.pedidos = [];
        $scope.buscar = 0;
        $http.get("/pedidos_data").then(function (response) {
            $scope.pedidos = response.data.pedidos;
        });

        $scope.noAtendidos = function(){
            $scope.buscar= 1;
        }
        $scope.atendidos = function(){
            $scope.buscar= 2;
        }
        $scope.nofiltrar = function(){
            $scope.buscar= 0;
        }
        $scope.predicate = 'fecha';
        $scope.reverse = true;
        $scope.order = function (por){
            if($scope.predicate === por){
                $scope.reverse = !$scope.reverse;
            }else{
                $scope.reverse = false;
            }
            $scope.predicate = por;
        }
    })
    .filter('uncheck', function(){
        return function(input, argum){
            var out = [];
            angular.forEach(input, function(p){
                if(argum==1){
                    if(p.estado != 1){
                        out.push(p);
                    }
                }else{
                    if(argum==2){
                        if(p.estado == 1){
                            out.push(p);
                        }
                    }else{
                        out.push(p);
                    }
                }
            })
            return out;
        }
    })
    .filter('estadoPedido', function(){
        return function(input){
            if(input == 0){
                return "En espera";
            }else{
                return "Atendido";
            }
        }
    });
