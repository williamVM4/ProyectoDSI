/*FORMULARIO DE AGREGAR CUENTA BANCARIA*/
const formularioCuentaBancaria = document.getElementById('AgregarCuentaBancaria');
const inputsCuentaBancaria = document.querySelectorAll('#AgregarCuentaBancaria input');
const expresiones = {
	nombrePropio: /^([A-ZÀ-ÿ]{1}[A-Za-zÀ-ÿ]+[\s]*)+$/,
	numeroCuentabancaria:/[0-9]{6,20}/,
}

const campos = {
	//Cuentas bancarias
	numeroCuentaBancaria:false,
	nombreCuentaBancaria:false,
	tipoCuenta:false,
	banco:false
}

const validarFormularioCuentaBancaria = (e) => {
	switch (e.target.name) {
		case "numeroCuentaBancaria": validar(expresiones.numeroCuentabancaria, e.target, 'numeroCuentaBancaria');break;
		case "nombreCuentaBancaria": validar(expresiones.nombrePropio, e.target, 'nombreCuentaBancaria'); break;
		case "tipoCuenta": validar(expresiones.nombrePropio, e.target, 'tipoCuenta'); break;
		case "banco": validar(expresiones.nombrePropio, e.target, 'banco'); break;
	}
}
const validar = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
		document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}

inputsCuentaBancaria.forEach((input) => {
	input.addEventListener('keyup', validarFormularioCuentaBancaria);
	input.addEventListener('blur', validarFormularioCuentaBancaria);
});

formularioCuentaBancaria.addEventListener('submit', (e) => {
	if(campos.numeroCuentaBancaria && campos.nombreCuentaBancaria && campos.tipoCuenta && campos.banco){
		$('form').submit(function(e){
			$('form').unbind('submit').submit()
		});
	} else {
		e.preventDefault();
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
});
