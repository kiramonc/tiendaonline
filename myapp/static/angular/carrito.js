function efecto(){
    var carritoB = document.getElementById("carritoButton");
    $("#carritoButton").addClass("tada");
    carritoB.addEventListener("animationend", function(){
        $("#carritoButton").removeClass("tada");
    }, false);
}

function unidadModificada(nodo){
    var nodoTd = nodo.parentNode.parentNode;
    $(nodoTd).addClass("warning");
    var pedidoB = document.getElementById("pedidoButton");
    pedidoB.setAttribute("disabled", "disabled");
    var establecerB = document.getElementById("establecerButton");
    establecerB.removeAttribute("disabled");
}

angular
    .module("adminCarrito", ['LocalStorageModule'])
    .config(['localStorageServiceProvider', function(localStorageServiceProvider){
        localStorageServiceProvider.setPrefix('ls');
    }])
    .controller("carritoCtrl", function($scope, localStorageService, save){

        if (localStorageService.get("ls.productos")) {
          $scope.productos = localStorageService.get("ls.productos");
        } else {
          $scope.productos=[];
        }

        $scope.agregar = function (data, precio, stock) {
            $scope.productos.push({"nombre": data, "precio": precio, "stock": stock, "unidad": 1});
            localStorageService.set("ls.productos", $scope.productos);
            efecto();
        };

        $scope.eliminar = function (indice) {
            $scope.productos.splice(indice, 1)
            localStorageService.set("ls.productos", $scope.productos);
        };

        $scope.editar = function () {
            localStorageService.set("ls.productos", $scope.productos);
            var nodoTd= document.getElementsByTagName("tr");
            $(nodoTd).removeClass("warning");
            var pedidoB = document.getElementById("pedidoButton");
            pedidoB.removeAttribute("disabled");
            var establecerB = document.getElementById("establecerButton");
            establecerB.setAttribute("disabled", "disabled");
        };

        $scope.enviar = function (data) {
            save.doPedido($scope.productos).then(function(res){
                console.log("carga terminada");
                $scope.productos=[];
                localStorageService.remove("ls.productos");
            })
        };

        $scope.redireccionar = function(data){
            var url = "/products/"+$scope.productos[data]["nombre"]
            window.location=url;
        }

        $scope.reset = function(){
            console.log("Carrito reseteado");
            $scope.productos=[];
            localStorageService.remove("ls.productos");
        }

    })
    .service('save', ["$http", "$q", function($http, $q){
        this.doPedido = function(arrayProd){
            var deferred = $q.defer();
            var formData = new FormData();
            var nombres = "";
            var unidades = "";
            for (i = 0; i < arrayProd.length; i++) {
                if(i==0){
                    nombres = arrayProd[i]["nombre"]
                    unidades = arrayProd[i]["unidad"]
                }else{
                    nombres = nombres+","+arrayProd[i]["nombre"]
                    unidades = unidades+","+arrayProd[i]["unidad"]
                }
            }
            formData.append("nombres", nombres);
            formData.append("unidades", unidades);

            return $http.post("/ajax_view", formData, {
                headers: {
                    "Content-type": undefined
                },
            })
            .success(function (res){
                deferred.resolve(res);
                window.location="/pedidos";
                //setTimeout("location.href='/pedidos'", 1000);
            })
            .error(function(msg, code){
                deferred.reject(msg);
            })

            return deferred.promise;
        }
    }])
