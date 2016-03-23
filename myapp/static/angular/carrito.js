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
            console.log(data);
            $scope.productos.push({"nombre": data, "precio": precio, "stock": stock, "unidad": 1});
            console.log($scope.productos);
            localStorageService.set("ls.productos", $scope.productos);
        };

        $scope.eliminar = function (indice) {
            console.log(indice);
            $scope.productos.splice(indice, 1)
            console.log($scope.productos);
            localStorageService.set("ls.productos", $scope.productos);
        };

        $scope.editar = function (indice) {
            console.log($scope.productos[indice]);
            localStorageService.set("ls.productos", $scope.productos);

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
            console.log(data)
            console.log(url)
            window.location=url;
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
                console.log("Exitoso: "+ res.message);

                window.location="/pedidos";
                //setTimeout("location.href='/pedidos'", 1000);
            })
            .error(function(msg, code){
                deferred.reject(msg);
            })

            return deferred.promise;
        }
    }])
