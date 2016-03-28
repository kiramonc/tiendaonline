angular
    .module("adminProducto", ['LocalStorageModule'])
    .config(['localStorageServiceProvider', function(localStorageServiceProvider){
        localStorageServiceProvider.setPrefix('ls');
    }])
    .controller("productoCtrl", function(localStorageService){
        var scope= this;
        if (localStorageService.get("ls.productos")) {
          scope.productos = localStorageService.get("ls.productos");
        } else {
          scope.productos=[];
        }

        scope.submitForm = function (formData) {
            console.log("Datos: ");
            console.log(typeof(formData));
            scope.save_form = 'valido';
        };

        scope.loadProductos = function(productoId){
            scope.getProductos(productoId).then(
                function(response){
                    var productoArray = response.data.productos;
                    console.log(JSON.stringify(productoArray))
                    scope.formData= productoArray;
                }
            )

        };

        scope.reset = function(){
            scope.productos=[];
            console.log("Carrito reseteado");
            localStorageService.remove("ls.productos");
        }

        scope.tipo="";
        scope.mostrar=false;
        scope.verTipo = function($scope){
        var datos= $scope.formData;
            console.log("Datos");
            console.log(datos);
            scope.mostrar=true;
            scope.tipo = typeof(datos);
        }

    });