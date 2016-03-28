angular
    .module("adminUsuario", ['LocalStorageModule'])
    .config(['localStorageServiceProvider', function(localStorageServiceProvider){
        localStorageServiceProvider.setPrefix('ls');
    }])
    .controller("usuarioCtrl", function(localStorageService){
        var scope= this;
        if (localStorageService.get("ls.productos")) {
          scope.productos = localStorageService.get("ls.productos");
        } else {
          scope.productos=[];
        }
        var inputConfirmar = document.getElementById("inputPasswordConfirm");
        var inputPass = document.getElementById("inputPassword");
        var inputPassr = document.getElementById("inputPasswordR");
        var botonActualizar = document.getElementById("botonActualizar");
        scope.clase={error:false}
        scope.user = {};
        scope.cambio = 'f';
        scope.submitForm = function (formData) {
            console.log("Datos: ");
            console.log(typeof(formData));
        };
        scope.userEdit= function(usuario){
            console.log(usuario.nombre);
        };

        scope.comprobarPass = function(){
            if(scope.passwordConfirm==scope.password){
                scope.password="";
            }
        }

        scope.establecerVacio = function(){
            inputPass.value="";
            inputPassr.value="";
        }

        scope.cambiarPass = function(){
            if(scope.cambio==='t'){
                inputConfirmar.setAttribute("required", '');
                inputPass.setAttribute("required", '');
                inputPassr.setAttribute("required", '');
                botonActualizar.setAttribute("disabled","disabled")
            }else{
                inputConfirmar.removeAttribute("required");
                inputPass.removeAttribute("required");
                inputPassr.removeAttribute("required");
                inputConfirmar.value="";
                scope.establecerVacio();
                inputPassr.removeAttribute("disabled");
            }
        }

        scope.reset = function(){
            scope.productos=[];
            console.log("Carrito reseteado");
            localStorageService.remove("ls.productos");
        }

    })
    .directive('passMatch', [function () {
        return {
            require: 'ngModel',
            link: function (scope, elem, attrs, ctrl) {
                var password = '#' + attrs.passMatch;
                elem.add(password).on('keyup', function () {
                    scope.$apply(function () {
                        ctrl.$setValidity('pwmatch', elem.val() === $(password).val());
                    });
                });
            }
        }
    }]);