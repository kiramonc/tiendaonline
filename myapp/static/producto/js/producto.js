angular
    .module("productoModulo", [])
    .directive("productoform", function(){
        return{
            restrict: 'E',
            replace: true,
            templateUrl: '/static/producto/html/productoform.pt'
        };
    });