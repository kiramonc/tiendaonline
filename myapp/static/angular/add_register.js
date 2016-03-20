angular
    .module("adminProducto", [])
    .controller("productoCtrl", function(){
        var scope= this;

        scope.submitForm = function (formData) {
            console.log("Datos: ");
            console.log(typeof(formData));
            alert('Form submitted with' + JSON.stringify(formData));
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