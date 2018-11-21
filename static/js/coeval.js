function jumpTo(anchor) {
	document.getElementById(anchor).scrollIntoView();
}

/* Home page */

function addCoev() {
    document.getElementById("add-coev-form").style.display = "block";
    document.getElementById("add-curso-form").style.display = "none";
    document.getElementById("add-coev-btn").classList.add("active");
    document.getElementById("add-curso-btn").classList.remove("active");
}

function addCurso() {
    document.getElementById("add-coev-form").style.display = "none";
    document.getElementById("add-curso-form").style.display = "block";
    document.getElementById("add-coev-btn").classList.remove("active");
    document.getElementById("add-curso-btn").classList.add("active");
}

function cancelAdd() {
    document.getElementById("add-coev-form").style.display = "none";
    document.getElementById("add-curso-form").style.display = "none";
    document.getElementById("add-coev-btn").classList.remove("active");
    document.getElementById("add-curso-btn").classList.remove("active");
}

/* Perfil */

function changePass() {
    document.getElementById("cambiar-contrasena").style.display = "block";
    document.getElementById("notas-resumen").style.display = "none";
    document.getElementById("notas-placeholder").style.display = "none";
    document.getElementById("change-pass-btn").classList.add("active");
    //document.getElementById("row-btn").classList.remove("active");
}

function loadCurso(id_curso) {
    cursocodigo = document.getElementById("cursocodigo"+id_curso).textContent;
    cursoano = document.getElementById("cursoano"+id_curso).textContent;
    return cursocodigo+', '+cursoano;
}

function showNotas(id_curso, n_cursos, n_coev) {
    //alert(n_coev);
    document.getElementById("currentCurso").innerHTML = loadCurso(id_curso);
    document.getElementById("cambiar-contrasena").style.display = "none";
    document.getElementById("notas-resumen").style.display = "block";
    document.getElementById("notas-placeholder").style.display = "none";
    //document.getElementById("row-btn"+id_curso).classList.add("active");

    //alert(id_curso);
    for(i = 0; i<= n_cursos; i++){
        //alert('hola');
        for(j = 0; j<=n_coev; j++){
            idval=i+"-"+j;
            //alert("agregar " + idval);
            if (i === id_curso) {
                try{
                    //alert("agregar " + idval);
                    document.getElementById(idval).style.display = "table-row";
                    document.getElementById("row-btn"+id_curso).classList.add("active");
                }catch{}
            } else {
                //alert("remover " + i);
                try {
                    document.getElementById(idval).style.display = "none";
                    //document.getElementById("row-btn" + id_curso).classList.remove("active");
                } catch {
                }
            }
        //alert("endfor")
        }
    }

    var changePass = document.getElementById("change-pass-btn");
    if (changePass !== null) changePass.classList.remove("active");
}


function cancelPass() {
    document.getElementById("cambiar-contrasena").style.display = "none";
    document.getElementById("notas-resumen").style.display = "none";
    document.getElementById("change-pass-btn").classList.add("active");
    document.getElementById("notas-placeholder").style.display = "block";
}

/* Gestión Curso */

function showGestionEstudiante() {
    document.getElementById("gestion-grupo").style.display = "none";
    document.getElementById("gestion-estudiante").style.display = "block";
    document.getElementById("gestion-placeholder").style.display = "none";
    document.getElementById("active-estudiante").classList.add("active");
    document.getElementById("active-grupo").classList.remove("active");
}

function showGestionGrupo() {
    document.getElementById("gestion-grupo").style.display = "block";
    document.getElementById("gestion-estudiante").style.display = "none";
    document.getElementById("gestion-placeholder").style.display = "none";
    document.getElementById("active-grupo").classList.add("active");
    document.getElementById("active-estudiante").classList.remove("active");
}