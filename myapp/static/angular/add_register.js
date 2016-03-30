angular
    .module("adminProducto", [])
    .controller("productoCtrl", function($scope, $http){
        $scope.producto={};
        if(document.getElementById("url")){
            $scope.url = "/product_data/"+document.getElementById("url").value;
            $http.get($scope.url).then(function (response) {
                $scope.producto = response.data.producto;
            });
        }

    });

angular
    .module("listProducto", [])
    .controller("prodCtrl", function($http){
        var scope= this;
        scope.buscar= 100000000;
        scope.productos = [];
        $http.get("/products_data").then(function (response) {
            scope.productos = response.data.productos;
        });
        scope.nofiltrar = function(){
            scope.buscar= 100000000;
        }
        scope.filtrar = function(){
            scope.buscar= 10;
        }
        scope.predicate = 'nombre';
        scope.reverse = true;
        scope.order = function (por){
            if(scope.predicate === por){
                scope.reverse = !scope.reverse;
            }else{
                scope.reverse = false;
            }
            scope.predicate = por;
        }
        scope.ver = function(indice){
            var url='/product/'+scope.productos[indice].nombre;
            location=url;
        }
    })
    .filter('falta', function(){
        return function(input, limit){
            var out = [];
            angular.forEach(input, function(p){
                if(p.inventario <= limit){
                    out.push(p)
                }
            })
            return out;
        }
    })