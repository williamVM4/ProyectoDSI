$(document).ready(function() {
    $('#dataTables-example').DataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
      }
    });
  });

  function myFunction() {
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

 