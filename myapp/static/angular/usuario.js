angular
    .module("adminUsuario", [])
    .controller("usuarioCtrl", function(){
        var scope= this;

        scope.submitForm = function (formData) {
            console.log("Datos: ");
            console.log(typeof(formData));
        };

    });