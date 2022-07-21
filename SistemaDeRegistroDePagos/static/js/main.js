


//---------Para que el menu se active segun cada url-------
// $(function() {
//   $('#menu').metisMenu();
// });
$(function() {
  var url = window.location;

  var element = $('ul.nav a').filter(function() {
      return this.href == url || url.href.indexOf(this.href) == 0;
  }).addClass('active').parent().parent().addClass('in').parent();
  if (element.is('li')) {
      element.addClass('active');
  }

  $('#li-inicio-menu').removeClass('active');
  $('#a-inicio-menu').removeClass('active');
  $('#sub-item-1').removeClass("in");

});
//----------Fin de menu--------------

/*Plugin para el idioma del datatable*/
$(document).ready(function() {
    $('#dataTables-example').DataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
      },
      "order": [],
    });
  });

// Funcion para buscar propietarios en vista seleccionar propietario ya registrado
function buscarPropietarios() {
    // Declare variables
    var input, filter, select, option, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    select = document.getElementById("id_propietarios");
    option = select.getElementsByTagName('option');
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < option.length; i++) {
      txtValue = option[i].innerHTML;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        option[i].style.display = "";
      } else {
        option[i].style.display = "none";
      }
    }
}

// Funciones para eliminar condiciones de pago
function eliminar_con(){
  let form = document.getElementById("eliminarCondiciones");
  form.submit();
 }

 function confirmacionEliminarCondiciones(){
  Swal.fire({
    "title":"¿Esta seguro de eliminar las condiciones de pago?",
    "text":"Se eliminaran de manera permanente",
    "icon":"question",
    "showCancelButton":true,
    "cancelButtonText":"Cancelar",
    "confirmButtonText":"Eliminar",
    "confirmButtonColor":"Red",

  })
  .then(function(result){
      if(result.isConfirmed)[
          eliminar_con()
      ]
  })
}

// Funciones para eliminar prima
function eliminarPrima(proyecto, detalleVenta, id){
  Swal.fire({
    "title":"¿Esta seguro de eliminar la prima?",
    "text":"Se eliminara de manera permanente",
    "icon":"question",
    "showCancelButton":true,
    "cancelButtonText":"Cancelar",
    "confirmButtonText":"Eliminar",
    "confirmButtonColor":"Red",

  })
  .then(function(result){
      if(result.isConfirmed)[
          window.location.href = "/eliminarPrima/"+proyecto+"/"+detalleVenta+"/"+id+"/"
      ]
  })

}

/* Validaciones formulario agregar propietario*/
(function(){

  // Inputmask("9{8}[-]9{1}", {
  //   placeholder: "",
  //   greedy: false
  // }).mask('#id_dui');

  Inputmask("9{4}[-]9{4}", {
    placeholder: "",
    greedy: false
  }).mask('#id_telefonoTrabajo');

  Inputmask("9{4}[-]9{4}", {
    placeholder: "",
    greedy: false
  }).mask('#id_telefonoCasa');

  Inputmask("9{4}[-]9{4}", {
    placeholder: "",
    greedy: false
  }).mask('#id_telefonoCelular');
})();

 