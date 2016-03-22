angular
    .module("adminPedido", [])
    .controller("pedidoCtrl", function(save){
        var scope= this;
        scope.productos = [{"nombre": "Prod1", "unidad": 1},
        {"nombre": "Prod2", "unidad": 4}];

        scope.enviar = function (data) {
            save.doPedido(scope.productos).then(function(res){
                console.log("carga terminada");
            })
        };
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
//                window.location="/pedidos";
                setTimeout("location.href='/pedidos'", 1000);
            })
            .error(function(msg, code){
                deferred.reject(msg);
            })

            return deferred.promise;
        }
    }])