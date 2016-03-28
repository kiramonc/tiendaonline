function mostrarMsj(){
    var contenedorMsj = document.getElementById("msj");
    console.log("Mensaje");
    console.log(contenedorMsj.innerHTML);
    if(contenedorMsj.innerHTML == ''){
        return true;
    }
    return false;
}
angular
    .module("appangular", ['LocalStorageModule'])
    .config(['localStorageServiceProvider', function(localStorageServiceProvider){
        localStorageServiceProvider.setPrefix('ls');
    }])
    .controller("HomeCtrl", function(localStorageService){
        var scope= this;
        if (localStorageService.get("ls.productos")) {
          scope.productos = localStorageService.get("ls.productos");
        } else {
          scope.productos=[];
        }
        scope.producto=[{nombre: 'Nuevo', descripcion: 'Vacio', inventario:"3"},
                    {nombre: 'NOOOOOo1', descripcion: 'Vacio1',inventario:"3"}
        ];

        scope.booleanForm= false;

        scope.switchState = function(){
            scope.booleanForm= true;
        }

        scope.save = function(){
            scope.producto.push({nombre: scope.newProduct.nombre, descripcion: scope.newProduct.descripcion, inventario:scope.newProduct.inventario});
            scope.booleanForm= false;
            scope.newProduct={};
        }

        scope.reset = function(){
            scope.productos=[];
            console.log("Carrito reseteado");
            localStorageService.remove("ls.productos");
        }
    });