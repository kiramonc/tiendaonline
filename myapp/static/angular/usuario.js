angular
    .module("adminUser", [])
    .controller("userCtrl", function($scope, $http){
        var inputPass = document.getElementById("inputPassword");
        var inputPassr = document.getElementById("inputPasswordR");
        $scope.cambio = 'f';

        $scope.usuario={};
        if(document.getElementById("url")){
            $scope.url = "/user_data/"+document.getElementById("url").value;
            $http.get($scope.url).then(function (response) {
                $scope.usuario = response.data.usuario;
            });
        }

        $scope.comprobarPass = function(){
            if($scope.passwordConfirm==$scope.password){
                $scope.password="";
            }
        }

        $scope.establecerVacio = function(){
            $scope.formData.password="";
            $scope.formData.passwordR="";
        }

        $scope.cambiarPass = function(){
            if($scope.cambio==='t'){
                inputPass.setAttribute("required", '');
                inputPassr.setAttribute("required", '');
            }else{
                inputPass.removeAttribute("required");
                inputPassr.removeAttribute("required");
                $scope.establecerVacio();
                inputPassr.removeAttribute("disabled");
            }
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

angular
    .module("adminUsuario", [])
    .controller("usuarioCtrl", function($http){
        var scope= this;

        scope.usuarios=[];
        $http.get("/users_data").then(function (response) {
            scope.usuarios = response.data.usuarios;
            console.log(scope.usuarios)
        });
    })
    .filter('typeuser', function(){
        return function(input){
            if(input == "admins"){
                return "Administrador";
            }else{
                return "Cliente";
            }
        }
    });

angular
    .module("adminCuenta", ['LocalStorageModule'])
    .config(['localStorageServiceProvider', function(localStorageServiceProvider){
        localStorageServiceProvider.setPrefix('ls');
    }])
    .controller("cuentaCtrl", function(localStorageService){
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
        scope.cambio = 'f';

        scope.comprobarPass = function(){
            if(scope.passwordConfirm==scope.password){
                scope.password="";
            }
        }

        scope.establecerVacio = function(){
            scope.formData.password="";
            scope.formData.passwordR="";
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