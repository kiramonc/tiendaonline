angular
    .module("appangular", [])
    .controller("HomeCtrl", function(){
        var scope= this;
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
    });